# Copyright (C) 2013 Joerg Faschingbauer

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.plugins.automake.pkg_config.setup import PkgConfigSetup
from libconfix.plugins.automake.out_automake import find_automake_output_builder

import unittest

class BasicTest(unittest.TestCase):

    def test(self):
        root = Directory()
        root.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        root.add(
            name=const.CONFIX2_DIR,
            entry=File())

        ext_lib = root.add(
            name='ext-lib',
            entry=Directory())
        ext_lib.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_H("ext_lib.h")',
                              'PKG_CONFIG_LIBRARY(packagename="ext_lib")']))

        main = root.add(
            name='main',
            entry=Directory())
        main.add(
            name='main.cc',
            entry=File(lines=['#include <ext_lib.h>',
                              '// CONFIX:REQUIRE_H("ext_lib.h", REQUIRED)',
                              '// CONFIX:EXENAME("the_exe")',
                              'int main() { return 0; }']))
        main.add(
            name=const.CONFIX2_DIR,
            entry=File())

        package = LocalPackage(rootdirectory=root,
                               setups=[ConfixSetup(use_libtool=False),
                                       PkgConfigSetup()])
        package.boil(external_nodes=[])
        package.output()

        maindir_builder = package.rootbuilder().find_entry_builder(['main'])
        self.assertFalse(maindir_builder is None)

        maindir_output_builder = find_automake_output_builder(maindir_builder)
        self.assertFalse(maindir_output_builder is None)
        
        self.assertTrue('$(ext_lib_PKG_CONFIG_CFLAGS)' in maindir_output_builder.makefile_am().am_cflags())
        self.assertTrue('$(ext_lib_PKG_CONFIG_CFLAGS)' in maindir_output_builder.makefile_am().am_cxxflags())

        main_ldadd = maindir_output_builder.makefile_am().compound_ldadd(compound_name='the_exe')
        self.assertFalse(main_ldadd is None)
        
        self.assertTrue('$(ext_lib_PKG_CONFIG_LIBS)' in main_ldadd)
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(BasicTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

