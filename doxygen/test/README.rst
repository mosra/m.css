Doxygen generator testing and code coverage
###########################################

Run tests:

.. code:: sh

    cd doxygen
    python -m unittest

Code coverage needs `coverage.py <https://coverage.readthedocs.io/>`_:

.. code:: sh

    cd doxygen
    coverage run -m unittest -v ; coverage html
    # open htmlcov/index.html in your browser

Files named ``test_something.py`` take their input from  ``something[_name]``
directories, ``name`` corresponds to given test class. Comment-out the line
that removes the ``html`` directory in ``__init__.py`` to see all test output
files.
