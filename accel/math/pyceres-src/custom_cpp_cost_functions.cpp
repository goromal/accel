#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <ceres/ceres.h>
#include <Eigen/Core>
#include <Eigen/Geometry>

namespace py = pybind11;

// AutoDiff local parameterization for the SO3 rotation [q] object. 
// The boxplus operator informs Ceres how the manifold evolves and also  
// allows for the calculation of derivatives.
struct SO3Plus {
  // boxplus operator for both doubles and jets
  template<typename T>
  bool operator()(const T* x, const T* delta, T* x_plus_delta) const
  {
    // // capture argument memory TODO (ajt)
    // Sophus::SE3<T> X;
    // cSE3convert(x, X);
    // Eigen::Map<const Eigen::Matrix<T, 6, 1>> dX(delta);
    // Eigen::Map<Eigen::Matrix<T, 7, 1>>       Yvec(x_plus_delta);

    // // increment pose using the exponential map
    // Sophus::SE3<T> Exp_dX = Sophus::SE3<T>::exp(dX);
    // Sophus::SE3<T> Y = X * Exp_dX;

    // // assign SE3 coefficients to compact vector
    // Eigen::Matrix<T,7,1> YvecCoef;
    // cSE3convert(Y, YvecCoef);
    // Yvec = YvecCoef;

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
    // // capture argument memory TODO (ajt)
    // Sophus::SE3<T> X;
    // cSE3convert(x, X);
    // Eigen::Map<const Eigen::Matrix<T, 6, 1>> dX(delta);
    // Eigen::Map<Eigen::Matrix<T, 7, 1>>       Yvec(x_plus_delta);

    // // increment pose using the exponential map
    // Sophus::SE3<T> Exp_dX = Sophus::SE3<T>::exp(dX);
    // Sophus::SE3<T> Y = X * Exp_dX;

    // // assign SE3 coefficients to compact vector
    // Eigen::Matrix<T,7,1> YvecCoef;
    // cSE3convert(Y, YvecCoef);
    // Yvec = YvecCoef;

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
  SO3Functor(Eigen::Matrix<double,4,1> &qi_vec, Eigen::Matrix<double,6,6> &Qij)
  {
    // Sophus::SE3<double> Xij;
    // cSE3convert(Xij_vec, Xij);
    // Xij_inv_ = Xij.inverse();
    // Qij_inv_ = Qij.inverse();
  }

  // templated residual definition for both doubles and jets
  // basically a weighted implementation of boxminus using Eigen templated types
  template<typename T>
  bool operator()(const T* _Xi_hat, const T* _Xj_hat, T* _res) const
  {
    // // assign memory to usable objects
    // Sophus::SE3<T> Xi_hat, Xj_hat;
    // cSE3convert(_Xi_hat, Xi_hat);
    // cSE3convert(_Xj_hat, Xj_hat);
    // Eigen::Map<Eigen::Matrix<T,6,1>> r(_res);

    // // compute current estimated relative pose
    // const Sophus::SE3<T> Xij_hat = Xi_hat.inverse() * Xj_hat;

    // // compute residual via boxminus (i.e., the logarithmic map of the error pose)
    // // weight with inverse covariance
    // r = Qij_inv_.cast<T>() * (Xij_inv_.cast<T>() * Xij_hat).log();  

    return true;
  }

  // cost function generator--ONLY FOR PYTHON WRAPPER
  static ceres::CostFunction *Create(Eigen::Matrix<double,4,1> &Xij, Eigen::Matrix<double,3,3> &Qij) {
    return new ceres::AutoDiffCostFunction<SO3Functor,
                                           6,
                                           7,
                                           7>(new SO3Functor(Xij, Qij));
  }

private:
  Sophus::SE3<double> Xij_inv_;
  Eigen::Matrix<double,6,6> Qij_inv_;
};

// AutoDiff cost function (factor) for the difference between a measured 3D
// relative transform, Xij = (tij_, qij_), and the relative transform between two  
// estimated poses, Xi_hat and Xj_hat. Weighted by measurement covariance, Qij_.
class SE3Functor
{
public:
EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  // store measured relative pose and inverted covariance matrix
  SE3Functor(Eigen::Matrix<double,7,1> &Xij_vec, Eigen::Matrix<double,6,6> &Qij)
  {
    // Sophus::SE3<double> Xij;
    // cSE3convert(Xij_vec, Xij);
    // Xij_inv_ = Xij.inverse();
    // Qij_inv_ = Qij.inverse();
  }

  // templated residual definition for both doubles and jets
  // basically a weighted implementation of boxminus using Eigen templated types
  template<typename T>
  bool operator()(const T* _Xi_hat, const T* _Xj_hat, T* _res) const
  {
    // // assign memory to usable objects
    // Sophus::SE3<T> Xi_hat, Xj_hat;
    // cSE3convert(_Xi_hat, Xi_hat);
    // cSE3convert(_Xj_hat, Xj_hat);
    // Eigen::Map<Eigen::Matrix<T,6,1>> r(_res);

    // // compute current estimated relative pose
    // const Sophus::SE3<T> Xij_hat = Xi_hat.inverse() * Xj_hat;

    // // compute residual via boxminus (i.e., the logarithmic map of the error pose)
    // // weight with inverse covariance
    // r = Qij_inv_.cast<T>() * (Xij_inv_.cast<T>() * Xij_hat).log();  

    return true;
  }

  // cost function generator--ONLY FOR PYTHON WRAPPER
  static ceres::CostFunction *Create(Eigen::Matrix<double,7,1> &Xij, Eigen::Matrix<double,6,6> &Qij) {
    return new ceres::AutoDiffCostFunction<SE3Functor,
                                           6,
                                           7,
                                           7>(new SE3Functor(Xij, Qij));
  }

private:
  Sophus::SE3<double> Xij_inv_;
  Eigen::Matrix<double,6,6> Qij_inv_;
};

void add_custom_cost_functions(py::module &m) {

  // Use pybind11 code to wrap your own cost function which is defined in C++

  // // SO3 Factors
  // m.def("SO3Parameterization", &SO3Plus::Create);
  // m.def("SO3Factor", &SO3Functor::Create);

  // // SE3 Factors
  // m.def("SE3Parameterization", &SE3Plus::Create);
  // m.def("SE3Factor", &SE3Functor::Create);

}
