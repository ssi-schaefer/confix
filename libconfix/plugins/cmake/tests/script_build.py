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

from libconfix.plugins.cmake import commands

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest
import sys
import os

class ScriptBuildTest(PersistentTestCase):
    def test__basic(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=[
                "from libconfix.setups.boilerplate import Boilerplate",
                "from libconfix.setups.cmake import CMake",
                "from libconfix.setups.script import Script",
                "PACKAGE_NAME('cmake-script-build')",
                "PACKAGE_VERSION('1.2.3')",
                "SETUP([Boilerplate(), CMake(library_dependencies=False), Script()])",
                ]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                'ADD_SCRIPT(filename="script")'
                ]))
        source.add(
            name='script',
            entry=File())

        package = LocalPackage(rootdirectory=source, setups=None)
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['install'])

        stat = os.stat(os.sep.join(install.abspath() + ['bin', 'script']))
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ScriptBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
