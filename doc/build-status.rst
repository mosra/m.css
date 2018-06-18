Build Status
############

:summary: CI build status of m.css
:footer:
    .. raw:: html

        <style>
          table.build-status th, table.build-status td {
            text-align: center;
            vertical-align: middle;
          }
          table.build-status td {
            padding: 0;
            min-width: 5rem;
          }
          table.build-status a {
            display: block;
            width: 100%;
            height: 100%;
            padding: 0.25rem 0.5rem;
            text-decoration: none;
          }
        </style>
        <script>

    .. raw:: html
        :file: build-status.js

    .. raw:: html

        </script>

Show builds for:

-   `master branch <{filename}/build-status.rst>`_
-   `next branch <{filename}/build-status.rst?mosra/m.css=next>`_

.. container:: m-container-inflate

    .. container:: m-scroll

        .. raw:: html

            <table class="m-table build-status">
              <thead>
                <tr>
                  <th></th>
                  <th>Python<br />3.4</th>
                  <th>Python<br />3.5</th>
                  <th>Python<br />3.6</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th class="m-text-right">Pelican theme</th>
                  <td rowspan="2" id="mcss-py34"><a>&nbsp;<br/><span class="m-text m-small">&nbsp;</span></a></td>
                  <td rowspan="3" id="mcss-py35"><a>&nbsp;<br/><span class="m-text m-small">&nbsp;</span></a></td>
                  <td rowspan="4" id="mcss-py36"><a>&nbsp;<br/><span class="m-text m-small">&nbsp;</span></a></td>
                </tr>
                <tr>
                  <th class="m-text-right">Pelican plugins</th>
                </tr>
                <tr>
                  <th class="m-text-right">Graph rendering</th>
                  <td class="m-dim"></td>
                </tr>
                <tr>
                  <th class="m-text-right">Doxygen theme</th>
                  <td class="m-dim"></td>
                  <td class="m-dim"></td>
                </tr>
                <tr>
                  <th class="m-text-right">Doxygen theme<br/>client search</th>
                  <td class="m-dim"></td>
                  <td class="m-dim"></td>
                  <td id="mcss-js"><a>&nbsp;<br/><span class="m-text m-small">&nbsp;</span></a></td>
                </tr>
                <tr>
                  <th class="m-text-right">Math rendering</th>
                  <td class="m-dim"></td>
                  <td class="m-dim"></td>
                  <td class="m-dim"></td>
                </tr>
              </tbody>
            </table>
