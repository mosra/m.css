#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> /* needed for std::vector! */
#include <pybind11/functional.h> /* for std::function */

namespace py = pybind11;

int scale(int a, float argument) {
    return int(a*argument);
}

PYBIND11_MODULE(pybind_docstrings, m) {
    m.doc() = "pybind11 function signature extraction";

    m
        .def("scale_kwargs", &scale, R"(Scale an integer, kwargs

    :param a: An integer
    :param argument: Scale factor
    :return: Scaled integer

    Here is a usage examples:

    >>> scale_kwargs(a=10, argument=1.63)
    16

    >>> scale_kwargs(a=3, argument=2.9)
    8

        )", py::arg("a"), py::arg("argument"))
        .def("scale_kwargs", [](int a){ return scale(a, 10); }, R"(Scale integer by 10



    :param a: An integer to scale by 10
    :return: Scaled integer

    Here is a usage example:

    >>> scale_kwargs(a=10)
    100
        )", py::arg("a"));
}
