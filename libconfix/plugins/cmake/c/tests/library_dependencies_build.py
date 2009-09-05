# Copyright (C) 2009 Joerg Faschingbauer

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

import inter_package

from libconfix.plugins.cmake import commands
from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.c.library_dependencies import LibraryDependenciesSetup
from libconfix.plugins.automake.repo_automake import AutomakeCascadedPackageRepository
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory

import unittest
import os
import time

class LibraryDependenciesBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryDependenciesTest('test'))
        pass
    pass

class LibraryDependenciesTest(PersistentTestCase):
    def test(self):
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
            mid_package.boil(external_nodes=repo.nodes())
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
            hi_package.boil(external_nodes=repo.nodes())
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
            self.failIf(os.stat(os.sep.join(install.abspath()+['lib', 'libmid.a'])).st_mtime >= lo_stat.st_mtime)
            pass

        # exe is rebuilt as it has liblo.a linked in.
        if True:
            commands.make(builddir=hi_build.abspath(), args=['install'])
            self.failUnless(os.stat(os.sep.join(install.abspath()+['bin', 'exe'])).st_mtime >= lo_stat.st_mtime)
            pass

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryDependenciesBuildSuite())
    pass
