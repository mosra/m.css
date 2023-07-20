#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023
#             Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

cmake_minimum_required(VERSION 3.5)
project(McssDocumentationPybindTests)

find_package(pybind11 CONFIG REQUIRED)

foreach(target pybind_signatures pybind_enums pybind_external_overload_docs pybind_submodules pybind_type_links search_long_suffix_length)
    pybind11_add_module(${target} ${target}/${target}.cpp)
    set_target_properties(${target} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${target})
endforeach()

# Need a special location for this one
pybind11_add_module(pybind_inspect_create_intersphinx inspect_create_intersphinx/inspect_create_intersphinx/pybind.cpp)
set_target_properties(pybind_inspect_create_intersphinx PROPERTIES
    OUTPUT_NAME pybind
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/inspect_create_intersphinx/inspect_create_intersphinx)

# Need a special location for this one
pybind11_add_module(pybind_link_formatting link_formatting/link_formatting/pybind.cpp)
set_target_properties(pybind_link_formatting PROPERTIES
    OUTPUT_NAME pybind
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/link_formatting/link_formatting)

# Need a special location for this one
pybind11_add_module(pybind_search search/search/pybind.cpp)
set_target_properties(pybind_search PROPERTIES
    OUTPUT_NAME pybind
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/search/search)

# Need a special name for this one
pybind11_add_module(pybind_name_mapping pybind_name_mapping/sub.cpp)
set_target_properties(pybind_name_mapping PROPERTIES
    OUTPUT_NAME _sub
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/pybind_name_mapping/pybind_name_mapping)

# Need a special name for this one
pybind11_add_module(pybind_submodules_package pybind_submodules_package/sub.cpp)
set_target_properties(pybind_submodules_package PROPERTIES
    OUTPUT_NAME sub
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/pybind_submodules_package/pybind_submodules_package)
