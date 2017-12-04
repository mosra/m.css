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

.. role:: html(code)
    :language: html

Blocks
======

Different :html:`<h*>` tags, the styling should be preserved across all sizes.

.. raw:: html

    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-default">
          <h3>Default block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-default">
          <h4>Default block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-default">
          <h5>Default block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-default">
          <h6>Default block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-primary">
          <h3>Primary block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-primary">
          <h4>Primary block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-primary">
          <h5>Primary block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-primary">
          <h6>Primary block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-success">
          <h3>Success block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-success">
          <h4>Success block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-success">
          <h5>Success block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-success">
          <h6>Success block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-warning">
          <h3>Warning block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-warning">
          <h4>Warning block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-warning">
          <h5>Warning block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-warning">
          <h6>Warning block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-danger">
          <h3>Danger block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-danger">
          <h4>Danger block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-danger">
          <h5>Danger block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-danger">
          <h6>Danger block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-info">
          <h3>Info block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-info">
          <h4>Info block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-info">
          <h5>Info block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-info">
          <h6>Info block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-dim">
          <h3>Dim block h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-dim">
          <h4>Dim block h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-dim">
          <h5>Dim block h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-block m-dim">
          <h6>Dim block h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. <a href="#">Link.</a>
        </div>
      </div>
    </div>

Badge
=====

Badge with lots of text and less text:

.. raw:: html

    <div class="m-block m-badge m-primary">
      <img src="{filename}/static/mosra.jpg" alt="The Author" />
      <h3>About the author</h3>
      <p><a href="#">The Author</a> is lorem ipsum dolor sit amet, consectetur
      adipiscing elit. Aenean id elit posuere, consectetur magna congue,
      sagittis est. Pellentesque est neque, aliquet nec consectetur in, mattis
      ac diam. Aliquam placerat justo ut purus interdum, ac placerat lacus
      consequat. Mauris id suscipit mauris, in scelerisque lectus.</p>
    </div>

    <div class="m-block m-badge m-dim">
      <img src="{filename}/static/mosra.jpg" alt="The Author" />
      <h3>About the author</h3>
      <p><a href="#">The Author</a> is lorem ipsum dolor sit amet, consectetur
      adipiscing elit.</p>
    </div>

Notes, frame
============

Different :html:`<h*>` tags.

.. raw:: html

    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-default">
          <h3>Default note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-default">
          <h4>Default note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-default">
          <h5>Default note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-default">
          <h6>Default note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-primary">
          <h3>Primary note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-primary">
          <h4>Primary note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-primary">
          <h5>Primary note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-primary">
          <h6>Primary note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-success">
          <h3>Success note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-success">
          <h4>Success note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-success">
          <h5>Success note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-success">
          <h6>Success note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-warning">
          <h3>Warning note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-warning">
          <h4>Warning note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-warning">
          <h5>Warning note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-warning">
          <h6>Warning note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-danger">
          <h3>Danger note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-danger">
          <h4>Danger note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-danger">
          <h5>Danger note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-danger">
          <h6>Danger note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-info">
          <h3>Info note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-info">
          <h4>Info note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-info">
          <h5>Info note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-info">
          <h6>Info note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-dim">
          <h3>Dim note h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-dim">
          <h4>Dim note h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-dim">
          <h5>Dim note h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-note m-dim">
          <h6>Dim note h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>
    <div class="m-row">
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-frame">
          <h3>Frame h3</h3>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-frame">
          <h4>Frame h4</h4>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-clearfix-s"></div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-frame">
          <h5>Frame h5</h5>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
      <div class="m-col-m-3 m-col-s-6">
        <div class="m-frame">
          <h6>Frame h6</h6>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="#">Link.</a>
        </div>
      </div>
    </div>

Labels
======

They should have proper vertical alignment.

