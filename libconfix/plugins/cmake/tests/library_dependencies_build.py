# Copyright (C) 2009-2013 Joerg Faschingbauer

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

from . import inter_package

from libconfix.plugins.cmake import commands
from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.library_dependencies import LibraryDependenciesSetup
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.repo import AutomakeCascadedPackageRepository
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import unittest
import os
import time

class LibraryDependenciesTest(PersistentTestCase):

    # inside a package, modifying a library means that an executable
    # that uses it is rebuilt.
    def test_intra_package(self):
        fs = FileSystem(path=self.rootpath())

        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibraryDependencies-Intra-Package')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['lib'])",
                              "DIRECTORY(['exe'])"]))

        lib = source.add(
            name='lib',
            entry=Directory())
        lib.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(basename='lib', members=[H(filename='lib.h'), C(filename='lib.c')])"]))
        lib.add(
            name='lib.h',
            entry=File(lines=['#ifndef lib_h',
                              '#define lib_h',
                              'void lib();',
                              '#endif']))
        lib.add(
            name='lib.c',
            entry=File(lines=['#include "lib.h"',
                              'void lib() {}']))

        exe = source.add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['EXECUTABLE(exename="exe", center=C(filename="main.c"))']))
        exe.add(
            name='main.c',
            entry=File(lines=['#include <lib.h>',
                              '// CONFIX:REQUIRE_H("lib.h", URGENCY_ERROR)',
                              'int main(void) {',
                              '    lib(); ',
                              '    return 0;',
                              '}']))

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(),
                                       ExplicitCSetup(),
                                       CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()
        
        commands.cmake(packageroot=source.abspath(),
                       builddir=build.abspath(),
                       args=[])
        commands.make(builddir=build.abspath(), args=[])

        # wait a bit and then touch liblo.a. (is there a better way
        # than sleeping?)
        time.sleep(1)
        lib_library = os.sep.join(build.abspath()+['lib', 'liblib.a'])
        os.utime(lib_library, None)
        lib_library_stat = os.stat(lib_library)

        # exe is rebuilt as it depends on liblib.a
        if True:
            commands.make(builddir=build.abspath(), args=[])
            self.assertTrue(os.stat(os.sep.join(build.abspath()+['exe', 'exe'])).st_mtime >= lib_library_stat.st_mtime)
            pass

        pass

    def test_inter_package(self):
        fs = FileSystem(path=self.rootpath())

        source = fs.rootdirectory().add(
            name='source',
            entry=inter_package.make_source_tree())
        lo_source = source.find(['lo'])
        mid_source = source.find(['mid'])
        hi_source = source.find(['hi'])
        
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        lo_build = build.add(
            name='lo',
            entry=Directory())
        mid_build = build.add(
            name='mid',
            entry=Directory())
        hi_build = build.add(
            name='hi',
            entry=Directory())

        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        # build and install lo
        if True:
            lo_package = LocalPackage(rootdirectory=lo_source,
                                      setups=[ExplicitDirectorySetup(),
                                              ExplicitCSetup(),
                                              CMakeSetup()])
            lo_package.boil(external_nodes=[])
            lo_package.output()

            fs.sync()

            commands.cmake(packageroot=lo_source.abspath(),
                           builddir=lo_build.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
            commands.make(builddir=lo_build.abspath(), args=['install'])
            pass

        # build and install mid
        if True:
            repo = AutomakeCascadedPackageRepository(
                prefix=install.abspath(),
                readonly_prefixes=[])

            mid_package = LocalPackage(rootdirectory=mid_source,
                                       setups=[ExplicitDirectorySetup(),
                                               ExplicitCSetup(),
                                               CMakeSetup()])
            mid_package.boil(external_nodes=repo.iter_nodes())
            mid_package.output()

            fs.sync()

            commands.cmake(packageroot=mid_source.abspath(),
                           builddir=mid_build.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
            commands.make(builddir=mid_build.abspath(), args=['install'])
            pass

        # build and install hi. declare that I want library
        # dependencies.
        if True:
            repo = AutomakeCascadedPackageRepository(
                prefix=install.abspath(),
                readonly_prefixes=[])
            
            hi_package = LocalPackage(rootdirectory=hi_source,
                                      setups=[ExplicitDirectorySetup(),
                                              ExplicitCSetup(),
                                              CMakeSetup(),
                                              LibraryDependenciesSetup()])
            hi_package.boil(external_nodes=repo.iter_nodes())
            hi_package.output()

            fs.sync()
            
            commands.cmake(packageroot=hi_source.abspath(),
                           builddir=hi_build.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
            commands.make(builddir=hi_build.abspath(), args=['install'])
            pass

        # wait a bit and then touch liblo.a. (is there a better way
        # than sleeping?)
        time.sleep(1)
        lo_lib = os.sep.join(install.abspath()+['lib', 'liblo.a'])
        os.utime(lo_lib, None)
        lo_stat = os.stat(lo_lib)

        # libmid.a is not rebuilt.
        if True:
            commands.make(builddir=mid_build.abspath(), args=['install'])
            self.assertFalse(os.stat(os.sep.join(install.abspath()+['lib', 'libmid.a'])).st_mtime >= lo_stat.st_mtime)
            pass

        # exe is rebuilt as it has liblo.a linked in.
        if True:
            commands.make(builddir=hi_build.abspath(), args=['install'])
            self.assertTrue(os.stat(os.sep.join(install.abspath()+['bin', 'exe'])).st_mtime >= lo_stat.st_mtime)
            pass

        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibraryDependenciesTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
