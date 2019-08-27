#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> /* needed for std::vector! */
#include <pybind11/functional.h> /* for std::function */

namespace py = pybind11;

void foo1(int, const std::tuple<int, std::string>&) {}
void foo2(std::function<int(float, std::vector<float>&)>) {}
void foo3(std::string) {}
void foo4(int) {}

struct Class {
    void foo1(int) {}
    void foo2(std::string) {}
};

PYBIND11_MODULE(pybind_external_overload_docs, m) {
    m.doc() = "pybind11 external overload docs";

    m
        .def("foo", &foo1, "First overload", py::arg("a"), py::arg("b"))
        .def("foo", &foo2, "Second overload")
        .def("foo", &foo3, "Third overload", py::arg("name"))
        .def("foo", &foo4, "Fourth overload", py::arg("param") = 4)
        .def("foo", &foo4, "This will produce param documentation mismatch warnings", py::arg("first"));

    py::class_<Class>(m, "Class", "My fun class!")
        .def("foo", &Class::foo1, "First overload", py::arg("index"))
        .def("foo", &Class::foo2, "Second overload", py::arg("name"));
}
