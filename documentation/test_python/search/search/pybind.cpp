#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

struct Foo {
    void method() {}
    void methodWithParams(int, float) {}
};

void overloadedFunction(int b, float) {}
void overloadedFunction(int b) {}
void overloadedFunction(int b, Foo) {}

}

PYBIND11_MODULE(pybind, m) {
    py::class_<Foo>{m, "Foo"}
        .def("method", &Foo::method)
        .def("method_with_params", &Foo::methodWithParams, py::arg("first"), py::arg("second"));

    m
        .def("overloaded_function", static_cast<void(*)(int, float)>(&overloadedFunction))
        .def("overloaded_function", static_cast<void(*)(int)>(&overloadedFunction))
        .def("overloaded_function", static_cast<void(*)(int, Foo)>(&overloadedFunction));
}
