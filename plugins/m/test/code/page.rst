m.code
######

.. role:: cpp(code)
    :language: c++
.. role:: tex(code)
    :language: tex
.. role:: rst(code)
    :language: rst

.. code:: c++

    int main() {
        return 0;
    }

.. code:: c++
    :class: m-inverted
    :hl_lines: 2

    int main() {
        return 1;
    }

Inline code is here: :cpp:`constexpr`. Code without a language should be
rendered as plain monospace text: :code:`code`.

.. include:: console.ansi
    :code: ansi

Console colors:

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
