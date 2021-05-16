#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020 Vladimír Vondruš <mosra@centrum.cz>
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
import unittest

from distutils.version import LooseVersion

from . import IntegrationTestCase, doxygen_version

class Listing(IntegrationTestCase):
    def test_index_pages(self):
        self.run_doxygen(wildcard='index.xml', index_pages=['annotated', 'namespaces', 'pages'])
        self.assertEqual(*self.actual_expected_contents('annotated.html'))
        self.assertEqual(*self.actual_expected_contents('namespaces.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))

    def test_index_pages_custom_expand_level(self):
        self.run_doxygen(wildcard='index.xml', index_pages=['files'])
        self.assertEqual(*self.actual_expected_contents('files.html'))

    def test_dir(self):
        self.run_doxygen(wildcard='dir_*.xml')
        self.assertEqual(*self.actual_expected_contents('dir_4b0d5f8864bf89936129251a2d32609b.html'))
        self.assertEqual(*self.actual_expected_contents('dir_bbe5918fe090eee9db2d9952314b6754.html'))

    def test_file(self):
        self.run_doxygen(wildcard='*_8h.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(*self.actual_expected_contents('Class_8h.html'))

    def test_namespace(self):
        self.run_doxygen(wildcard='namespaceRoot_1_1Directory.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceRoot_1_1Directory.html'))

    def test_namespace_empty(self):
        self.run_doxygen(wildcard='namespaceAnother.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceAnother.html'))

    def test_class(self):
        self.run_doxygen(wildcard='classRoot_1_1Directory_1_1Sub_1_1Class.xml')
        self.assertEqual(*self.actual_expected_contents('classRoot_1_1Directory_1_1Sub_1_1Class.html'))

    def test_page_no_toc(self):
        self.run_doxygen(wildcard='page-no-toc.xml')
        self.assertEqual(*self.actual_expected_contents('page-no-toc.html'))

class Detailed(IntegrationTestCase):
    def test_namespace(self):
        self.run_doxygen(wildcard='namespaceNamee.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceNamee.html'))

    def test_class_template(self):
        self.run_doxygen(wildcard='structTemplate.xml')
        self.assertEqual(*self.actual_expected_contents('structTemplate.html'))

    def test_class_template_specialized(self):
        self.run_doxygen(wildcard='structTemplate_3_01void_01_4.xml')
        self.assertEqual(*self.actual_expected_contents('structTemplate_3_01void_01_4.html'))

    def test_class_template_warnings(self):
        self.run_doxygen(wildcard='structTemplateWarning.xml')
        self.assertEqual(*self.actual_expected_contents('structTemplateWarning.html'))

    def test_function(self):
        self.run_doxygen(wildcard='namespaceFoo.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceFoo.html'))

    def test_enum(self):
        self.run_doxygen(wildcard='namespaceEno.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceEno.html'))

    def test_function_enum_warnings(self):
        self.run_doxygen(wildcard='namespaceWarning.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceWarning.html'))

    def test_typedef(self):
        self.run_doxygen(wildcard='namespaceType.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceType.html'))

    def test_var(self):
        self.run_doxygen(wildcard='namespaceVar.xml')
        self.assertEqual(*self.actual_expected_contents('namespaceVar.html'))

    def test_define(self):
        self.run_doxygen(wildcard='File_8h.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class Ignored(IntegrationTestCase):
    def test(self):
        self.run_doxygen(index_pages=[], wildcard='*.xml')

        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'classA.html')))

        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'classA_1_1PrivateClass.html')))
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'File_8cpp.html')))
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'input_8h.html')))
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'namespace_0D0.html')))

    @unittest.expectedFailure
    def test_empty_class_doc_not_generated(self):
        # This needs to be generated in order to be compatible with tag files
        self.run_doxygen(index_pages=[], wildcard='classBrief.xml')
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'classBrief.html')))

class Modules(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('group__group.html'))
        self.assertEqual(*self.actual_expected_contents('group__group2.html'))
        self.assertEqual(*self.actual_expected_contents('group__subgroup.html'))
        self.assertEqual(*self.actual_expected_contents('modules.html'))

