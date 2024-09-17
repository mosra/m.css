#include <pybind11/pybind11.h>

namespace py = pybind11;

int defaultValueShouldBeEscaped(const char*) { return 0; }

PYBIND11_MODULE(pybind, m) {
    m.doc() = "pybind11 html escaping";

    m.def("default_value_should_be_escaped", defaultValueShouldBeEscaped, py::arg("string") = "<&>");
}
