#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

void function() {}
void functionWithParams(int, float) {}

struct Foo {
    void overloadedMethod1(int, float) {}
    void overloadedMethod2(int) {}
    void overloadedMethod3(int, Foo) {}
};

}

PYBIND11_MODULE(pybind, m) {
    m.def("function", &function)
     .def("function_with_params", &functionWithParams, py::arg("first"), py::arg("second"));

    py::class_<Foo>{m, "Foo"}
        .def("overloaded_method", &Foo::overloadedMethod1, py::arg("first"), py::arg("second"))
        .def("overloaded_method", &Foo::overloadedMethod2)
        .def("overloaded_method", &Foo::overloadedMethod3);
}
