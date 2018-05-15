..
    This file is part of m.css.

    Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>

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

:save_as: plugins/plots/test/index.html
:breadcrumb: {filename}/plugins.rst Pelican plugins
             {filename}/plugins/plots.rst Plots

.. container:: m-row

    .. container:: m-col-m-6

        .. plot:: Fastest animals
            :type: barh
            :labels:
                Cheetah
                Pronghorn
            :units: km/h
            :values: 109.4 88.5
            :colors: warning primary
            :errors: 14.32 5.5

    .. container:: m-col-m-6

        .. plot:: Fastest animals
            :type: barh
            :labels:
                Cheetah
                Pronghorn
                Springbok
                Wildebeest
            :units: km/h
            :values: 109.4 88.5 88 80.5
            :colors: warning primary danger info
