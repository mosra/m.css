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

struct Class26 {
    void foo1(int) {}
    void foo2(int, float, const std::string&) {}
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

    py::class_<Class26> pybind26{m, "Class26", "Pybind 2.6 features"};

    /* Checker so the Python side can detect if testing pybind 2.6 features is
       feasible */
    pybind26.attr("is_pybind26") =
        #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 206
        true
        #else
        false
        #endif
        ;

    #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 206
    pybind26
        .def("foo", &Class26::foo2, "Positional and keyword-only arguments", py::arg("a"), py::pos_only{}, py::arg("b"), py::kw_only{}, py::arg("keyword"));
    #endif
}
