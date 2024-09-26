#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;

namespace {

struct Foo {};

std::function<int()> function(const Foo&) { return []{ return 3; }; }

}

PYBIND11_MODULE(pybind, m) {
    py::class_<Foo>{m.def_submodule("sub"), "Foo"};

    m.def("function", &function);
}
