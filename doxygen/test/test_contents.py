#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

import os
import pickle
import shutil
import subprocess
import unittest

from hashlib import sha1

from distutils.version import LooseVersion

from . import BaseTestCase, IntegrationTestCase, doxygen_version

class Typography(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'typography', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Blocks(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'blocks', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertEqual(*self.actual_expected_contents('todo.html'))
        # Multiple xrefitems should be merged into one
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(*self.actual_expected_contents('old.html'))

class Code(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'code', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class CodeLanguage(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'code_language', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/621")
    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/623")
    def test_ansi(self):
        self.run_dox2html5(wildcard='ansi.xml')
        self.assertEqual(*self.actual_expected_contents('ansi.html'))

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/621")
    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Image(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'image', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'tiny.png')))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Math(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'math', *args, **kwargs)

    @unittest.skipUnless(shutil.which('latex'),
                         "Math rendering requires LaTeX installed")
    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    @unittest.skipUnless(shutil.which('latex'),
                         "Math rendering requires LaTeX installed")
    def test_latex_error(self):
        with self.assertRaises(subprocess.CalledProcessError) as context:
            self.run_dox2html5(wildcard='error.xml')

class MathCached(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'math_cached', *args, **kwargs)

       # Actually generated from $ \frac{\tau}{2} $ tho
        self.tau_half_hash = sha1("""$ \pi $""".encode('utf-8')).digest()
        self.tau_half = """<?xml version='1.0' encoding='UTF-8'?>
<!-- This file was generated by dvisvgm 2.1.3 -->
<svg height='15.3267pt' version='1.1' viewBox='1.19551 -8.1387 4.67835 12.2613' width='5.84794pt' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
<defs>
<path d='M2.50262 -2.90909H3.92927C4.05679 -2.90909 4.14446 -2.90909 4.22416 -2.97285C4.3198 -3.06052 4.34371 -3.16413 4.34371 -3.21196C4.34371 -3.43512 4.14446 -3.43512 4.00897 -3.43512H1.60199C1.43462 -3.43512 1.13176 -3.43512 0.74122 -3.05255C0.454296 -2.76563 0.231133 -2.399 0.231133 -2.34321C0.231133 -2.27148 0.286924 -2.24757 0.350685 -2.24757C0.430386 -2.24757 0.446326 -2.27148 0.494147 -2.33524C0.884682 -2.90909 1.35492 -2.90909 1.53823 -2.90909H2.22366L1.53823 -0.70137C1.48244 -0.518057 1.37883 -0.191283 1.37883 -0.151432C1.37883 0.0318804 1.5462 0.0956413 1.64184 0.0956413C1.93674 0.0956413 1.98456 -0.183313 2.00847 -0.302864L2.50262 -2.90909Z' id='g0-28'/>
<path d='M2.24757 -1.6259C2.37509 -1.74545 2.70984 -2.00847 2.83736 -2.12005C3.33151 -2.57435 3.80174 -3.0127 3.80174 -3.73798C3.80174 -4.68643 3.00473 -5.30012 2.00847 -5.30012C1.05205 -5.30012 0.422416 -4.57484 0.422416 -3.8655C0.422416 -3.47497 0.73325 -3.41918 0.844832 -3.41918C1.0122 -3.41918 1.25928 -3.53873 1.25928 -3.84159C1.25928 -4.25604 0.860772 -4.25604 0.765131 -4.25604C0.996264 -4.83786 1.53026 -5.03711 1.9208 -5.03711C2.66202 -5.03711 3.04458 -4.40747 3.04458 -3.73798C3.04458 -2.90909 2.46276 -2.30336 1.52229 -1.33898L0.518057 -0.302864C0.422416 -0.215193 0.422416 -0.199253 0.422416 0H3.57061L3.80174 -1.42665H3.55467C3.53076 -1.26725 3.467 -0.868742 3.37136 -0.71731C3.32354 -0.653549 2.71781 -0.653549 2.59029 -0.653549H1.17161L2.24757 -1.6259Z' id='g1-50'/>
</defs>
<g id='page1'>
<use x='1.19551' xlink:href='#g0-28' y='-4.70713'/>
<rect height='0.478187' width='4.67835' x='1.19551' y='-3.22789'/>
<use x='1.4176' xlink:href='#g1-50' y='4.12263'/>
</g>
</svg>"""
        # Actually generated from \[ a^3 + b^3 \neq c^3 \] tho
        self.fermat_hash = sha1("""\[ a^2 + b^2 = c^2 \]""".encode('utf-8')).digest()
        self.fermat = """<?xml version='1.0' encoding='UTF-8'?>
<!-- This file was generated by dvisvgm 2.1.3 -->
<svg height='15.4964pt' version='1.1' viewBox='164.011 -12.3971 60.0231 12.3971' width='75.0289pt' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
<defs>
<path d='M7.53176 -8.09365C7.6274 -8.26102 7.6274 -8.28493 7.6274 -8.3208C7.6274 -8.40448 7.55567 -8.5599 7.38829 -8.5599C7.24483 -8.5599 7.20897 -8.48817 7.12528 -8.3208L1.75741 2.11606C1.66177 2.28344 1.66177 2.30735 1.66177 2.34321C1.66177 2.43885 1.74545 2.58232 1.90087 2.58232C2.04433 2.58232 2.0802 2.51059 2.16389 2.34321L7.53176 -8.09365Z' id='g0-54'/>
<path d='M3.59851 -1.42267C3.53873 -1.21943 3.53873 -1.19552 3.37136 -0.968369C3.10834 -0.633624 2.58232 -0.119552 2.02042 -0.119552C1.53026 -0.119552 1.25529 -0.561893 1.25529 -1.26725C1.25529 -1.92478 1.6259 -3.26376 1.85305 -3.76588C2.25953 -4.60274 2.82142 -5.03313 3.28767 -5.03313C4.07671 -5.03313 4.23213 -4.0528 4.23213 -3.95716C4.23213 -3.94521 4.19626 -3.78979 4.18431 -3.76588L3.59851 -1.42267ZM4.36364 -4.48319C4.23213 -4.79402 3.90934 -5.27223 3.28767 -5.27223C1.93674 -5.27223 0.478207 -3.52677 0.478207 -1.75741C0.478207 -0.573848 1.17161 0.119552 1.98456 0.119552C2.64209 0.119552 3.20399 -0.394521 3.53873 -0.789041C3.65828 -0.0836862 4.22017 0.119552 4.57883 0.119552S5.22441 -0.0956413 5.4396 -0.526027C5.63088 -0.932503 5.79826 -1.66177 5.79826 -1.70959C5.79826 -1.76936 5.75044 -1.81719 5.6787 -1.81719C5.57111 -1.81719 5.55915 -1.75741 5.51133 -1.57808C5.332 -0.872727 5.10486 -0.119552 4.61469 -0.119552C4.268 -0.119552 4.24408 -0.430386 4.24408 -0.669489C4.24408 -0.944458 4.27995 -1.07597 4.38755 -1.54222C4.47123 -1.8411 4.53101 -2.10411 4.62665 -2.45081C5.06899 -4.24408 5.17659 -4.67447 5.17659 -4.7462C5.17659 -4.91357 5.04508 -5.04508 4.86575 -5.04508C4.48319 -5.04508 4.38755 -4.62665 4.36364 -4.48319Z' id='g1-97'/>
<path d='M2.76164 -7.99801C2.7736 -8.04583 2.79751 -8.11756 2.79751 -8.17733C2.79751 -8.29689 2.67796 -8.29689 2.65405 -8.29689C2.64209 -8.29689 2.21171 -8.26102 1.99651 -8.23711C1.79328 -8.22516 1.61395 -8.20125 1.39875 -8.18929C1.11183 -8.16538 1.02814 -8.15342 1.02814 -7.93823C1.02814 -7.81868 1.1477 -7.81868 1.26725 -7.81868C1.87696 -7.81868 1.87696 -7.71108 1.87696 -7.59153C1.87696 -7.50785 1.78132 -7.16115 1.7335 -6.94595L1.44658 -5.79826C1.32702 -5.32005 0.645579 -2.60623 0.597758 -2.39103C0.537983 -2.09215 0.537983 -1.88892 0.537983 -1.7335C0.537983 -0.514072 1.21943 0.119552 1.99651 0.119552C3.38331 0.119552 4.81793 -1.66177 4.81793 -3.39527C4.81793 -4.49514 4.19626 -5.27223 3.29963 -5.27223C2.67796 -5.27223 2.11606 -4.75816 1.88892 -4.51905L2.76164 -7.99801ZM2.00847 -0.119552C1.6259 -0.119552 1.20747 -0.406476 1.20747 -1.33898C1.20747 -1.7335 1.24334 -1.96065 1.45853 -2.79751C1.4944 -2.95293 1.68568 -3.71806 1.7335 -3.87347C1.75741 -3.96912 2.46276 -5.03313 3.27572 -5.03313C3.80174 -5.03313 4.04085 -4.5071 4.04085 -3.88543C4.04085 -3.31158 3.7061 -1.96065 3.40722 -1.33898C3.10834 -0.6934 2.55841 -0.119552 2.00847 -0.119552Z' id='g1-98'/>
<path d='M4.67447 -4.49514C4.44732 -4.49514 4.33973 -4.49514 4.17235 -4.35168C4.10062 -4.29191 3.96912 -4.11258 3.96912 -3.9213C3.96912 -3.68219 4.14844 -3.53873 4.37559 -3.53873C4.66252 -3.53873 4.98531 -3.77783 4.98531 -4.25604C4.98531 -4.82989 4.43537 -5.27223 3.61046 -5.27223C2.04433 -5.27223 0.478207 -3.56264 0.478207 -1.86501C0.478207 -0.824907 1.12379 0.119552 2.34321 0.119552C3.96912 0.119552 4.99726 -1.1477 4.99726 -1.30311C4.99726 -1.37484 4.92553 -1.43462 4.87771 -1.43462C4.84184 -1.43462 4.82989 -1.42267 4.72229 -1.31507C3.95716 -0.298879 2.82142 -0.119552 2.36712 -0.119552C1.54222 -0.119552 1.2792 -0.836862 1.2792 -1.43462C1.2792 -1.85305 1.48244 -3.0127 1.91283 -3.82565C2.22366 -4.38755 2.86924 -5.03313 3.62242 -5.03313C3.77783 -5.03313 4.43537 -5.00922 4.67447 -4.49514Z' id='g1-99'/>
<path d='M2.01644 -2.66202C2.64608 -2.66202 3.04458 -2.19975 3.04458 -1.36289C3.04458 -0.366625 2.4787 -0.071731 2.05629 -0.071731C1.61793 -0.071731 1.02017 -0.231133 0.74122 -0.653549C1.02814 -0.653549 1.2274 -0.836862 1.2274 -1.09988C1.2274 -1.35492 1.04408 -1.53823 0.789041 -1.53823C0.573848 -1.53823 0.350685 -1.40274 0.350685 -1.08394C0.350685 -0.326775 1.16364 0.167372 2.07223 0.167372C3.13225 0.167372 3.87347 -0.565878 3.87347 -1.36289C3.87347 -2.02441 3.34745 -2.63014 2.5345 -2.80548C3.16413 -3.02864 3.63437 -3.57061 3.63437 -4.20822S2.91706 -5.30012 2.08817 -5.30012C1.23537 -5.30012 0.589788 -4.83786 0.589788 -4.23213C0.589788 -3.93724 0.789041 -3.80971 0.996264 -3.80971C1.24334 -3.80971 1.40274 -3.98506 1.40274 -4.21619C1.40274 -4.51108 1.1477 -4.62267 0.972354 -4.63064C1.3071 -5.06899 1.9208 -5.0929 2.06426 -5.0929C2.27148 -5.0929 2.87721 -5.02914 2.87721 -4.20822C2.87721 -3.65031 2.64608 -3.31557 2.5345 -3.18804C2.29539 -2.94097 2.11208 -2.92503 1.6259 -2.89315C1.47447 -2.88518 1.41071 -2.87721 1.41071 -2.7736C1.41071 -2.66202 1.48244 -2.66202 1.61793 -2.66202H2.01644Z' id='g2-51'/>
<path d='M4.77011 -2.76164H8.06974C8.23711 -2.76164 8.4523 -2.76164 8.4523 -2.97684C8.4523 -3.20399 8.24907 -3.20399 8.06974 -3.20399H4.77011V-6.50361C4.77011 -6.67098 4.77011 -6.88618 4.55492 -6.88618C4.32777 -6.88618 4.32777 -6.68294 4.32777 -6.50361V-3.20399H1.02814C0.860772 -3.20399 0.645579 -3.20399 0.645579 -2.98879C0.645579 -2.76164 0.848817 -2.76164 1.02814 -2.76164H4.32777V0.537983C4.32777 0.705355 4.32777 0.920548 4.54296 0.920548C4.77011 0.920548 4.77011 0.71731 4.77011 0.537983V-2.76164Z' id='g3-43'/>
<path d='M8.06974 -3.87347C8.23711 -3.87347 8.4523 -3.87347 8.4523 -4.08867C8.4523 -4.31582 8.24907 -4.31582 8.06974 -4.31582H1.02814C0.860772 -4.31582 0.645579 -4.31582 0.645579 -4.10062C0.645579 -3.87347 0.848817 -3.87347 1.02814 -3.87347H8.06974ZM8.06974 -1.64981C8.23711 -1.64981 8.4523 -1.64981 8.4523 -1.86501C8.4523 -2.09215 8.24907 -2.09215 8.06974 -2.09215H1.02814C0.860772 -2.09215 0.645579 -2.09215 0.645579 -1.87696C0.645579 -1.64981 0.848817 -1.64981 1.02814 -1.64981H8.06974Z' id='g3-61'/>
</defs>
<g id='page1'>
<use x='164.011' xlink:href='#g1-97' y='-2.3246'/>
<use x='170.156' xlink:href='#g2-51' y='-7.26078'/>
<use x='177.545' xlink:href='#g3-43' y='-2.3246'/>
<use x='189.306' xlink:href='#g1-98' y='-2.3246'/>
<use x='194.283' xlink:href='#g2-51' y='-7.26078'/>
<use x='202.336' xlink:href='#g0-54' y='-2.3246'/>
<use x='202.336' xlink:href='#g3-61' y='-2.3246'/>
<use x='214.762' xlink:href='#g1-99' y='-2.3246'/>
<use x='219.8' xlink:href='#g2-51' y='-7.26078'/>
</g>
</svg>"""

    # This is using the cache, so doesn't matter if LaTeX is found or not
    def test(self):
        math_cache = (0, 5, {
            self.tau_half_hash: (5, 0.3448408333333333, self.tau_half),
            self.fermat_hash: (5, 0.0, self.fermat),
            b'does not exist': (5, 0.0, 'something')})
        with open(os.path.join(self.path, 'xml/math.cache'), 'wb') as f:
            pickle.dump(math_cache, f)

        self.run_dox2html5(wildcard='math.xml')
        self.assertEqual(*self.actual_expected_contents('math.html'))

        # Expect that after the operation the global cache age is bumped,
        # unused entries removed and used entries age bumped as well
        with open(os.path.join(self.path, 'xml/math.cache'), 'rb') as f:
            math_cache_actual = pickle.load(f)
        math_cache_expected = (0, 6, {
            self.tau_half_hash: (6, 0.3448408333333333, self.tau_half),
            self.fermat_hash: (6, 0.0, self.fermat)})
        self.assertEqual(math_cache_actual, math_cache_expected)

    @unittest.skipUnless(shutil.which('latex'),
                         "Math rendering requires LaTeX installed")
    def test_uncached(self):
        # Write some bullshit there, which gets immediately reset
        with open(os.path.join(self.path, 'xml/math.cache'), 'wb') as f:
            pickle.dump((1337, 0, {"something different"}), f)

        self.run_dox2html5(wildcard='math-uncached.xml')

        with open(os.path.join(self.path, 'math.html')) as f:
            expected_contents = f.read().strip()
        # The file is the same expect for titles of the formulas. Replace them
        # and then compare.
        with open(os.path.join(self.path, 'html', 'math-uncached.html')) as f:
            actual_contents = f.read().strip().replace('a^3 + b^3 \\neq c^3', 'a^2 + b^2 = c^2').replace('\\frac{\\tau}{2}', '\pi')

        self.assertEqual(actual_contents, expected_contents)

        # Expect that after the operation the global cache is filled
        with open(os.path.join(self.path, 'xml/math.cache'), 'rb') as f:
            math_cache_actual = pickle.load(f)
        math_cache_expected = (0, 0, {
            sha1("$ \\frac{\\tau}{2} $".encode('utf-8')).digest():
                (0, 0.3448408333333333, self.tau_half),
            sha1("\\[ a^3 + b^3 \\neq c^3 \\]".encode('utf-8')).digest():
                (0, 0.0, self.fermat)})
        self.assertEqual(math_cache_actual, math_cache_expected)

    def test_noop(self):
        if os.path.exists(os.path.join(self.path, 'xml/math.cache')):
            shutil.rmtree(os.path.join(self.path, 'xml/math.cache'))

        # Processing without any math
        self.run_dox2html5(wildcard='indexpage.xml')

        # There should be no file generated
        self.assertFalse(os.path.exists(os.path.join(self.path, 'xml/math.cache')))

class Tagfile(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'tagfile', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class Custom(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'custom', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    @unittest.skipUnless(shutil.which('latex'),
                         "Math rendering requires LaTeX installed")
    def test_math(self):
        self.run_dox2html5(wildcard='math.xml')
        self.assertEqual(*self.actual_expected_contents('math.html'))

class ParseError(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'parse_error', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='broken.xml')

        # The index file should be generated, no abort
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'index.html')))

# JAVADOC_AUTOBRIEF should be nuked from orbit. Or implemented from scratch,
# properly.

class AutobriefHr(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'autobrief_hr', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='namespaceNamespace.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))

class AutobriefMultiline(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'autobrief_multiline', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='namespaceNamespace.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))

class AutobriefHeading(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'autobrief_heading', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='namespaceNamespace.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))

class SectionUnderscoreOne(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'section_underscore_one', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class SectionInFunction(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'section_in_function', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='File_8h.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class AnchorInBothGroupAndNamespace(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'anchor_in_both_group_and_namespace', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='namespaceFoo.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceFoo.html'))
