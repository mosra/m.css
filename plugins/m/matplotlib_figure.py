#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
#   Copyright © 2020 Sergei Izmailov <sergei.a.izmailov@gmail.com>
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

import os
import shutil
import io
import traceback

from contextlib import redirect_stdout, redirect_stderr
from docutils.parsers import rst
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive, directives
from docutils import nodes
from typing import List, Dict
from hashlib import sha1

from m.py_exec import PyCodeExec


class MatplotlibFigure(PyCodeExec):
    output_path = './'  # initialized by configure_pelican() below

    def run_before_snippet(self, gl):
        import matplotlib
        matplotlib.use('agg')

    # TODO: move this run function to abstract base class (e.g. PythonFigure) to produce
    #       consistent image styling across different image providers
    def run(self):
        # TODO: render figures & code nicely, now it's just two adjacent nodes with no styling
        container = nodes.figure('')
        for el in super().run():
            container.append(el)

        image_reference = rst.directives.uri(self.image_uri)
        image_node = nodes.image('', uri=image_reference)
        container.append(image_node)
        return [container]

    def run_after_snippet(self, gl):
        import matplotlib.pyplot as plt

        source_filename = self.state.document.current_source
        # TODO: replace hash with relative path to source .rst to produce better names
        source_filename_hash = sha1(source_filename.encode('utf-8')).hexdigest()

        rel_out_path = os.path.join("matplotlib-figures", source_filename_hash)
        os.makedirs(os.path.join(self.output_path, rel_out_path), exist_ok=True)

        self.image_uri = os.path.join(rel_out_path, "line-{:02d}.svg".format(self.lineno))

        # TODO: is there need to choose which figure to render?
        plt.savefig(os.path.join(self.output_path, self.image_uri))


def register_mcss(**kwargs):
    rst.directives.register_directive('matplotlib-figure', MatplotlibFigure)


# Below is only Pelican-specific functionality. If Pelican is not found, these
# do nothing.

def configure_pelican(pelicanobj):
    MatplotlibFigure.output_path = os.path.join(pelicanobj.output_path)


def register():
    import pelican.signals
    pelican.signals.initialized.connect(configure_pelican)
    register_mcss()
