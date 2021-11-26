#include "utils/quat.h"
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <sstream>

using namespace Eigen;
namespace py = pybind11;

PYBIND11_MODULE(utils_quat, m)
{
  m.doc() = "Python binding module for the utils quat class.";

  py::class_<transforms::Quatd>(m, "Quat")
    .def(py::init())
    .def(py::init<const Ref<const Matrix<double,4,1>>>())
    .def("w", &transforms::Quatd::w)
    .def("x", &transforms::Quatd::x)
    .def("y", &transforms::Quatd::y)
    .def("z", &transforms::Quatd::z)
    .def("setW", &transforms::Quatd::setW)
    .def("setX", &transforms::Quatd::setX)
    .def("setY", &transforms::Quatd::setY)
    .def("setZ", &transforms::Quatd::setZ)
    .def("elements", &transforms::Quatd::elements)
    .def(py::self * py::self)
    .def(py::self + Matrix<double,3,1>())
    .def(py::self - py::self)
    .def("roll", &transforms::Quatd::roll)
    .def("pitch", &transforms::Quatd::pitch)
    .def("yaw", &transforms::Quatd::yaw)
    .def("euler", &transforms::Quatd::euler)
    .def("R", &transforms::Quatd::R)
    .def("normalize", &transforms::Quatd::normalize)
    .def("rota", (Matrix<double, 3, 1> (transforms::Quatd::*) (const Matrix<double, 3, 1>&) const) &transforms::Quatd::rota, "The same as R.T * v but faster")
    .def("rotp", (Matrix<double, 3, 1> (transforms::Quatd::*) (const Matrix<double, 3, 1>&) const) &transforms::Quatd::rotp, "The same as R * v but faster")
    .def("invert", &transforms::Quatd::invert)
    .def("inverse", &transforms::Quatd::inverse)
    .def("__repr__",
      [](const transforms::Quatd &q) {
        std::stringstream ss;
        ss << q;
        return ss.str();
      }
    );

    m.def("skew", &transforms::Quatd::skew);
    m.def("exp", &transforms::Quatd::exp);
    m.def("log", &transforms::Quatd::log);
    m.def("from_R", &transforms::Quatd::from_R);
    m.def("from_axis_angle", &transforms::Quatd::from_axis_angle);
    m.def("from_euler", &transforms::Quatd::from_euler);
    m.def("from_two_unit_vectors", &transforms::Quatd::from_two_unit_vectors);
    m.def("Identity", &transforms::Quatd::Identity);
    m.def("Random", &transforms::Quatd::Random);
}
