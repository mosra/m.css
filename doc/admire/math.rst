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

m.css math
##########

.. role:: em-strong(strong)
    :class: m-text m-em
.. role:: text-primary
    :class: m-text m-primary

:url: admire/math/
:cover: {filename}/static/cover-math.jpg
:summary: The fastest possible math rendering for the modern web
:footer:
    .. note-dim::

        *Wondering what m.css is all about?* Visit the `main page <{filename}/index.rst>`_
        to see what else it can offer to you.
:landing:
    .. container:: m-row

        .. container:: m-col-l-6 m-push-l-1 m-col-m-7 m-nopadb

            .. raw:: html

                <h1><span class="m-thin">m.css</span> math</h1>

    .. container:: m-row

        .. container:: m-col-l-6 m-push-l-1 m-col-m-7 m-nopadt

            *The* :em-strong:`fastest possible` *math rendering for the modern web.*

            With latest advancements in web tech, the browser should no longer
            *struggle* to render math. Yet it still does. Why *jump around*
            several times until the math settles down? Why *stutter* for
            *seconds* in a heavy JavaScript renderer from a third-party CDN
            that gets shut down every once a while? Why *saturate* the network
            with extra requests for every small snippet? You don't need
            *any of that*.

        .. container:: m-col-l-3 m-push-l-2 m-col-m-4 m-push-m-1 m-col-s-6 m-push-s-3 m-col-t-8 m-push-t-2

            .. button-primary:: #demo
                :class: m-fullwidth

                See the demo

                | don't worry,
                | it's already loaded

    .. container:: m-row

        .. container:: m-col-m-12

            .. https://en.wikipedia.org/wiki/Rendering_equation

            .. math::

                L_o(p,\omega_o) = \int\limits_{\Omega} f_r(p,\omega_i,\omega_o) L_i(p,\omega_i) n \cdot \omega_i d\omega_i

.. container:: m-row m-container-inflate

    .. container:: m-col-m-4

        .. block-warning:: *Self-contained* inline SVG

            Embed math directly in HTML5 markup as pure paths, cutting away all
            external dependencies or extra fonts. And having the SVG inline
            means you can make use of all the CSS goodies on it.

            .. button-warning:: {filename}/css/components.rst#math
                :class: m-fullwidth

                See the possibilites

    .. container:: m-col-m-4

        .. block-success:: *Fastest possible* rendering

            As you unleash the full power of a static site generator to convert
            LaTeX formulas to vector graphics locally, your viewers are saved
            from needless HTTP requests and heavy JavaScript processing.

            .. button-success:: {filename}/pelican.rst
                :class: m-fullwidth

                Start using Pelican

    .. container:: m-col-m-4

        .. block-info:: You are *completely* in charge

            Since the math is rendered by your local TeX installation, you have
            the full control over its appearance and you can be sure that it
            will also render the same on all browsers. Now or two years later.

            .. button-info:: {filename}/plugins/math-and-code.rst#math
                :class: m-fullwidth

                Get the Pelican plugin

.. _demo:

Demo time!
==========

Be sure to refresh your browser a couple of times to see how the rendering
performs and that there is no blank space or jumping until the math appears.
View the page source to verify that there is nothing extra being loaded to make
this happen.

    .. math::

        \pi = \cfrac{4} {1+\cfrac{1^2} {2+\cfrac{3^2} {2+\cfrac{5^2} {2+\ddots}}}}
            = \sum_{n=0}^\infty \frac{4(-1)^n}{2n+1}
            = \frac{4}{1} - \frac{4}{3} + \frac{4}{5} - \frac{4}{7} +- \cdots

    .. class:: m-text m-text-right m-dim m-em

    --- `Generalized continued fraction <https://en.wikipedia.org/wiki/Generalized_continued_fraction#.CF.80>`_,
    Wikipedia

Matrices render pretty well also:

    .. math::

        R = \begin{pmatrix}
        \langle\mathbf{e}_1,\mathbf{a}_1\rangle & \langle\mathbf{e}_1,\mathbf{a}_2\rangle &  \langle\mathbf{e}_1,\mathbf{a}_3\rangle  & \ldots \\
        0                & \langle\mathbf{e}_2,\mathbf{a}_2\rangle                        &  \langle\mathbf{e}_2,\mathbf{a}_3\rangle  & \ldots \\
        0                & 0                                       & \langle\mathbf{e}_3,\mathbf{a}_3\rangle                          & \ldots \\
        \vdots           & \vdots                                  & \vdots                                    & \ddots \end{pmatrix}.

    .. class:: m-text m-text-right m-dim m-em

    --- `QR decomposition <https://en.wikipedia.org/wiki/QR_decomposition>`_,
    Wikipedia

And :text-primary:`everything can be colored` just by putting CSS classes
around:

    .. math::
        :class: m-primary

        X_{k+N} \ \stackrel{\mathrm{def}}{=} \ \sum_{n=0}^{N-1} x_n e^{-\frac{2\pi i}{N} (k+N) n} = \sum_{n=0}^{N-1} x_n e^{-\frac{2\pi i}{N} k n}  \underbrace{e^{-2 \pi i n}}_{1} = \sum_{n=0}^{N-1} x_n e^{-\frac{2\pi i}{N} k n} = X_k.

    .. class:: m-text m-text-right m-dim m-em

    --- `Discrete Fourier transform § Periodicity <https://en.wikipedia.org/wiki/Discrete_Fourier_transform#Periodicity>`_, Wikipedia

And now, finally, some inline math. Note the vertical alignment, consistent
line spacing and that nothing gets relayouted during page load:

    Multiplying :math:`x_n` by a *linear phase* :math:`e^{\frac{2\pi i}{N}n m}`
    for some integer :math:`m` corresponds to a *circular shift* of the output
    :math:`X_k`: :math:`X_k` is replaced by :math:`X_{k-m}`, where the
    subscript is interpreted `modulo <https://en.wikipedia.org/wiki/Modular_arithmetic>`_
    :math:`N` (i.e., periodically).  Similarly, a circular shift of the input
    :math:`x_n` corresponds to multiplying the output :math:`X_k` by a linear
    phase. Mathematically, if :math:`\{x_n\}` represents the vector
    :math:`\boldsymbol{x}` then

    if :math:`\mathcal{F}(\{x_n\})_k=X_k`

    then :math:`\mathcal{F}(\{ x_n\cdot e^{\frac{2\pi i}{N}n m} \})_k=X_{k-m}`

    and :math:`\mathcal{F}(\{x_{n-m}\})_k=X_k\cdot e^{-\frac{2\pi i}{N}k m}`

    .. class:: m-text m-text-right m-dim m-em

    ---  `Discrete Fourier transform § Shift theorem <https://en.wikipedia.org/wiki/Discrete_Fourier_transform#Shift_theorem>`_, Wikipedia
