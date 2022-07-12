# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2013 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.plugins.automake import makefile
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier

import unittest

class HeaderInstallTest(unittest.TestCase):
    def test__zerodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=[])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        # installation of file.h goes directly to $(includedir); no
        # subdir involved.
        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.assertFalse(rootdir_output_builder is None)

        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('')
        self.assertFalse(directory_definition is None)
        self.assertTrue(directory_definition.dirname() is None)
        self.assertFalse(directory_definition.files('HEADERS') is None)
        self.assertTrue(directory_definition.files('HEADERS') == ['file.h'])

        # no local install is done; user will have his includepath
        # pointed to $(srcdir)
        pass

    def test__onedeep(self):

        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        # public installation goes to $(includedir)/xxx; see if the
        # subdir stuff is handled correctly.
        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.assertFalse(rootdir_output_builder is None)
        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('publicheader_xxx')
        self.assertFalse(directory_definition is None)
        self.assertTrue(directory_definition.dirname() == '$(includedir)/xxx')
        self.assertFalse(directory_definition.files('HEADERS') is None)
        self.assertTrue(directory_definition.files('HEADERS') == ['file.h'])

        # private installation stuff.

        # all-local -> confix-install-local -> $(top_builddir)/confix-include/file.h -> $(top_builddir)/confix-include

        confix_install_local = makefile.find_rule(
            targets=['confix-install-local'],
            elements=rootdir_output_builder.makefile_am().elements())
        install_file_h = makefile.find_rule(
            targets=['$(top_builddir)/confix-include/xxx/file.h'],
            elements=rootdir_output_builder.makefile_am().elements())
        mkdir = makefile.find_rule(
            targets=['$(top_builddir)/confix-include/xxx'],
            elements=rootdir_output_builder.makefile_am().elements())
        self.assertFalse(confix_install_local is None)
        self.assertFalse(install_file_h is None)
        self.assertFalse(mkdir is None)
        self.assertTrue('confix-install-local' in rootdir_output_builder.makefile_am().all_local().prerequisites())
        self.assertTrue('$(top_builddir)/confix-include/xxx/file.h' in confix_install_local.prerequisites())

        # clean-local -> confix-clean-local -> $(top_builddir)/confix-include/file.h-clean

        confix_clean_local = makefile.find_rule(
            targets=['confix-clean-local'],
            elements=rootdir_output_builder.makefile_am().elements())
        clean_file_h = makefile.find_rule(
            targets=['$(top_builddir)/confix-include/xxx/file.h-clean'],
            elements=rootdir_output_builder.makefile_am().elements())
        self.assertFalse(confix_clean_local is None)
        self.assertFalse(clean_file_h is None)
        self.assertTrue('confix-clean-local' in rootdir_output_builder.makefile_am().clean_local().prerequisites())
        self.assertTrue('$(top_builddir)/confix-include/xxx/file.h-clean' in confix_clean_local.prerequisites())
        
        pass

    def test__twodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx/yyy'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.assertFalse(rootdir_output_builder is None)

        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('publicheader_xxxyyy')
        self.assertFalse(directory_definition is None)
        self.assertTrue(directory_definition.dirname() == '$(includedir)/xxx/yyy')
        self.assertFalse(directory_definition.files('HEADERS') is None)
        self.assertTrue(directory_definition.files('HEADERS') == ['file.h'])
        pass
        
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(HeaderInstallTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
