#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

void overloadedFunction(int, float) {}
void overloadedFunction(int) {}

}

PYBIND11_MODULE(pybind, m) {
    m
        .def("overloaded_function", static_cast<void(*)(int, float)>(&overloadedFunction))
        .def("overloaded_function", static_cast<void(*)(int)>(&overloadedFunction));
}
