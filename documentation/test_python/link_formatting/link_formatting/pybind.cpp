#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

struct Foo {
    static int aFunction(int a) { return 5 + a; }

    int foo(int a) { return 3 + a; }

    int bar(int a) { return 5 + a; }
};

int takesInt(int a) { return 3 + a; }

int anOverloadedFunction(int b, float) { return int(b); }
int anOverloadedFunction(int b) { return b; }
int anOverloadedFunction(int b, Foo) { return b; }

}

PYBIND11_MODULE(pybind, m) {
    m.doc() = "pybind11 overloaded function link formatting";

    py::class_<Foo>{m, "Foo", "A class"}
        .def_static("a_function", &Foo::aFunction, "A static function that should have the same hash as takes_int()")
        .def("foo", &Foo::foo, "Should have the same hash as bar() but not as a_function()")
        .def("bar", &Foo::bar, "Should have the same hash as foo() but not as a_function()");

    m
        .def("takes_int", &takesInt, "Should have the same hash as Foo.a_function()")
        .def("an_overloaded_function", static_cast<int(*)(int, float)>(&anOverloadedFunction), "Each overload should have a different hash")
        .def("an_overloaded_function", static_cast<int(*)(int)>(&anOverloadedFunction), "Each overload should have a different hash")
        .def("an_overloaded_function", static_cast<int(*)(int, Foo)>(&anOverloadedFunction), "Each overload should have a different hash");
}
