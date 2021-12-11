#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <ceres/ceres.h>
#include <Eigen/Core>
#include <SO3.h>
#include <SE3.h>

namespace py = pybind11;

// AutoDiff local parameterization for the SO3 rotation [q] object. 
// The boxplus operator informs Ceres how the manifold evolves and also  
// allows for the calculation of derivatives.
struct SO3Plus {
  // boxplus operator for both doubles and jets
  template<typename T>
  bool operator()(const T* x, const T* delta, T* x_plus_delta) const
  {
    SO3<T> X(x);
    Eigen::Map<const Eigen::Matrix<T, 3, 1>> dX(delta);
    
    SO3<T> Y = X + dX;
    
    Eigen::Map<Eigen::Matrix<T, 4, 1>> Yvec(x_plus_delta);
    Yvec << Y.array();

    return true;
  }
  
  // local parameterization generator--ONLY FOR PYTHON WRAPPER
  static ceres::LocalParameterization *Create() {
    return new ceres::AutoDiffLocalParameterization<SO3Plus,
                                                    4,
                                                    3>(new SO3Plus);
  }
};

// AutoDiff local parameterization for the compact SE3 pose [t q] object. 
// The boxplus operator informs Ceres how the manifold evolves and also  
// allows for the calculation of derivatives.
struct SE3Plus {
  // boxplus operator for both doubles and jets
  template<typename T>
  bool operator()(const T* x, const T* delta, T* x_plus_delta) const
  {
    SE3<T> X(x);
    Eigen::Map<const Eigen::Matrix<T, 6, 1>> dX(delta);
    
    SE3<T> Y = X + dX;
    
    Eigen::Map<Eigen::Matrix<T, 7, 1>> Yvec(x_plus_delta);
    Yvec << Y.array();

    return true;
  }
  
  // local parameterization generator--ONLY FOR PYTHON WRAPPER
  static ceres::LocalParameterization *Create() {
    return new ceres::AutoDiffLocalParameterization<SE3Plus,
                                                    7,
                                                    6>(new SE3Plus);
  }
};

// AutoDiff cost function (factor) for the difference between two rotations.
// Weighted by measurement covariance, Qij_.
class SO3Functor
{
public:
EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  // store measured relative pose and inverted covariance matrix
  SO3Functor(Eigen::Matrix<double,4,1> &qi_vec, Eigen::Matrix<double,3,3> &Qij)
  : q_(qi_vec)
  {
    Qij_inv_ = Qij.inverse();
  }

  // templated residual definition for both doubles and jets
  // basically a weighted implementation of boxminus using Eigen templated types
  template<typename T>
  bool operator()(const T* _q_hat, T* _res) const
  {
    SO3<T> q_hat(_q_hat);
    Eigen::Map<Eigen::Matrix<T,3,1>> r(_res);
    
    r = Qij_inv_.cast<T>() * (q_hat - q_.cast<T>());
    
    return true;
  }

  // cost function generator--ONLY FOR PYTHON WRAPPER
  static ceres::CostFunction *Create(Eigen::Matrix<double,4,1> &qi, Eigen::Matrix<double,3,3> &Qij) {
    return new ceres::AutoDiffCostFunction<SO3Functor,
                                           3,
                                           4>(new SO3Functor(qi, Qij));
  }

private:
  SO3d q_;
  Eigen::Matrix<double,3,3> Qij_inv_;
};

class DeltaSO3Functor
{
public:
EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  DeltaSO3Functor(Eigen::Matrix<double,4,1> &qij_vec, Eigen::Matrix<double,3,3> &Qij) : qij_(qij_vec)
  {
    Qij_inv_ = Qij.inverse();
  }

