#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
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

from docutils.parsers import rst
from docutils.parsers.rst import directives

module_doc_output = None
class_doc_output = None
enum_doc_output = None
function_doc_output = None
property_doc_output = None
data_doc_output = None

class PyModule(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged}

    def run(self):
        module_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'content': '\n'.join(self.content)
        }
        return []

class PyClass(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged}

    def run(self):
        class_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'content': '\n'.join(self.content)
        }
        return []

class PyEnum(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged}

    def run(self):
        enum_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'content': '\n'.join(self.content)
        }
        return []

# List option (allowing multiple arguments). See _docutils_assemble_option_dict
# in python.py for details.
def directives_unchanged_list(argument):
    return [directives.unchanged(argument)]

class PyFunction(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged,
                   'param': directives_unchanged_list,
                   'return': directives.unchanged}

    def run(self):
        # Check that params are parsed properly, turn them into a dict. This
        # will blow up if the param name is not specified.
        params = {}
        for name, content in self.options.get('param', []):
            if name in params: raise KeyError(f"duplicate param {name}")
            params[name] = content

        function_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'params': params,
            'return': self.options.get('return'),
            'content': '\n'.join(self.content)
        }
        return []

class PyProperty(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged}

    def run(self):
        property_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'content': '\n'.join(self.content)
        }
        return []

class PyData(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1
    option_spec = {'summary': directives.unchanged}

    def run(self):
        data_doc_output[self.arguments[0]] = {
            'summary': self.options.get('summary', ''),
            'content': '\n'.join(self.content)
        }
        return []

def register_mcss(module_doc_contents, class_doc_contents, enum_doc_contents, function_doc_contents, property_doc_contents, data_doc_contents, **kwargs):
    global module_doc_output, class_doc_output, enum_doc_output, function_doc_output, property_doc_output, data_doc_output
    module_doc_output = module_doc_contents
    class_doc_output = class_doc_contents
    enum_doc_output = enum_doc_contents
    function_doc_output = function_doc_contents
    property_doc_output = property_doc_contents
    data_doc_output = data_doc_contents

    rst.directives.register_directive('py:module', PyModule)
    rst.directives.register_directive('py:class', PyClass)
    rst.directives.register_directive('py:enum', PyEnum)
    rst.directives.register_directive('py:function', PyFunction)
    rst.directives.register_directive('py:property', PyProperty)
    rst.directives.register_directive('py:data', PyData)

def register(): # for Pelican
    assert not "This plugin is for the m.css Doc theme only" # pragma: no cover
