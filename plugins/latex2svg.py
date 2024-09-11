#!/usr/bin/env python3
"""latex2svg

Read LaTeX code from stdin and render a SVG using LaTeX + dvisvgm.
"""
__version__ = '0.1.0'
__author__ = 'Tino Wagner'
__email__ = 'ich@tinowagner.com'
__license__ = 'MIT'
__copyright__ = '(c) 2017, Tino Wagner'

import os
import sys
import subprocess
import shlex
import re
from tempfile import TemporaryDirectory
from ctypes.util import find_library

default_template = r"""
\documentclass[{{ fontsize }}pt,preview]{standalone}
{{ preamble }}
\begin{document}
\begin{preview}
{{ code }}
\end{preview}
\end{document}
"""

default_preamble = r"""
\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
\usepackage[libertine]{newtxmath}
"""

latex_cmd = 'latex -interaction nonstopmode -halt-on-error'
dvisvgm_cmd = 'dvisvgm --no-fonts'

default_params = {
    'fontsize': 12,  # pt
    'template': default_template,
    'preamble': default_preamble,
    'latex_cmd': latex_cmd,
    'dvisvgm_cmd': dvisvgm_cmd,
    'libgs': None,
}

libgs = find_library('gs')
if not hasattr(os.environ, 'LIBGS') and not libgs:
    if sys.platform == 'darwin':
        # Fallback to homebrew Ghostscript on macOS
        homebrew_libgs = '/usr/local/opt/ghostscript/lib/libgs.dylib'
        if os.path.exists(homebrew_libgs):
            default_params['libgs'] = homebrew_libgs
    if not default_params['libgs']:
        print('Warning: libgs not found')
# dvisvgm < 3.0 only looks for ghostscript < 10 on its own, attempt to supply
# it directly if version 10 is found. Fixed in
# https://github.com/mgieseki/dvisvgm/commit/46b11c02a46883309a824e3fc798f8093041daec
# TODO related https://bugs.archlinux.org/task/76083 was resolved on May 29th
# 2023, remove after enough time passes if no similar case happens in other
# distros
elif '.so.10' in str(libgs):
    # If dvisvgm seems to be at least 3.0, don't even attempt to find libgs and
    # just assume it works
    dvisvgm_is_new_enough = False
    try:
        ret = subprocess.run(['dvisvgm', '--version'], stdout=subprocess.PIPE)
        if b'dvisvgm 3' in ret.stdout:
            dvisvgm_is_new_enough = True
    except:
        pass

    # Just winging it here, there doesn't seem to be an easy way to get the
    # actual full path the library was found in -- ctypes/util.py does crazy
    # stuff like invoking gcc (!!) to get the library filename.
    #
    # On Arch /usr/lib64 is a symlink to /usr/lib, so only the former is
    # needed; on Fedora it's two distinct directories and libgs is in the
    # latter (ugh). Elsewhere it might be /usr/lib/x86_64-linux-gnu or just
    # anything else, so let's just bet that dvisvgm is 3.0+ in most cases and
    # this gets hit only very rarely.
    if not dvisvgm_is_new_enough:
        prefixes = ['/usr/lib', '/usr/lib64']
        for prefix in prefixes:
            libgs_absolute = os.path.join(prefix, libgs)
            if os.path.exists(libgs_absolute):
                default_params['libgs'] = libgs_absolute
                break
        else:
            raise RuntimeError('libgs found by linker magic, but is not in {}'.format(' or '.join(prefixes)))

def latex2svg(code, params=default_params, working_directory=None):
    """Convert LaTeX to SVG using dvisvgm.

    Parameters
    ----------
    code : str
        LaTeX code to render.
    params : dict
        Conversion parameters.
    working_directory : str or None
        Working directory for external commands and place for temporary files.

    Returns
    -------
    dict
        Dictionary of SVG output and output information:

        * `svg`: SVG data
        * `width`: image width in *em*
        * `height`: image height in *em*
        * `depth`: baseline position in *em*
    """
    if working_directory is None:
        with TemporaryDirectory() as tmpdir:
            return latex2svg(code, params, working_directory=tmpdir)

    fontsize = params['fontsize']
    document = (params['template']
                .replace('{{ preamble }}', params['preamble'])
                .replace('{{ fontsize }}', str(fontsize))
                .replace('{{ code }}', code))

    with open(os.path.join(working_directory, 'code.tex'), 'w') as f:
        f.write(document)

    # Run LaTeX and create DVI file
    try:
        ret = subprocess.run(shlex.split(params['latex_cmd']+' code.tex'),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=working_directory)
        # LaTeX prints errors on stdout instead of stderr (stderr is empty),
        # so print stdout instead
        if ret.returncode: print(ret.stdout.decode('utf-8'))
        ret.check_returncode()
    except FileNotFoundError:
        raise RuntimeError('latex not found')

    # Add LIBGS to environment if supplied
    env = os.environ.copy()
    if params['libgs']:
        env['LIBGS'] = params['libgs']

    # Convert DVI to SVG
    try:
        ret = subprocess.run(shlex.split(params['dvisvgm_cmd']+' code.dvi'),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=working_directory, env=env)
        if ret.returncode: print(ret.stderr.decode('utf-8'))
        ret.check_returncode()
    except FileNotFoundError:
        raise RuntimeError('dvisvgm not found')

    with open(os.path.join(working_directory, 'code.svg'), 'r') as f:
        svg = f.read()

    # Parse dvisvgm output for size and alignment
    def get_size(output):
        regex = r'\b([0-9.]+)pt x ([0-9.]+)pt'
        match = re.search(regex, output)
        if match:
            return (float(match.group(1)) / fontsize,
                    float(match.group(2)) / fontsize)
        else:
            return None, None

    def get_measure(output, name):
        regex = r'\b%s=([0-9.e-]+)pt' % name
        match = re.search(regex, output)
        if match:
            return float(match.group(1)) / fontsize
        else:
            return None

    output = ret.stderr.decode('utf-8')

    # Since we rely on Ghostscript to give us a "depth" (= vertical alignment)
    # value, dvisvgm not using it means the output would be broken and it makes
    # no sense to continue.
    if 'Ghostscript not found' in output:
        raise RuntimeError('libgs not detected by dvisvgm, point the LIBGS environment variable to its location')

    width, height = get_size(output)
    depth = get_measure(output, 'depth')
    return {'svg': svg, 'depth': depth, 'width': width, 'height': height}


def main():
    """Simple command line interface to latex2svg.

    - Read from `stdin`.
    - Write SVG to `stdout`.
    - Write metadata as JSON to `stderr`.
    - On error: write error messages to `stdout` and return with error code.
    """
    import json
    import argparse
    parser = argparse.ArgumentParser(description="""
    Render LaTeX code from stdin as SVG to stdout. Writes metadata (baseline
    position, width, height in em units) as JSON to stderr.
    """)
    parser.add_argument('--preamble',
                        help="LaTeX preamble code to read from file")
    args = parser.parse_args()
    preamble = default_preamble
    if args.preamble is not None:
        with open(args.preamble) as f:
            preamble = f.read()
    latex = sys.stdin.read()
    try:
        params = default_params.copy()
        params['preamble'] = preamble
        out = latex2svg(latex, params)
        sys.stdout.write(out['svg'])
        meta = {key: out[key] for key in out if key != 'svg'}
        sys.stderr.write(json.dumps(meta))
    except subprocess.CalledProcessError as exc:
        print(exc.output.decode('utf-8'))
        sys.exit(exc.returncode)


if __name__ == '__main__':
    main()