.. raw:: html

    <h1>Heading 1 <span class="m-label m-default">label</span> <span class="m-label m-dim">label</span></h1>
    <h2>Heading 2 <span class="m-label m-primary">label</span> <span class="m-label m-flat m-default">flat</span></h2>
    <h3>Heading 3 <span class="m-label m-success">label</span> <span class="m-label m-flat m-primary">flat</span></h3>
    <h4>Heading 4 <span class="m-label m-warning">label</span> <span class="m-label m-flat m-success">flat</span></h4>
    <h5>Heading 5 <span class="m-label m-danger">label</span> <span class="m-label m-flat m-warning">flat</span></h5>
    <h6>Heading 6 <span class="m-label m-info">label</span> <span class="m-label m-flat m-danger">flat</span></h6>

    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span class="m-label m-primary">label</span> <span class="m-label m-flat m-info">flat</span> Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula.</p>

    <p class="m-text m-big">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ultrices <span class="m-label m-success">label</span> <span class="m-label m-flat m-dim">flat</span> a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula.</p>

    <p class="m-text m-small">Lorem ipsum dolor sit amet,  <span class="m-label m-warning">label</span> <span class="m-label m-flat m-info">flat</span> consectetur adipiscing elit. Vivamus ultrices a erat eu suscipit. Aliquam pharetra imperdiet tortor sed vehicula.</p>

Tables
======

.. raw:: html

    <table class="m-table m-flat">
      <caption>Flat table (w/o hover effect)</caption>
      <tr>
        <th scope="row">1</th>
        <td>Cell</td>
        <td>Second cell</td>
      </tr>
      <tr>
        <th scope="row">2</th>
        <td>2nd row cell</td>
        <td>2nd row 2nd cell</td>
      </tr>
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
      <span>Photo © <a href="http://blog.mosra.cz/">The Author</a></span>
    </figure>

Figure, centered, image link, flat:

.. raw:: html

    <figure class="m-figure m-flat">
      <a href="http://blog.mosra.cz/"><img src="{filename}/static/ship-small.jpg" /></a>
      <figcaption>A Ship</figcaption>
      <span>Photo © <a href="http://blog.mosra.cz/">The Author</a></span>
    </figure>

Figure, fullwidth, without description (yes, it should be pixelated):

.. raw:: html

    <figure class="m-figure m-fullwidth">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Ship</figcaption>
    </figure>

Figure, fullwidth, with a long caption and description, there should be no
unnecessary wrapping of the text:

.. raw:: html

    <figure class="m-figure m-fullwidth">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Somewhat Lengthy Caption For A Photo</figcaption>
      <span>The Photo Displayed Above Was Kindly Taken And Allowed To Be Used
      On This Page By <a href="http://blog.mosra.cz/">The Author</a>. All
      Rights Reserved.</span>
    </figure>

Figure with a large image but not fullwidth, should look the same as above, no
leaking of the image outside of the page:

.. raw:: html

    <figure class="m-figure">
      <img src="{filename}/static/ship.jpg" />
      <figcaption>A Somewhat Lengthy Caption For A Photo</figcaption>
      <span>The Photo Displayed Above Was Kindly Taken And Allowed To Be Used
      On This Page By <a href="http://blog.mosra.cz/">The Author</a>. All
      Rights Reserved.</span>
    </figure>

Figure with a long caption and description, then just a caption (it should wrap
instead of extending the border and there should be proper padding on bottom):

.. raw:: html

    <figure class="m-figure">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Somewhat Lengthy Caption For A Photo</figcaption>
      <span>The Photo Displayed Above Was Kindly Taken And Allowed To Be Used
      On This Page By <a href="http://blog.mosra.cz/">The Author</a>. All
      Rights Reserved.</span>
    </figure>

.. raw:: html

    <figure class="m-figure">
      <img src="{filename}/static/ship-small.jpg" />
      <figcaption>A Somewhat Lengthy Caption For A Photo</figcaption>
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

.. don't remove the header link, needed for testing!

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

Console figure:

.. raw:: html

    <figure class="m-console-figure">
        <pre class="m-console">Some
        console
    output</pre>
        And a description of that illegal crackery that's done above.
    </figure>
