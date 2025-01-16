#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace {

template<class> struct Foo {};

void overload(short) {}
Foo<int> overload(int) { return {}; }
Foo<float> overload(float) { return {}; }

void overload2(short) {}
void overload2(Foo<int>) {}
void overload2(Foo<float>) {}

}

PYBIND11_MODULE(pybind, m) {
    /* Foo is deliberately not exposed to make it cause a signature parse
       error. The output should then contain multiple overloads but each with
       an ellipsis for params.

       Additionally, math.log is imported and added alongside these from within
       __init__.py. */
    m.def("overload", static_cast<void(*)(short)>(overload))
     .def("overload", static_cast<Foo<int>(*)(int)>(overload))
     .def("overload", static_cast<Foo<float>(*)(float)>(overload))
     .def("overload2", static_cast<void(*)(short)>(overload2))
     .def("overload2", static_cast<void(*)(Foo<int>)>(overload2))
     .def("overload2", static_cast<void(*)(Foo<float>)>(overload2));
}
