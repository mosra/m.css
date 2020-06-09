m.plots
#######

Note: the test uses DejaVu Sans instead of Source Sans Pro in order to have
predictable rendering on the CIs.

.. raw:: html

    <style>
    div.m-plot svg { font-family: DejaVu Sans; }
    </style>

.. plot:: A plot with a single color
    :type: barh
    :labels:
        First
        Second
    :units: meters, i guess?
    :values: 15 30
    :colors: success

.. using legacy underscored options below to test the compatibility (the dashed
    options are used on the site, which should be enough to verify those work)

.. container:: m-col-m-6 m-center-m

    A plot with separate colors, extra labels, error bars and custom width + height

    .. plot:: Yes.
        :type: barh
        :labels:
            January
            February
            March
        :labels_extra:
            a paradise
            ..
            hell!
        :units: Mondays
        :values: 3 4 5
        :errors: 0.1 2.1 1.0
        :colors: success info danger
        :plot-width: 4.5
        :bar_height: 0.75

.. plot:: Stacked plot
    :type: barh
    :labels:
        A
        B
        C
    :units: kB
    :values:
        111.9 74.4 52.1
        731.2 226.3 226.0
    :colors:
        success
        info

.. plot:: Stacked plot with errors and full colors
    :type: barh
    :labels:
        A
        B
    :units: kB
    :values:
        111.9 74.4
        731.2 226.3
    :errors:
        25.0 15.3
        200.0 5.0
    :colors:
        success danger
        info primary
