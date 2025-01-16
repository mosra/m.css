..
    This file is part of m.css.

    Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
              Vladimír Vondruš <mosra@centrum.cz>

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
:breadcrumb: {filename}/plugins.rst Plugins
             {filename}/plugins/math-and-code.rst Math and code

.. role:: math-default(math)
    :class: m-default
.. role:: math-primary(math)
    :class: m-primary
.. role:: math-success(math)
    :class: m-success
.. role:: math-warning(math)
    :class: m-warning
.. role:: math-danger(math)
    :class: m-danger
.. role:: math-info(math)
    :class: m-info
.. role:: math-dim(math)
    :class: m-dim

.. role:: code-math(code)
    :class: m-math
.. role:: code-math-default(code)
    :class: m-math m-default
.. role:: code-math-primary(code)
    :class: m-math m-primary
.. role:: code-math-success(code)
    :class: m-math m-success
.. role:: code-math-warning(code)
    :class: m-math m-warning
.. role:: code-math-danger(code)
    :class: m-math m-danger
.. role:: code-math-info(code)
    :class: m-math m-info
.. role:: code-math-dim(code)
    :class: m-math m-dim

Math
====

First is colored except :math:`c^2`, second is colored globally, third is
colored globally with overrides except for :math:`c^2`. Second row in each is
the same but inline instead of a block.

.. container:: m-row

    .. container:: m-col-m-4

        .. math::

            {\color{m-default} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-default} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-default

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-default:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-default} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-default} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::

            {\color{m-primary} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-primary} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-primary

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-primary:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-primary} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-primary} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::

            {\color{m-success} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-success} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-success

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-success:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-success} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-success} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::

            {\color{m-warning} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-warning} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-warning

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-warning:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-warning} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-warning} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::

            {\color{m-danger} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-danger} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-danger:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-success

            {\color{m-danger} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-success:`{\color{m-danger} a^2 + b^2 =} ~ c^2`

.. container:: m-row

    .. container:: m-col-m-4

        .. math::

            {\color{m-info} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-info} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-info

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-info:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-info} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-info} a^2 + b^2 =} ~ c^2`

.. container:: m-row

    .. container:: m-col-m-4

        .. math::

            {\color{m-dim} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math:`{\color{m-dim} a^2 + b^2 =} ~ c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-dim

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :math-dim:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. math::
            :class: m-danger

            {\color{m-dim} a^2 + b^2 =} ~ c^2

        .. class:: m-text-center m-noindent

        :math-danger:`{\color{m-dim} a^2 + b^2 =} ~ c^2`

Math as code
------------

Block and inline math, same as above. Since the ``M_MATH_RENDER_AS_CODE``
option is global, here it's faked with code blocks that have classes applied.

.. container:: m-row

    .. container:: m-col-m-4

        .. code::
            :class: m-math

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. code::
            :class: m-math m-default

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-default:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. code::
            :class: m-math m-primary

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-primary:`a^2 + b^2 = c^2`

.. container:: m-row

    .. container:: m-col-m-4

        .. code::
            :class: m-math m-success

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-success:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. code::
            :class: m-math m-warning

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-warning:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4

        .. code::
            :class: m-math m-danger

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-danger:`a^2 + b^2 = c^2`

.. container:: m-row

    .. container:: m-col-m-4 m-push-m-2

        .. code::
            :class: m-math m-info

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-info:`a^2 + b^2 = c^2`

    .. container:: m-col-m-4 m-push-m-2

        .. code::
            :class: m-math m-dim

            a^2 + b^2 = c^2

        .. class:: m-text-center m-noindent

        :code-math-dim:`a^2 + b^2 = c^2`
