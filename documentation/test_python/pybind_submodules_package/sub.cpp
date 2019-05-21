#include <pybind11/pybind11.h>

PYBIND11_MODULE(sub, m) {
    m.doc() = "pybind11 submodule of a Python package";

    m.def_submodule("subsub", "Yay a submodule");
    m.def_submodule("another", "Yay another");
}
