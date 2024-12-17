#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/chrono.h> /* for std::chrono */
#include <pybind11/stl.h> /* needed for std::vector! */
#include <pybind11/functional.h> /* for std::function */

#if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 207
#include <pybind11/stl/filesystem.h> /* for std::filesystem::path */
#endif

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

void dateTime(std::chrono::time_point<std::chrono::system_clock>, std::chrono::nanoseconds) {}

struct MyClass {
    static MyClass staticFunction(int, float) { return {}; }

    std::pair<float, int> instanceFunction(int, const std::string&) { return {0.5f, 42}; }

    int another() { return 42; }

    float foo() const { return _foo; }
    void setFoo(float foo) { _foo = foo; }

    private: float _foo = 0.0f;
};

void defaultUnrepresentableArgument(MyClass) {}

struct Pybind23 {
    void setFoo(float) {}

    void setFooCrazy(const Crazy<3, int>&) {}
};

struct Pybind26 {
    static int positionalOnly(int, float) { return 1; }
    static int keywordOnly(float, const std::string&) { return 2; }
    static int positionalKeywordOnly(int, float, const std::string&) { return 3; }
};

struct Pybind27 {
    #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 207
    /* In https://github.com/pybind/pybind11/commit/5bcaaa0423c6757ca1c2738d0a54947dacdb03a1
       it says that std::filesystem_path gets converted to pathlib.Path (i.e.,
       as a return value?) instead of os.PathLike, but that's not the case,
       both are exposed as os.PathLike */
    static std::filesystem::path path(const std::filesystem::path& path) {
        return path;
    }
    #endif
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
        .def("date_time", &dateTime, "A function taking a datetime.datetime and timedelta")
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
        .def("tenOverloads", &tenOverloads<std::string, std::string>, "Ten overloads of a function")

        .def("full_docstring", &voidFunction, R"(A summary

And a larger docstring as well.)")
        .def("full_docstring_overloaded", &tenOverloads<int, int>, R"(An overload summary

This function takes a value of 2. full_docstring_overloaded(a: float, b: float)
takes just 3 instead.)")
        .def("full_docstring_overloaded", &tenOverloads<float, float>, R"(Another overload summary

This overload, however, takes just a 32-bit (or 64-bit) floating point value of
3. full_docstring_overloaded(a: int, b: int)
takes just 2. There's nothing for 4. full_docstring_overloaded(a: poo, b: foo)
could be another, but it's not added yet.)");

    py::class_<MyClass>(m, "MyClass", "My fun class!")
        .def_static("static_function", &MyClass::staticFunction, "Static method with positional-only args")
        .def(py::init(), "Constructor")
        .def("instance_function", &MyClass::instanceFunction, "Instance method with positional-only args")
        .def("instance_function_kwargs", &MyClass::instanceFunction, "Instance method with position or keyword args", py::arg("hey"), py::arg("what") = "<eh?>")
        .def("another", &MyClass::another, "Instance method with no args, 'self' is thus position-only")
        .def_property("foo", &MyClass::foo, &MyClass::setFoo, "A read/write property")
        .def_property_readonly("bar", &MyClass::foo, "A read-only property");

    /* Has to be done only after the MyClass is defined */
    m.def("default_unrepresentable_argument", &defaultUnrepresentableArgument, "A function with an unrepresentable default argument", py::arg("a") = MyClass{});

    m.def_submodule("just_overloads", "Stubs for this module should import typing as well")
        .def("overloaded", static_cast<std::string(*)(int)>(&overloaded), "Overloaded for ints")
        .def("overloaded", static_cast<bool(*)(float)>(&overloaded), "Overloaded for floats");

    py::class_<Pybind23> pybind23{m, "Pybind23", "Testing pybind 2.3 features"};

    /* Checker so the Python side can detect if testing pybind 2.3+ features is
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
        .def_property("writeonly", nullptr, &Pybind23::setFoo, "A write-only property")
        .def_property("writeonly_crazy", nullptr, &Pybind23::setFooCrazy, "A write-only property with a type that can't be parsed");
    #endif

    py::class_<Pybind26> pybind26{m, "Pybind26", "Testing pybind 2.6 features"};

    /* Checker so the Python side can detect if testing pybind 2.6+ features is
       feasible */
    pybind26.attr("is_pybind26") =
        #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 206
        true
        #else
        false
        #endif
        ;

    #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 206
    pybind26
        .def_static("positional_only", &Pybind26::positionalOnly, "Positional-only arguments", py::arg("a"), py::pos_only{}, py::arg("b"))
        .def_static("keyword_only", &Pybind26::keywordOnly, "Keyword-only arguments", py::arg("b"), py::kw_only{}, py::arg("keyword") = "no")
        .def_static("positional_keyword_only", &Pybind26::positionalKeywordOnly, "Positional and keyword-only arguments", py::arg("a"), py::pos_only{}, py::arg("b"), py::kw_only{}, py::arg("keyword") = "no");
    #endif

    py::class_<Pybind27> pybind27{m, "Pybind27", "Testing pybind 2.7 features"};

    /* Checker so the Python side can detect if testing pybind 2.7+ features is
       feasible */
    pybind27.attr("is_pybind27") =
        #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 207
        true
        #else
        false
        #endif
        ;

    #if PYBIND11_VERSION_MAJOR*100 + PYBIND11_VERSION_MINOR >= 207
    pybind27
        .def_static("path", &Pybind27::path, "Take and return a std::filesystem::path");
    #endif
}
