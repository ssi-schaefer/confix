# Copyright (C) 2006 Joerg Faschingbauer

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

from dirstructure import DirectoryStructure

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.setup import DirectorySetup

from libconfix.testutils import find
from libconfix.testutils import makefileparser
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.library_dependencies import LibraryDependenciesFinderSetup

import unittest

class LibraryDependenciesInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryDependenciesInMemoryTest('test'))
        pass
    pass

class LibraryDependenciesInMemoryTest(PersistentTestCase):
    def test(self):
        dirstructure = DirectoryStructure(path=self.rootpath())

        # kind of bootstrap packages in order (just without writing
        # anything - just boil and install)

        first_local_package = LocalPackage(rootdirectory=dirstructure.first_source(),
                                           setups=[DefaultCSetup(short_libnames=False,
                                                                 use_libtool=False)])
        first_local_package.boil(external_nodes=[])
        first_installed_package = first_local_package.install()
        
        second_local_package = LocalPackage(rootdirectory=dirstructure.second_source(),
                                            setups=[DefaultCSetup(short_libnames=False,
                                                                  use_libtool=False)])
        second_local_package.boil(external_nodes=first_installed_package.nodes())
        second_installed_package = second_local_package.install()

        third_local_package = LocalPackage(rootdirectory=dirstructure.third_source(),
                                           setups=[DirectorySetup(),
                                                   DefaultCSetup(short_libnames=False,
                                                                 use_libtool=False),
                                                   LibraryDependenciesFinderSetup()])
        third_local_package.boil(external_nodes=first_installed_package.nodes()+second_installed_package.nodes())
        third_local_package.output()
        

        # so here, finally, go the tests ...

        exe_builder = find.find_entrybuilder(rootbuilder=third_local_package.rootbuilder(),
                                                   path=['exe'])
        self.failIf(exe_builder is None)

        # see if we have the convenience item in makefile_am()
        convenience_deps = exe_builder.makefile_am().compound_dependencies('ThirdPackage_exe_exe')
        self.failIf(convenience_deps is None)

        # see if the convenience item has all it should have
        self.failUnless('$(top_builddir)/library/libThirdPackage_library.a' in convenience_deps)
        self.failUnless('@installeddeplib_FirstPackage@' in convenience_deps)
        self.failUnless('@installeddeplib_SecondPackage@' in convenience_deps)

        # see if it got correctly written to the Makefile.am
        real_deps = makefileparser.find_list(
            elements=makefileparser.parse_makefile(exe_builder.makefile_am().lines()),
            name='ThirdPackage_exe_exe_DEPENDENCIES')
        self.failIf(real_deps is None)
        self.failUnless('$(top_builddir)/library/libThirdPackage_library.a' in real_deps)
        self.failUnless('@installeddeplib_FirstPackage@' in real_deps)
        self.failUnless('@installeddeplib_SecondPackage@' in real_deps)
        
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryDependenciesInMemorySuite())
    pass
