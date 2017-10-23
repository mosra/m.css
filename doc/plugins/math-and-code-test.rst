..
    This file is part of m.css.

    Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
..

Test
####

:save_as: plugins/math-and-code/test/index.html
:breadcrumb: {filename}/plugins.rst Pelican plugins
             {filename}/plugins/math-and-code.rst Math and code

.. role:: tex(code)
    :language: latex

Properly align *huge* formulas vertically on a line: :math:`\hat q^{-1} = \frac{\hat q^*}{|\hat q|^2}`
and make sure there's enough space for all the complex :math:`W` things between
the lines :math:`W = \sum_{i=0}^{n} \frac{w_i}{h_i}` because  :math:`Y = \sum_{i=0}^{n} B`

The :tex:`\\cfrac` thing doesn't align well: :math:`W = \sum_{i=0}^{n} \cfrac{w_i}{h_i}`

Huh, apparently backslashes have to be escaped in things like this:
:tex:`\frac`
