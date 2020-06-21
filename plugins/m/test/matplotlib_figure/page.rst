m.matplotlib_figure
###################


.. matplotlib-figure::

    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(-np.pi, np.pi, 1000)

    plt.plot(x, np.sin(x), label='sine', color='black')
    plt.plot(x, x, label='Taylor series, n=1', color='red')
    plt.plot(x, x*(1-x**2/6), label='Taylor series, n=3', color='blue')
    plt.plot(x, x*(1-x**2/6*(1-x**2/20)), label='Taylor series, n=5', color='green')
    plt.ylim(-1.1, 1.1)

    plt.xlabel("x")
    plt.legend()
    plt.grid(color="#CCCCCC", lw=0.2)
    plt.tight_layout()