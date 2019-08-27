#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> /* needed for std::vector! */
#include <pybind11/functional.h> /* for std::function */

namespace py = pybind11;

int scale(int a, float argument) {
    return int(a*argument);
}

void voidFunction(int) {}

std::tuple<int, int, int> takingAListReturningATuple(const std::vector<float>&) {
    return {};
}

template<std::size_t, class> struct Crazy {};

void crazySignature(const Crazy<3, int>&) {}

std::string overloaded(int) { return {}; }
bool overloaded(float) { return {}; }

// Doesn't work with just a plain function pointer, MEH
void takesAFunction(std::function<int(float, std::vector<float>&)>) {}
void takesAFunctionReturningVoid(std::function<void()>) {}

struct MyClass {
    static MyClass staticFunction(int, float) { return {}; }

    std::pair<float, int> instanceFunction(int, const std::string&) { return {0.5f, 42}; }

    int another() { return 42; }

    float foo() const { return _foo; }
    void setFoo(float foo) { _foo = foo; }

    private: float _foo = 0.0f;
};

struct MyClass23 {
    void setFoo(float) {}

    void setFooCrazy(const Crazy<3, int>&) {}
};

void duck(py::args, py::kwargs) {}

template<class T, class U> void tenOverloads(T, U) {}

PYBIND11_MODULE(pybind_signatures, m) {
    m.doc() = "pybind11 function signature extraction";

    m
        .def("scale", &scale, "Scale an integer")
        .def("scale_kwargs", &scale, "Scale an integer, kwargs", py::arg("a"), py::arg("argument"))
        .def("void_function", &voidFunction, "Returns nothing")
        .def("taking_a_list_returning_a_tuple", &takingAListReturningATuple, "Takes a list, returns a tuple")
        .def("crazy_signature", &crazySignature, "Function that failed to get parsed")
        .def("overloaded", static_cast<std::string(*)(int)>(&overloaded), "Overloaded for ints")
        .def("overloaded", static_cast<bool(*)(float)>(&overloaded), "Overloaded for floats")
        .def("duck", &duck, "A function taking args/kwargs directly")
        .def("takes_a_function", &takesAFunction, "A function taking a Callable")
        .def("takes_a_function_returning_none", &takesAFunctionReturningVoid, "A function taking a Callable that returns None")
        .def("escape_docstring", &voidFunction, "A docstring that <em>should</em> be escaped")
        .def("failed_parse_docstring", &crazySignature, "A failed parse should <strong>also</strong> escape the docstring")

        .def("tenOverloads", &tenOverloads<float, float>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<int, float>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<bool, float>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<float, int>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<int, int>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<bool, int>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<float, bool>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<int, bool>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<bool, bool>, "Ten overloads of a function")
        .def("tenOverloads", &tenOverloads<std::string, std::string>, "Ten overloads of a function");

    py::class_<MyClass>(m, "MyClass", "My fun class!")
        .def_static("static_function", &MyClass::staticFunction, "Static method with positional-only args")
        .def(py::init(), "Constructor")
        .def("instance_function", &MyClass::instanceFunction, "Instance method with positional-only args")
        .def("instance_function_kwargs", &MyClass::instanceFunction, "Instance method with position or keyword args", py::arg("hey"), py::arg("what") = "<eh?>")
        .def("another", &MyClass::another, "Instance method with no args, 'self' is thus position-only")
        .def_property("foo", &MyClass::foo, &MyClass::setFoo, "A read/write property")
        .def_property_readonly("bar", &MyClass::foo, "A read-only property");

    py::class_<MyClass23> pybind23{m, "MyClass23", "Testing pybind 2.3 features"};

    /* Checker so the Python side can detect if testing pybind 2.3 features is
       feasible */
    pybind23.attr("is_pybind23") =
        #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 203
        true
        #else
        false
        #endif
        ;

    #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 203
    pybind23
        .def_property("writeonly", nullptr, &MyClass23::setFoo, "A write-only property")
        .def_property("writeonly_crazy", nullptr, &MyClass23::setFooCrazy, "A write-only property with a type that can't be parsed");
    #endif
}
