Contributing guide
##################

Bug reports, feature requests or code contributions are always very welcome.
To make things easier, here are a few tips:

Reporting bugs, requesting features
===================================

-   Best way to report bugs and request new features is to use GitHub
    `issues <https://github.com/mosra/m.css/issues>`_, but you can contact me
    also any other way.

Code contribution
=================

-   Setting up and using m.css for your own project is described in the
    `documentation <http://mcss.mosra.cz/>`_.
-   Documentation and the website is essential part of the project and every
    larger Pelican theme, plugin code or CSS contribution should be reflected
    there. The website is contained inside `site/ <site>`_ subdirectory and you
    can build and start a local version of it using Pelican by executing
    ``make devserver`` in there. The website is then available at
    http://localhost:8000. See `Pelican usage documentation <http://mcss.mosra.cz/pelican/>`_
    for more information.
-   Documentation and website content is written in reStructuredText and
    resides in `doc/ <doc>`_ subdirectory. Please verify that all your changes
    there do not break the website build.
-   Best way to contribute is by using GitHub `pull requests <https://github.com/mosra/m.css/pulls>`_
    --- fork the repository and make pull request from feature branch. You can
    also send patches via e-mail or contact me any other way.
-   All your code will be released under license of the project (see `COPYING <COPYING>`_
    file for details), so make sure you and your collaborators (or employers)
    have no problems with it. If you create new files, don't forget to add
    license header (verbatim copied from other files) and don't forget to add
    yourself to license header of files you added or significantly modified
    (including documentation pages), for example::

        /*
            This file is part of m.css.

            Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>
            Copyright © YEAR YOUR_NAME <your@mail.com>

            Permission is hereby granted, free of charge, to any person obtaining a
            ...

Contact
=======

-   Website --- http://mcss.mosra.cz
-   GitHub --- https://github.com/mosra/m.css
-   Gitter --- https://gitter.im/mosra/m.css
-   Twitter --- https://twitter.com/czmosra
-   E-mail --- mosra@centrum.cz
-   Jabber --- mosra@jabbim.cz
