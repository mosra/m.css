set -e

wget --no-clobber https://github.com/pybind/pybind11/archive/v$PYBIND_VERSION.tar.gz && tar -xzf v$PYBIND_VERSION.tar.gz

cd pybind11-$PYBIND_VERSION
mkdir -p build && cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=$HOME/pybind$PYBIND_VERSION \
    -DPYBIND11_PYTHON_VERSION=$TRAVIS_PYTHON_VERSION \
    -DPYBIND11_TEST=OFF \
    -G Ninja
ninja install
