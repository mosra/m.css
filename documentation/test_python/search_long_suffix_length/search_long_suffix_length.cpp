#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace {

void manyParameters1(std::tuple<float, int, std::string, std::vector<std::pair<int, int>>>, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>>, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>>) {}
void manyParameters2(std::tuple<int, float, std::string, std::vector<std::pair<int, int>>>, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>>, std::tuple<int, float, std::string, std::vector<std::pair<int, int>>>) {}

}

PYBIND11_MODULE(search_long_suffix_length, m) {
    m.def("many_parameters", &manyParameters1)
     .def("many_parameters", &manyParameters2);
}