  template<typename T>
  bool operator()(const T* _qi_hat, const T* _qj_hat, T* _res) const
  {
    SO3<T> qi_hat(_qi_hat);
    SO3<T> qj_hat(_qj_hat);
    Eigen::Map<Eigen::Matrix<T,3,1>> r(_res);
    
    r = Qij_inv_.cast<T>() * (qi_hat.inverse() * qj_hat - qij_.cast<T>());  

    return true;
  }

  static ceres::CostFunction *Create(Eigen::Matrix<double,4,1> &qij, Eigen::Matrix<double,3,3> &Qij) {
    return new ceres::AutoDiffCostFunction<DeltaSO3Functor,
                                           3,
                                           4,
                                           4>(new DeltaSO3Functor(qij, Qij));
  }

private:
  SO3d qij_;
  Eigen::Matrix<double,3,3> Qij_inv_;
};

class SE3Functor
{
public:
EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  SE3Functor(Eigen::Matrix<double,7,1> &T_vec, Eigen::Matrix<double,6,6> &Q) : T_(T_vec)
  {
    Q_inv_ = Q.inverse();
  }
  
  template<typename T>
  bool operator()(const T* _T_hat, T* _res) const
  {
    SE3<T> T_hat(_T_hat);
    Eigen::Map<Eigen::Matrix<T,6,1>> r(_res);
    
    r = Q_inv_.cast<T>() * (T_hat - T_.cast<T>());
    
    return true;
  }
  
  static ceres::CostFunction *Create(Eigen::Matrix<double,7,1> &T, Eigen::Matrix<double,6,6> &Q) {
    return new ceres::AutoDiffCostFunction<SE3Functor,
                                           6,
                                           7>(new SE3Functor(T, Q));
  }
  
private:
  SE3d T_;
  Eigen::Matrix<double,6,6> Q_inv_;
};

// AutoDiff cost function (factor) for the difference between a measured 3D
// relative transform, Xij = (tij_, qij_), and the relative transform between two  
// estimated poses, Xi_hat and Xj_hat. Weighted by measurement covariance, Qij_.
class DeltaSE3Functor
{
public:
EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  // store measured relative pose and inverted covariance matrix
  DeltaSE3Functor(Eigen::Matrix<double,7,1> &Xij_vec, Eigen::Matrix<double,6,6> &Qij) : Xij_(Xij_vec)
  {
    Qij_inv_ = Qij.inverse();
  }

  // templated residual definition for both doubles and jets
  // basically a weighted implementation of boxminus using Eigen templated types
  template<typename T>
  bool operator()(const T* _Xi_hat, const T* _Xj_hat, T* _res) const
  {
    SE3<T> Xi_hat(_Xi_hat);
    SE3<T> Xj_hat(_Xj_hat);
    Eigen::Map<Eigen::Matrix<T,6,1>> r(_res);
    
    r = Qij_inv_.cast<T>() * (Xi_hat.inverse() * Xj_hat - Xij_.cast<T>());  

    return true;
  }

  // cost function generator--ONLY FOR PYTHON WRAPPER
  static ceres::CostFunction *Create(Eigen::Matrix<double,7,1> &Xij, Eigen::Matrix<double,6,6> &Qij) {
    return new ceres::AutoDiffCostFunction<DeltaSE3Functor,
                                           6,
                                           7,
                                           7>(new DeltaSE3Functor(Xij, Qij));
  }

private:
  SE3d Xij_;
  Eigen::Matrix<double,6,6> Qij_inv_;
};

void add_custom_cost_functions(py::module &m) {

  // Use pybind11 code to wrap your own cost function which is defined in C++

  // SO3 Factors
  m.def("SO3Parameterization", &SO3Plus::Create);
  m.def("SO3Factor", &SO3Functor::Create);
  m.def("DeltaSO3Factor", &DeltaSO3Functor::Create);

  // SE3 Factors
  m.def("SE3Parameterization", &SE3Plus::Create);
  m.def("SE3Factor", &SE3Functor::Create);
  m.def("DeltaSE3Factor", &DeltaSE3Functor::Create);

}
