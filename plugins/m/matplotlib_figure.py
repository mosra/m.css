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

from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils import nodes

from m.py_exec import PyCodeExec

MCSS_MPL_DARK = os.path.join(os.path.dirname(__file__), "mcss-dark.mplstyle")


class MatplotlibFigure(PyCodeExec):
    input_root = './'  # initialized by configure_pelican() defined below

    def run_before_snippet(self, gl):
        import matplotlib
        matplotlib.use('agg')
        gl['MCSS_MPL_DARK'] = MCSS_MPL_DARK

    def run(self):
        code_figure = super().run()
        if code_figure:
            code_figure = code_figure[0]
        else:
            code_figure = nodes.container('', classes=['m-code-figure'])

        image_reference = rst.directives.uri(self.image_uri)
        image_node = nodes.image('', uri=image_reference)
        div = nodes.container('', classes=['m-py-exec'])
        div.append(image_node)
        code_figure.append(div)
        return [code_figure]

    def run_after_snippet(self, gl):
        import matplotlib.pyplot as plt

        source_filename = self.state.document.current_source
        source_to_root = os.path.relpath(source_filename, self.input_root)

        output_img_filename = os.path.join(self.input_root, "matplotlib-figures", source_to_root,
                                           "line-{:02d}.svg".format(self.lineno))
        os.makedirs(os.path.dirname(output_img_filename), exist_ok=True)

        # store relative path
        # TODO: need a reliably way to find resulting .html path, now it's assumed to be output root
        self.image_uri = os.path.relpath(output_img_filename, self.input_root)
        # self.image_uri = os.path.relpath(output_img_filename, os.path.dirname(source_filename))

        # render current figure
        # TODO: is there need to choose which figure(s) to render?
        plt.savefig(output_img_filename)

        # clean-up: reset possibly altered matplotlib state & close all figures
        if 'context-id' not in self.options or 'discard-context' in self.options:
            plt.close('all')
            plt.style.use('default')


def register_mcss(mcss_settings, **kwargs):
    MatplotlibFigure.input_root = os.path.abspath(mcss_settings['INPUT'])
    rst.directives.register_directive('matplotlib-figure', MatplotlibFigure)


# Below is only Pelican-specific functionality. If Pelican is not found, these
# do nothing.

def _configure_pelican(pelicanobj):
    settings = {
        'INPUT': pelicanobj.settings['PATH'],
    }
    register_mcss(mcss_settings=settings)


def register():
    import pelican.signals
    pelican.signals.initialized.connect(_configure_pelican)
