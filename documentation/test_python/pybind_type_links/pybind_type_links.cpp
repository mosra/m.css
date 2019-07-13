#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

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

void typeNested(const std::pair<Foo, std::vector<Enum>>&) {}

}

PYBIND11_MODULE(pybind_type_links, m) {
    m.doc() = "pybind11 type linking";

    py::enum_<Enum>{m, "Enum", "An enum"}
        .value("FIRST", Enum::First)
        .value("SECOND", Enum::Second);

    py::class_<Foo> foo{m, "Foo", "A class"};
    foo
        .def(py::init<Enum>(), "Constructor")
        .def_readwrite("property", &Foo::property, "A property");

    m
        .def("type_enum", &typeEnum, "A function taking an enum", py::arg("value") = Enum::Second)
        .def("type_return", &typeReturn, "A function returning a type")
        .def("type_nested", &typeNested, "A function with nested type annotation");

    /* Test also attributes (annotated from within Python) */
    m.attr("TYPE_DATA") = Foo{Enum::First};
    foo.attr("TYPE_DATA") = Enum::Second;
}
