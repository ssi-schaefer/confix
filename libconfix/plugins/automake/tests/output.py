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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.automake.setup import AutomakeSetup

from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.library import LibraryBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import dirhier

import unittest

class AutomakeOutputTest(unittest.TestCase):
    def setUp(self):
        self.__fs = dirhier.packageroot()
        subdir1 = self.__fs.rootdirectory().add(name='subdir1', entry=Directory())
        subdir1.add(name=const.CONFIX2_DIR,
                    entry=File(lines=['PROVIDE_SYMBOL("subdir1")']))
        
        subdir2 = self.__fs.rootdirectory().add(name='subdir2', entry=Directory())
        subdir2.add(name=const.CONFIX2_DIR,
                    entry=File(lines=['PROVIDE_SYMBOL("subdir2")',
                                      'REQUIRE_SYMBOL("subdir1")']))
        subdir3 = self.__fs.rootdirectory().add(name='subdir3', entry=Directory())
        subdir3.add(name=const.CONFIX2_DIR,
                    entry=File(lines=['REQUIRE_SYMBOL("subdir2")']))
        
        self.__package = LocalPackage(rootdirectory=self.__fs.rootdirectory(),
                                     setups=[ImplicitDirectorySetup(), AutomakeSetup(use_libtool=False)])
        self.__package.boil(external_nodes=[])
        self.__package.output()

        self.__subdir1_builder = self.__package.rootbuilder().find_entry_builder(['subdir1'])
        self.__subdir2_builder = self.__package.rootbuilder().find_entry_builder(['subdir2'])
        self.__subdir3_builder = self.__package.rootbuilder().find_entry_builder(['subdir3'])
        assert self.__subdir1_builder
        assert self.__subdir2_builder
        assert self.__subdir3_builder

        pass

    def tearDown(self):
        self.__fs = None
        self.__package = None
        pass

    def test__subdirs(self):
        rootdir_automake_builder = find_automake_output_builder(self.__package.rootbuilder())

        self.assertNotEqual(self.__fs.rootdirectory().find(['Makefile.am']), None)
        self.assertTrue(const.CONFIX2_DIR in rootdir_automake_builder.makefile_am().extra_dist())
        self.assertTrue(const.CONFIX2_PKG in rootdir_automake_builder.makefile_am().extra_dist())

        # relative positions of subdir1, subdir2, subdir3 in toplevel
        # Makefile.am's SUBDIRS must be subdir1 < subdir2 <
        # subdir3. (we cannot count on absolute positions because the
        # topological range of '.' is random - '.' has no
        # dependencies. (same hold for aux.))

        aux = dot = subdir1 = subdir2 = subdir3 = None

        for i in range(len(rootdir_automake_builder.makefile_am().subdirs())):
            if rootdir_automake_builder.makefile_am().subdirs()[i] == 'confix-admin/automake':
                self.assertTrue(aux is None)
                aux = i
            elif rootdir_automake_builder.makefile_am().subdirs()[i] == 'subdir1':
                self.assertTrue(subdir1 is None)
                subdir1 = i
            elif rootdir_automake_builder.makefile_am().subdirs()[i] == 'subdir2':
                self.assertTrue(subdir2 is None)
                subdir2 = i
            elif rootdir_automake_builder.makefile_am().subdirs()[i] == 'subdir3':
                self.assertTrue(subdir3 is None)
                subdir3 = i
                pass
            elif rootdir_automake_builder.makefile_am().subdirs()[i] == '.':
                self.assertTrue(dot is None)
                dot = i
                pass
            pass

        # see if there is anything in there at all
        self.assertNotEqual(len(self.__fs.rootdirectory().find(['Makefile.am']).lines()), 0)

        self.assertFalse(aux is None)
        self.assertFalse(dot is None)
        self.assertFalse(subdir1 is None)
        self.assertFalse(subdir2 is None)
        self.assertFalse(subdir3 is None)

        self.assertTrue(subdir1 < subdir2 < subdir3)

        # see if we have our subdir's Makefiles registered for output
        self.assertTrue('Makefile' in rootdir_automake_builder.configure_ac().ac_config_files() or \
                        './Makefile' in rootdir_automake_builder.configure_ac().ac_config_files())
        self.assertTrue('subdir1/Makefile' in rootdir_automake_builder.configure_ac().ac_config_files())
        self.assertTrue('subdir2/Makefile' in rootdir_automake_builder.configure_ac().ac_config_files())
        self.assertTrue('subdir3/Makefile' in rootdir_automake_builder.configure_ac().ac_config_files())
        
        pass

    def test__configure_ac(self):
        rootdir_automake_builder = find_automake_output_builder(self.__package.rootbuilder())

        self.assertNotEqual(self.__fs.rootdirectory().find(['configure.ac']), None)
        self.assertTrue('config.h' in rootdir_automake_builder.configure_ac().ac_config_headers())
        self.assertFalse(rootdir_automake_builder.configure_ac().packagename() is None)
        self.assertFalse(rootdir_automake_builder.configure_ac().packageversion() is None)
        pass

    def test__auxdir(self):
        rootdir_automake_builder = find_automake_output_builder(self.__package.rootbuilder())

        auxdir = self.__package.rootbuilder().directory().find(['confix-admin', 'automake'])
        self.assertFalse(auxdir is None)
        mf_am = auxdir.find(['Makefile.am'])
        self.assertFalse(mf_am is None)
        self.assertEqual(rootdir_automake_builder.configure_ac().ac_config_aux_dir(), 'confix-admin/automake')
        self.assertTrue('confix-admin/automake/Makefile' in rootdir_automake_builder.configure_ac().ac_config_files())
        pass

    def test__toplevel_makefile_am(self):
        rootdir_automake_builder = find_automake_output_builder(self.__package.rootbuilder())

        self.assertTrue('1.9' in rootdir_automake_builder.makefile_am().automake_options())
        self.assertTrue('dist-bzip2' in rootdir_automake_builder.makefile_am().automake_options())
        self.assertTrue('dist-shar' not in rootdir_automake_builder.makefile_am().automake_options())
        self.assertTrue('dist-zip' in rootdir_automake_builder.makefile_am().automake_options())
        self.assertTrue(const.CONFIX2_DIR in rootdir_automake_builder.makefile_am().extra_dist())
        self.assertTrue(const.CONFIX2_PKG in rootdir_automake_builder.makefile_am().extra_dist())
        self.assertTrue(self.__package.name()+'.repo' in rootdir_automake_builder.makefile_am().extra_dist())
        self.assertTrue('Makefile.in' in rootdir_automake_builder.makefile_am().maintainercleanfiles())
        self.assertTrue('Makefile.am' in rootdir_automake_builder.makefile_am().maintainercleanfiles())
        pass

    def test__subdir1_makefile_am(self):
        subdir1_automake_builder = find_automake_output_builder(
            self.__package.rootbuilder().find_entry_builder(['subdir1']))

        self.assertNotEqual(self.__fs.rootdirectory().find(['subdir1', 'Makefile.am']), None)
        self.assertTrue(const.CONFIX2_DIR in subdir1_automake_builder.makefile_am().extra_dist())
        self.assertTrue('Makefile.in' in subdir1_automake_builder.makefile_am().maintainercleanfiles())
        self.assertTrue('Makefile.am' in subdir1_automake_builder.makefile_am().maintainercleanfiles())
        pass

    def test__subdir2_makefile_am(self):
        subdir2_automake_builder = find_automake_output_builder(
            self.__package.rootbuilder().find_entry_builder(['subdir2']))

        self.assertNotEqual(self.__fs.rootdirectory().find(['subdir2', 'Makefile.am']), None)
        self.assertTrue(const.CONFIX2_DIR in subdir2_automake_builder.makefile_am().extra_dist())
        self.assertTrue('Makefile.in' in subdir2_automake_builder.makefile_am().maintainercleanfiles())
        self.assertTrue('Makefile.am' in subdir2_automake_builder.makefile_am().maintainercleanfiles())
        pass

    def test__subdir3_makefile_am(self):
        subdir3_automake_builder = find_automake_output_builder(
            self.__package.rootbuilder().find_entry_builder(['subdir3']))

        self.assertNotEqual(self.__fs.rootdirectory().find(['subdir3', 'Makefile.am']), None)
        self.assertTrue(const.CONFIX2_DIR in subdir3_automake_builder.makefile_am().extra_dist())
        self.assertTrue('Makefile.in' in subdir3_automake_builder.makefile_am().maintainercleanfiles())
        self.assertTrue('Makefile.am' in subdir3_automake_builder.makefile_am().maintainercleanfiles())
        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(AutomakeOutputTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
