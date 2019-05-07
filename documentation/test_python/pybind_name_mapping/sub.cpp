#include <pybind11/pybind11.h>

struct Foo {
    static Foo aThing() { return {}; }
};

PYBIND11_MODULE(_sub, m) {
    pybind11::class_<Foo>{m, "Foo", "A class, renamed from Foo to Class"}
        .def("a_thing", &Foo::aThing, "A method");

    pybind11::module bar = m.def_submodule("bar");
    bar.doc() = "This submodule is renamed from bar to submodule and should have a function member.";
    bar.def("foo", [](Foo, int a) { return a*2; }, "A function");
}
