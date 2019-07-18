#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace {

void manyParameters(std::tuple<int, float, std::string, std::vector<std::pair<int, int>>> a, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>> b, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>> c) {}

}

PYBIND11_MODULE(search_long_suffix_length, m) {
    m.def("many_parameters", &manyParameters);
}
