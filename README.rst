m.css
#####

*A no-nonsense, no-JavaScript CSS framework and Pelican theme for
content-oriented websites.*

.. image:: https://badges.gitter.im/mosra/m.css.svg
   :alt: Join the chat at https://gitter.im/mosra/m.css
   :target: https://gitter.im/mosra/m.css?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Do you *hate* contemporary web development like I do? Do you also feel that
it's not right for a web page to take *seconds* and *megabytes* to render? Do
you want to write beautiful content but *can't* because the usual CMS tools
make your blood boil and so you rather stay silent? Well, I have something for
you.

Project website: http://mcss.mosra.cz

Pure CSS and HTML
=================

Everything you need is a few kilobytes of compressed CSS. This framework has
exactly 0 bytes of JavaScript because *nobody actually needs it*. Even for
responsive websites.

`Get the CSS <http://mcss.mosra.cz/css/>`_

Designed for content
====================

If you just want to write content with beautiful typography, you don't need
forms, progressbars, popups, dropdowns or other cruft. You want fast iteration
times.

`Use it with Pelican <http://mcss.mosra.cz/pelican/>`_

Authoring made easy
===================

Code snippets, math, linking to docs, presenting photography in a beautiful
way? Or making a complex page without even needing to touch HTML? Everything is
possible.

`Get Pelican plugins <http://mcss.mosra.cz/plugins/>`_

-------

*Still not convinced?* Head over to a `detailed explanation <http://mcss.mosra.cz/why/>`_
of this project goals and design decisions.

BUILDING THE SITE
=================

**Note:** this is about building the m.css website itself, *not* about using
m.css in your project. Check `the website <http://mcss.mosra.cz>`_ for end-user
docs instead.*

The m.css website makes use of all the m.css features, which means that it also
needs all the possible dependencies, combined. Sorry in advance :)

On ArchLinux:

.. code:: sh

    pacman -S texlive-most pelican python-pillow
    cower -d python-pyphen # Build the python-pyphen package from AUR

On Ubuntu you need these:

.. code:: sh

    sudo apt-get install texlive-base texlive-latex-extra texlive-fonts-extra
    pip install pelican Pyphen Pillow

Once you have all the dependencies, simply go to the ``site/`` subdirectory and
start development server there. The live-reloading website will appear on
http://localhost:8000.

.. code:: sh

    cd site
    make devserver

Publishing the website with ``make publish`` depends on a few patches that are
not in any stable Pelican release yet (most importantly
https://github.com/getpelican/pelican/pull/2246), in order to have them,
install Pelican from my local fork instead:

.. code:: sh

    pip install git+https://github.com/mosra/pelican.git@mosra-master

CONTRIBUTING
============

Head over to the `contribution guide <CONTRIBUTING.rst>`_.

CONTACT
=======

Want to learn more about m.css? Found a bug or want to share an awesome idea?
Feel free to visit the project website or contact the author at:

-   Website --- http://mcss.mosra.cz
-   GitHub --- https://github.com/mosra/m.css
-   Gitter --- https://gitter.im/mosra/m.css
-   Twitter --- https://twitter.com/czmosra
-   E-mail --- mosra@centrum.cz
-   Jabber --- mosra@jabbim.cz

CREDITS
=======

See the `CREDITS.rst <CREDITS.rst>`_ file for details about contributors and
third-party code involved in this project. Big thanks to everyone involved!

LICENSE
=======

m.css is licensed under MIT/Expat license, see `COPYING <COPYING>`_ file for
details.
