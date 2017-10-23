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

Test
####

:save_as: css/components/test/index.html
:breadcrumb: {filename}/css.rst CSS
             {filename}/css/components.rst Components

Blocks
======

.. raw:: html

    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-default">
          <h3>Default block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-primary">
          <h3>Primary block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-success">
          <h3>Success block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-warning">
          <h3>Warning block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-danger">
          <h3>Danger block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-info">
          <h3>Info block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-dim">
          <h3>Dim block</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>

Notes, frame
============

.. raw:: html

    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-default">
          <h3>Default note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-primary">
          <h3>Primary note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-success">
          <h3>Success note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-warning">
          <h3>Warning note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-danger">
          <h3>Danger note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-info">
          <h3>Info note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-dim">
          <h3>Dim note</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-frame">
          <h3>Frame</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>

Text
====

.. raw:: html

    <p class="m-text m-default">Default text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-primary">Primary text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-success">Success text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-warning">Warning text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-danger">Danger text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-info">Info text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>
    <p class="m-text m-dim">Dim text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula. <a href="#">Link.</a></p>

Tables
======

.. raw:: html

    <table class="m-table m-center-t">
      <caption>Table caption</caption>
      <thead>
        <tr>
          <th>#</th>
          <th>Heading</th>
          <th>Second<br/>heading</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">1</th>
          <td>Cell</td>
          <td>Second cell</td>
        </tr>
      </tbody>
      <tbody>
        <tr>
          <th scope="row">2</th>
          <td>2nd row cell</td>
          <td>2nd row 2nd cell</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <th>&Sigma;</th>
          <td>Footer</td>
          <td>Second<br/>footer</td>
        </tr>
      </tfoot>
    </table>
    <div class="m-scroll"><table class="m-table m-fullwidth">
      <caption>Full-width table</caption>
      <thead>
        <tr>
          <th>#</th>
          <th>Heading text</th>
          <th>Heading text</th>
          <th>Heading text</th>
          <th>Heading text</th>
          <th>Heading text</th>
          <th>Heading text</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">1</th>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
          <td>Cell contents</td>
        </tr>
      </tbody>
    </table></div>
    <div class="m-scroll"><table class="m-table m-center-t">
      <tbody>
        <tr class="m-default">
          <th>Default row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-primary">
          <th>Primary row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-success">
          <th>Success row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-warning">
          <th>Warning row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-danger">
          <th>Danger row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-info">
          <th>Info row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr class="m-dim">
          <th>Dim row</th>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
          <td><a href="#">Link</a></td>
        </tr>
        <tr>
          <td class="m-default">Default cell</td>
          <td class="m-default"><a href="#">Link</a></td>
          <td class="m-default">Lorem</td>
          <td class="m-default">ipsum</td>
          <td class="m-default">dolor</td>
          <td class="m-default">sit</td>
          <td class="m-default">amet</td>
        </tr>
        <tr>
          <td class="m-primary">Primary cell</td>
          <td class="m-primary"><a href="#">Link</a></td>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td class="m-default">Lorem</td>
          <td class="m-success">Success cell</td>
          <td class="m-success"><a href="#">Link</a></td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td class="m-default">ipsum</td>
          <td class="m-warning">Warning cell</td>
          <td class="m-warning"><a href="#">Link</a></td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td class="m-default">dolor</td>
          <td class="m-danger">Danger cell</td>
          <td class="m-danger"><a href="#">Link</a></td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td class="m-default">sit</td>
          <td class="m-info">Info cell</td>
          <td class="m-info"><a href="#">Link</a></td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td class="m-default">amet</td>
          <td class="m-dim">Dim cell</td>
          <td class="m-dim"><a href="#">Link</a></td>
        </tr>
        <tr>
          <th class="m-default">Default header</th>
          <td class="m-default"><a href="#">Link</a></td>
          <td class="m-default">Lorem</td>
          <td class="m-default">ipsum</td>
          <td class="m-default">dolor</td>
          <td class="m-default">sit</td>
          <td class="m-default">amet</td>
        </tr>
        <tr>
          <th class="m-primary">Primary header</th>
          <td class="m-primary"><a href="#">Link</a></td>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td class="m-default">Lorem</td>
          <th class="m-success">Success header</th>
          <td class="m-success"><a href="#">Link</a></td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td class="m-default">ipsum</td>
          <th class="m-warning">Warning header</th>
          <td class="m-warning"><a href="#">Link</a></td>
          <td>dolor</td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td class="m-default">dolor</td>
          <th class="m-danger">Danger header</th>
          <td class="m-danger"><a href="#">Link</a></td>
          <td>sit</td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td class="m-default">sit</td>
          <th class="m-info">Info header</th>
          <td class="m-info"><a href="#">Link</a></td>
          <td>amet</td>
        </tr>
        <tr>
          <td>Lorem</td>
          <td>ipsum</td>
          <td>dolor</td>
          <td>sit</td>
          <td class="m-default">amet</td>
          <th class="m-dim">Dim header</th>
          <td class="m-dim"><a href="#">Link</a></td>
        </tr>
      </tbody>
    </table>

