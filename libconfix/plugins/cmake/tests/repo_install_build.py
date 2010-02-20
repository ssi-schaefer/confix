# Copyright (C) 2009-2010 Joerg Faschingbauer

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

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake import commands

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.cmake import CMake

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest
import os

class RepoInstallBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RepoInstallTest('test'))
        pass
    pass

class RepoInstallTest(PersistentTestCase):
    """
    The repo file can be installed before anything else is installed.

    This is not a feature that is heavily used, but Salomon likes it.
    """
    
    def test(self):
        fs = FileSystem(path=self.rootpath())
        
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("Repo-Install")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())

        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+os.sep.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['repo-install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['share', 'confix2', 'repo', 'Repo-Install.repo']))
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(RepoInstallBuildSuite())
    pass
