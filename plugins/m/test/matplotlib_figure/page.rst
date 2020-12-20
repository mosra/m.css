m.matplotlib_figure
###################

Show snippet, produce some output and render matplotlib figure:

.. matplotlib-figure::
    :context-id: figure

    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    x = np.linspace(-np.pi, np.pi, 1000)

    # use pre-defined variable MCSS_MPL_DARK
    plt.style.use(MCSS_MPL_DARK)


    plt.plot(x, np.sin(x),                label='n=∞')
    plt.plot(x, x*(1-x**2/6*(1-x**2/20)), label='n=5')
    plt.plot(x, x*(1-x**2/6),             label='n=3')
    plt.plot(x, x,                        label='n=1')

    plt.ylim(-1.1, 1.1)

    plt.xlabel("time, s")
    plt.ylabel("magnitude, a.u.")
    plt.title("Sine series at x=0")

    plt.grid(color="#CCCCCC", lw=0.2)
    plt.legend()
    plt.tight_layout()

    print("output")
    print("error", file=sys.stderr)

Replot figure without code, destroy context. (all figures are closed & global matplotlib state restored to default)

.. matplotlib-figure::
    :hide-code:
    :context-id: figure
    :discard-context:

    pass

Now we start new anon context with default settings:

.. matplotlib-figure::

    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(-np.pi, np.pi, 100)
    plt.plot(x, np.sin(x), label='sine')