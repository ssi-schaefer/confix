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

from .dirstructure import DirectoryStructure

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.builder import Builder
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.automake.c.library_dependencies import LibraryDependenciesFinderSetup
from libconfix.plugins.automake.c.library_dependencies import LibraryDependenciesFinder
from libconfix.plugins.automake import makefile

from libconfix.plugins.c.executable import ExecutableBuilder

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.c import C
from libconfix.setups.automake import Automake

import unittest

class LibraryDependenciesInMemoryTest(PersistentTestCase):
    def test__plain_output(self):
        dirstructure = DirectoryStructure(path=self.rootpath())

        # kind of bootstrap packages in order (just without writing
        # anything - just boil and install)

        first_local_package = LocalPackage(rootdirectory=dirstructure.first_source(),
                                           setups=[ConfixSetup(use_libtool=False)])
        first_local_package.boil(external_nodes=[])
        first_installed_package = first_local_package.install()
        
        second_local_package = LocalPackage(rootdirectory=dirstructure.second_source(),
                                            setups=[ConfixSetup(use_libtool=False)])
        second_local_package.boil(external_nodes=first_installed_package.nodes())
        second_installed_package = second_local_package.install()

        third_local_package = LocalPackage(rootdirectory=dirstructure.third_source(),
                                           setups=[ConfixSetup(use_libtool=False)])
        third_local_package.boil(external_nodes=first_installed_package.nodes()+second_installed_package.nodes())
        third_local_package.output()
        

        # so here, finally, go the tests ...

        exedir_builder = third_local_package.rootbuilder().find_entry_builder(['exe'])
        self.assertFalse(exedir_builder is None)
        exedir_output_builder = find_automake_output_builder(exedir_builder)

        # see if we have the convenience item in makefile_am()
        convenience_deps = exedir_output_builder.makefile_am().compound_dependencies('ThirdPackage_exe_exe')
        self.assertFalse(convenience_deps is None)

        # see if the convenience item has all it should have
        self.assertTrue('$(top_builddir)/library/libThirdPackage_library.a' in convenience_deps)
        self.assertTrue('@installeddeplib_FirstPackage@' in convenience_deps)
        self.assertTrue('@installeddeplib_SecondPackage@' in convenience_deps)

        # see if it got correctly written to the Makefile.am
        real_deps = makefile.find_list(
            elements=makefile.parse_makefile(exedir_output_builder.makefile_am().lines()),
            name='ThirdPackage_exe_exe_DEPENDENCIES')
        self.assertFalse(real_deps is None)
        self.assertTrue('$(top_builddir)/library/libThirdPackage_library.a' in real_deps)
        self.assertTrue('@installeddeplib_FirstPackage@' in real_deps)
        self.assertTrue('@installeddeplib_SecondPackage@' in real_deps)
        
        pass

    def test__executable_come_and_go(self):
        class TestGuide(Builder):
            """
            Removes executable as it sees it, and checks that the
            accompanying LibraryDependenciesFinder is also removed.
            """
            EXE_NOT_SEEN = 0
            EXE_SEEN = 1
            DEPFINDER_SEEN = 2
            DEPFINDER_DISAPPEARED = 3

            def __init__(self, exename):
                Builder.__init__(self)
                self.__exename = exename
                self.__state = self.EXE_NOT_SEEN
                self.__exe = None
                self.__depfinder = None
                pass
            def locally_unique_id(self):
                return str(self.__class__)
            def state(self): return self.__state
            def enlarge(self):
                if self.__state == self.EXE_NOT_SEEN:
                    for b in self.parentbuilder().iter_builders():
                        if isinstance(b, ExecutableBuilder) and b.exename() == self.__exename:
                            self.__state = self.EXE_SEEN
                            self.__exe = b
                            self.force_enlarge()
                            return
                        pass
                    pass
                elif self.__state == self.EXE_SEEN:
                    for b in self.parentbuilder().iter_builders():
                        if isinstance(b, LibraryDependenciesFinder):
                            self.__state = self.DEPFINDER_SEEN
                            self.__depfinder = b
                            break
                        pass
                    if self.__state == self.DEPFINDER_SEEN:
                        self.parentbuilder().remove_builder(self.__exe)
                        self.__exe = None
                        pass
                    pass
                elif self.__state == self.DEPFINDER_SEEN:
                    # we removed the executable in the last
                    # round. wait for the depfinder to disappear.
                    for b in self.parentbuilder().iter_builders():
                        if b is self.__depfinder:
                            return # still there; continue
                        pass
                    else:
                        self.__state = self.DEPFINDER_DISAPPEARED
                        self.__depfinder = None
                        pass
                    pass
                else:
                    self.fail()
                    pass
                pass
            pass

        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_executable_come_and_go')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(exename='exe', center=C(filename='main.c'))"]))
        fs.rootdirectory().add(
            name='main.c',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(),
                                       C(),
                                       Automake(use_libtool=False, library_dependencies=True)])
        guide = TestGuide(exename='exe')
        package.rootbuilder().add_builder(guide)
        package.boil(external_nodes=[])
        self.assertEqual(guide.state(), guide.DEPFINDER_DISAPPEARED)
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibraryDependenciesInMemoryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
