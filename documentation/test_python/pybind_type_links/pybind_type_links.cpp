#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace {

enum class Enum {
    First, Second
};

void typeEnumAndDefault(Enum) {}

struct Foo {
    Enum property;
};

Foo typeReturn() { return {}; }

void typeNested(const std::pair<Foo, std::vector<Enum>>&) {}

void typeNestedEnumAndDefault(std::pair<int, Enum>) {}

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
        .def("type_enum_and_default", &typeEnumAndDefault, "A function taking an enum with a default", py::arg("value") = Enum::Second)
        .def("type_return", &typeReturn, "A function returning a type")
        .def("type_nested", &typeNested, "A function with nested type annotation")
        .def("type_nested_enum_and_default", &typeNestedEnumAndDefault, "A function taking a nested enum with a default. This won't have a link.", py::arg("value") = std::pair<int, Enum>{3, Enum::First});

    /* Test also attributes (annotated from within Python) */
    m.attr("TYPE_DATA") = Foo{Enum::First};
    foo.attr("TYPE_DATA") = Enum::Second;
}
