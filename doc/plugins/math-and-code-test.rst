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
