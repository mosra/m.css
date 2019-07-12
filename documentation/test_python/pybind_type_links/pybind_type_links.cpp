#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

enum class Enum {
    First, Second
};

void typeEnum(Enum) {}

struct Foo {
    Enum property;
};

Foo typeReturn() { return {}; }

}

PYBIND11_MODULE(pybind_type_links, m) {
    m.doc() = "pybind11 type linking";

    py::enum_<Enum>{m, "Enum", "An enum"}
        .value("FIRST", Enum::First)
        .value("SECOND", Enum::Second);

    py::class_<Foo>{m, "Foo", "A class"}
        .def(py::init<Enum>(), "Constructor")
        .def_readwrite("property", &Foo::property, "A property");

    m
        .def("type_enum", &typeEnum, "A function taking an enum")
        .def("type_return", &typeReturn, "A function returning a type");
}
