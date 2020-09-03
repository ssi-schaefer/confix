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

from dirstructure import DirectoryStructure

from libconfix.plugins.automake import bootstrap, configure, make, makefile

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.repo import AutomakePackageRepository
from libconfix.core.filesys import scan
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils.persistent import PersistentTestCase

import itertools
import unittest
import sys
import os

class LibraryDependenciesBuildTest(PersistentTestCase):
    def test__basic(self):
        dirstructure = DirectoryStructure(path=self.rootpath())

        # bootstrap&&configure&&build&&install packages in order
        first_local_package = LocalPackage(rootdirectory=dirstructure.first_source(),
                                           setups=[ConfixSetup(use_libtool=False)])
        first_local_package.boil(external_nodes=[])
        first_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.first_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.first_source().abspath(),
            builddir=dirstructure.first_build().abspath(),
            prefix=dirstructure.first_install().abspath(),
            readonly_prefixes=None)
        make.make(
            builddir=dirstructure.first_build().abspath(),
            args=['install'])


        second_local_package = LocalPackage(rootdirectory=dirstructure.second_source(),
                                            setups=[ConfixSetup(use_libtool=False)])
        second_local_package.boil(external_nodes=AutomakePackageRepository(prefix=dirstructure.first_install().abspath()).iter_nodes())
        second_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.second_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.second_source().abspath(),
            builddir=dirstructure.second_build().abspath(),
            prefix=dirstructure.second_install().abspath(),
            readonly_prefixes=[dirstructure.first_install().abspath()])
        make.make(
            builddir=dirstructure.second_build().abspath(),
            args=['install'])


        third_local_package = LocalPackage(rootdirectory=dirstructure.third_source(),
                                           setups=[ConfixSetup(use_libtool=False)])
        third_local_package.boil(external_nodes=itertools.chain(
            AutomakePackageRepository(prefix=dirstructure.first_install().abspath()).iter_nodes(),
            AutomakePackageRepository(prefix=dirstructure.second_install().abspath()).iter_nodes()))
        third_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.third_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.third_source().abspath(),
            builddir=dirstructure.third_build().abspath(),
            prefix=None,
            readonly_prefixes=[dirstructure.first_install().abspath(),
                               dirstructure.second_install().abspath()])
        make.make(
            builddir=dirstructure.third_build().abspath(),
            args=None)

        # so here, finally, go the tests.

        fs = scan.scan_filesystem(path=self.rootpath())

        first_library = fs.rootdirectory().find(dirstructure.first_install().relpath(self.rootpath())+['lib', 'libFirstPackage.a'])
        second_library = fs.rootdirectory().find(dirstructure.second_install().relpath(self.rootpath())+['lib', 'libSecondPackage.a'])
        third_library = fs.rootdirectory().find(dirstructure.third_build().relpath(self.rootpath())+['library', 'libThirdPackage_library.a'])
        third_exe_Makefile = fs.rootdirectory().find(dirstructure.third_build().relpath(self.rootpath())+['exe', 'Makefile'])
        self.failIf(first_library is None)
        self.failIf(second_library is None)
        self.failIf(third_library is None)
        self.failIf(third_exe_Makefile is None)

        elements = makefile.parse_makefile(third_exe_Makefile.lines())
        deps = makefile.find_list(name='ThirdPackage_exe_exe_DEPENDENCIES',
                                  elements=elements)
        self.failIf(deps is None)

        self.failUnless(os.sep.join(first_library.abspath()) in deps)
        self.failUnless(os.sep.join(second_library.abspath()) in deps)
        self.failUnless('$(top_builddir)/library/libThirdPackage_library.a' in deps)
        
        pass

    def test__implicit_with_explicit_libname(self):
        fs = FileSystem(path=self.rootpath())

        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_implicit_with_explicit_libname')",
                              "PACKAGE_VERSION('1.2.3')",

                              "from libconfix.setups.boilerplate import AutoBoilerplate",
                              "from libconfix.setups.c import AutoC",
                              "from libconfix.setups.automake import Automake",

                              "SETUP([AutoBoilerplate(),",
                              "       AutoC(),",
                              "       Automake(use_libtool=False, library_dependencies=True)])"
                              ]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        library = source.add(
            name='library',
            entry=Directory())
        library.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('my-library')",
                              "LIBNAME('my-library')"]))
        library.add(
            name='library.c',
            entry=File(lines=['void f() {}']))

        exe = source.add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('my-library', URGENCY_ERROR)"]))
        exe.add(
            name='main.c',
            entry=File(lines=['int main(void) { return 0; }']))

        package = LocalPackage(rootdirectory=source, setups=None)
        package.boil(external_nodes=[])
        package.output()

        exe_Makefile_am = source.find(['exe', 'Makefile.am'])
        elements = makefile.parse_makefile(exe_Makefile_am.lines())
        deps = makefile.find_list(name='test_implicit_with_explicit_libname_exe_main_DEPENDENCIES',
                                  elements=elements)
        self.failUnless('$(top_builddir)/library/libmy-library.a' in deps)

        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None,
            readonly_prefixes=[]
            )
        make.make(
            builddir=build.abspath(),
            args=[])

        self.failUnless(os.path.isfile(
            os.sep.join(itertools.chain(build.abspath(), ['exe', 'test_implicit_with_explicit_libname_exe_main']))))
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibraryDependenciesBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
