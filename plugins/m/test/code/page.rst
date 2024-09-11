m.code
######

.. role:: ansi(code)
    :language: ansi
.. role:: cpp(code)
    :language: c++
.. role:: tex(code)
    :language: tex
.. role:: rst(code)
    :language: rst
.. role:: py(code)
    :language: py

.. code:: c++

    int main() {
        return 0;
    }

.. code:: c++
    :class: m-inverted
    :hl-lines: 2

    int main() {
        return 1;
    }

Legacy :rst:`:hl_lines:` option should work the same:

.. code:: c++
    :class: m-inverted
    :hl_lines: 2

    int main() {
        return 1;
    }

Same as above, but for a :rst:`.. include::`, which should also support line
highlighting:

.. include:: code.cpp
    :code: c++
    :class: m-inverted
    :hl-lines: 2

Inline code is here: :cpp:`constexpr`. Code without a language should be
rendered as plain monospace text: :code:`code`.

.. include:: console.ansi
    :code: ansi

Syntax highlighting:

.. code:: py

    # Comment
    var = "string{}escape\n"

Console colors, including :ansi:`[31minline` code:

.. include:: console-colors.ansi
    :code: ansi

.. code:: whatthefuck

    // this language is not highlighted

Properly preserve backslashes: :tex:`\frac{a}{b}` ... and backticks:
:rst:`:ref:`a function <os.path.join()>``

Don't trim leading spaces in blocks:

.. code:: c++

            nope();
        return false;
    }

`Advanced file inclusion`_
==========================

.. include:: file.py
    :start-after: """
    :end-before: """

.. the following tests :start-on:, empty :end-before: and :strip-prefix: also:

.. include:: file.py
    :start-on: # This is a reST
    :end-before:
    :strip-prefix: '# '

.. include:: file.py
    :start-after: # [yay-code]
    :end-before: # [/yay-code]
    :strip-prefix: '    '
    :code: py

In comparison, here's the default output without :rst:`:strip-prefix:`:

.. include:: file.py
    :start-after: # [yay-code]
    :end-before: # [/yay-code]
    :code: py

`Filters`_
==========

.. role:: css(code)
    :language: css

Applied by default, adding typographically correct spaces before and a color
swatch after --- and for inline as well: :css:`p{ color:#ff3366; }`

.. code:: css

    p{
        color:#ff3366;
    }

.. role:: css-filtered(code)
    :language: css
    :filters: lowercase replace_colors

Applied explicitly and then by default --- and for inline as well:
:css-filtered:`P{ COLOR:#C0FFEE; }`

.. code:: css
    :filters: lowercase replace_colors

    P{
        COLOR:#C0FFEE;
    }

Includes too:

.. include:: style.css
    :code: css
    :filters: lowercase replace_colors