class ModulesInNamespace(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('group__group1.html'))
        self.assertEqual(*self.actual_expected_contents('group__group2.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))
        self.assertEqual(*self.actual_expected_contents('file3_8h.html'))

class Deprecated(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        # Test that the [deprecated] label is in all places where it should ne

        # Class tree
        self.assertEqual(*self.actual_expected_contents('annotated.html'))

        # Member namespace and define listing
        self.assertEqual(*self.actual_expected_contents('DeprecatedFile_8h.html'))

        # Member file and directory listing
        self.assertEqual(*self.actual_expected_contents('dir_da5033def2d0db76e9883b31b76b3d0c.html'))

        # File and directory tree
        self.assertEqual(*self.actual_expected_contents('files.html'))

        # Member module listing
        self.assertEqual(*self.actual_expected_contents('group__group.html'))

        # Module tree
        self.assertEqual(*self.actual_expected_contents('modules.html'))

        # Member namespace, class, function, variable, typedef and enum listing
        self.assertEqual(*self.actual_expected_contents('namespaceDeprecatedNamespace.html'))

        # Namespace tree
        self.assertEqual(*self.actual_expected_contents('namespaces.html'))

        # Page tree
        self.assertEqual(*self.actual_expected_contents('pages.html'))

        # Base and derived class listing
        self.assertEqual(*self.actual_expected_contents('structDeprecatedNamespace_1_1BaseDeprecatedClass.html'))
        self.assertEqual(*self.actual_expected_contents('structDeprecatedNamespace_1_1DeprecatedClass.html'))

class NamespaceMembersInFileScope(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='namespaceNamespace.xml')

        # The namespace should have the detailed docs
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.14"),
                         "https://github.com/doxygen/doxygen/pull/653")
    def test_file(self):
        self.run_doxygen(wildcard='File_8h.xml')

        # The file should have just links to detailed docs
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class NamespaceMembersInFileScopeDefineBaseUrl(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.14"),
                         "https://github.com/doxygen/doxygen/pull/653")
    def test(self):
        self.run_doxygen(wildcard='File_8h.xml')

        # The file should have just links to detailed docs
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class FilenameCase(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # Verify that all filenames are "converted" to lowercase and the links
        # and page tree work properly as well
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))
        self.assertEqual(*self.actual_expected_contents('_u_p_p_e_r_c_a_s_e.html'))
        self.assertEqual(*self.actual_expected_contents('class_u_p_p_e_r_c_l_a_s_s.html'))

class CrazyTemplateParams(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # The file should have the whole template argument as a type
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class Includes(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # The Contained namespace should have just the global include, the
        # Spread just the local includes, the class a global include and the
        # group, even though in a single file, should have local includes; and
        # the SpreadClass struct is forward-declared in another file, which
        # triggers a silly Doxygen bug so it has per-member includes also
        self.assertEqual(*self.actual_expected_contents('namespaceContained.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceSpread.html'))
        self.assertEqual(*self.actual_expected_contents('classClass.html'))
        self.assertEqual(*self.actual_expected_contents('group__group.html'))
        self.assertEqual(*self.actual_expected_contents('structSpreadClass.html'))

        # These two should all have local includes because otherwise it gets
        # misleading; the Empty namespace a global one
        self.assertEqual(*self.actual_expected_contents('namespaceContainsNamespace.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceContainsNamespace_1_1ContainsClass.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceEmpty.html'))

class IncludesDisabled(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # No include information as SHOW_INCLUDE_FILES is disabled globally,
        # and no useless detailed sections either
        self.assertEqual(*self.actual_expected_contents('namespaceContained.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceSpread.html'))
        self.assertEqual(*self.actual_expected_contents('classClass.html'))
        self.assertEqual(*self.actual_expected_contents('group__group.html'))
        self.assertEqual(*self.actual_expected_contents('structSpreadClass.html'))

class IncludesUndocumentedFiles(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # The files are not documented, so there should be no include
        # information and no useless detailed sections either -- practically
        # the same output as when SHOW_INCLUDE_FILES is disabled globally
        self.assertEqual(*self.actual_expected_contents('namespaceContained.html', '../compound_includes_disabled/namespaceContained.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceSpread.html', '../compound_includes_disabled/namespaceSpread.html'))
        self.assertEqual(*self.actual_expected_contents('classClass.html', '../compound_includes_disabled/classClass.html'))
        self.assertEqual(*self.actual_expected_contents('group__group.html', '../compound_includes_disabled/group__group.html'))
        self.assertEqual(*self.actual_expected_contents('structSpreadClass.html', '../compound_includes_disabled/structSpreadClass.html'))

class IncludesTemplated(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # All entries should have the includes next to the template
        self.assertEqual(*self.actual_expected_contents('namespaceSpread.html'))
        self.assertEqual(*self.actual_expected_contents('structStruct.html'))

class BaseDerivedInRootNamespace(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # Shouldn't crash or anything
        self.assertEqual(*self.actual_expected_contents('structNamespace_1_1BothBaseAndDerivedInRootNamespace.html'))

class Since(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # Verify all entries and details get the Since badge with a link to
        # changelog. Not class/namespace/file/dir entries yet because we don't
        # propagate those right now.
        self.assertEqual(*self.actual_expected_contents('dir_4b0d5f8864bf89936129251a2d32609b.html'))
        self.assertEqual(*self.actual_expected_contents('Class_8h.html'))
        self.assertEqual(*self.actual_expected_contents('group__group.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceFoo.html'))
        self.assertEqual(*self.actual_expected_contents('classFoo_1_1Class.html'))
        self.assertEqual(*self.actual_expected_contents('structFoo_1_1Subclass.html'))
        self.assertEqual(*self.actual_expected_contents('a.html'))

        # And these should have an extended deprecation badge
        self.assertEqual(*self.actual_expected_contents('dir_73d1500434dee6f1c83b12ee799c54af.html'))
        self.assertEqual(*self.actual_expected_contents('DeprecatedClass_8h.html'))
        self.assertEqual(*self.actual_expected_contents('group__deprecated-group.html'))
        self.assertEqual(*self.actual_expected_contents('namespaceDeprecatedFoo.html'))
        self.assertEqual(*self.actual_expected_contents('classDeprecatedFoo_1_1DeprecatedClass.html'))
        self.assertEqual(*self.actual_expected_contents('structDeprecatedFoo_1_1DeprecatedSubclass.html'))
        self.assertEqual(*self.actual_expected_contents('deprecated-a.html'))

        # The listings should have both
        self.assertEqual(*self.actual_expected_contents('annotated.html'))
        self.assertEqual(*self.actual_expected_contents('files.html'))
        self.assertEqual(*self.actual_expected_contents('modules.html'))
        self.assertEqual(*self.actual_expected_contents('namespaces.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class ExceptionReference(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class BaseTemplateClasses(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('structNamespace_1_1MyClass.html'))

class InlineNamespace(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        with open(os.path.join(self.path, 'xml/namespaceFoo_1_1Bar.xml')) as f:
            if 'kind="namespace" inline="yes"' not in f.read():
                self.skipTest("Doxygen doesn't support inline namespaces here")

        self.assertEqual(*self.actual_expected_contents('namespaceFoo_1_1Bar.html'))
        self.assertEqual(*self.actual_expected_contents('annotated.html'))
        self.assertEqual(*self.actual_expected_contents('namespaces.html'))