Images
======

Image, centered:

.. raw:: html

    <img src="{filename}/static/flowers-small.jpg" class="m-image" />

Image, centered, link:

.. raw:: html

    <div class="m-image">
      <a href="http://blog.mosra.cz/"><img src="{filename}/static/flowers-small.jpg" /></a>
    </div>

Image, fullwidth (yes, it should be pixelated):

.. raw:: html

    <img src="{filename}/static/flowers-small.jpg" class="m-image m-fullwidth" />

Image, fullwidth, link (yes, it should be pixelated):

.. raw:: html

    <div class="m-image m-fullwidth">
      <a href="http://blog.mosra.cz/"><img src="{filename}/static/flowers-small.jpg" /></a>
    </div>

Figures
=======

Figure, centered:

.. raw:: html

    <figure class="m-figure">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Ship</figcaption>
      <div>Photo © <a href="http://blog.mosra.cz/">The Author</a></div>
    </figure>

Figure, centered, image link, flat:

.. raw:: html

    <figure class="m-figure m-flat">
      <a href="http://blog.mosra.cz/"><img src="{filename}/static/ship-small.jpg" /></a>
      <figcaption>A Ship</figcaption>
      <div>Photo © <a href="http://blog.mosra.cz/">The Author</a></div>
    </figure>

Figure, fullwidth, without description (yes, it should be pixelated):

.. raw:: html

    <figure class="m-figure m-fullwidth">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Ship</figcaption>
    </figure>

Image grid
==========

Without the link:

.. raw:: html

    <div class="m-imagegrid m-container-inflate">
      <div>
        <figure style="width: 69.127%">
          <img src="{filename}/static/ship.jpg" />
          <figcaption>F9.0, 1/250 s, ISO 100</figcaption>
        </figure>
        <figure style="width: 30.873%">
          <img src="{filename}/static/flowers.jpg" />
          <figcaption>F2.8, 1/1600 s, ISO 100</figcaption>
        </figure>
      </div>
    </div>

With link, without caption, not inflated:

.. raw:: html

    <div class="m-imagegrid">
      <div>
        <figure style="width: 30.873%">
          <a href="{filename}/static/flowers.jpg">
            <img src="{filename}/static/flowers.jpg" />
            <div></div>
          </a>
        </figure>
        <figure style="width: 69.127%">
          <a href="{filename}/static/ship.jpg">
            <img src="{filename}/static/ship.jpg" />
            <div></div>
          </a>
        </figure>
      </div>
    </div>

Without link or caption:

.. raw:: html

    <div class="m-imagegrid m-container-inflate">
      <div>
        <figure style="width: 69.127%">
          <img src="{filename}/static/ship.jpg" />
          <div></div>
        </figure>
        <figure style="width: 30.873%">
          <img src="{filename}/static/flowers.jpg" />
          <div></div>
        </figure>
      </div>
    </div>

`Code figure`_
==============

A flat code figure:

.. raw:: html

    <figure class="m-code-figure m-flat">
        <pre>Some
        code
    snippet</pre>
        And a resulting output.
    </figure>

A code figure with :html:`<pre>` in description. Activating the section header
should not affect it.

.. raw:: html

    <figure class="m-code-figure">
        <pre>Some
        code
    snippet</pre>
        <pre>And a resulting output.</pre>
    </figure>
