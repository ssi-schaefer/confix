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

from libconfix.plugins.cmake import commands

from libconfix.plugins.plainfile.tests.package import make_package

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.testutils.persistent import PersistentTestCase
from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.plainfile import Plainfile
from libconfix.setups.cmake import CMake

import os
import sys
import unittest

class PlainfileBuildTest(PersistentTestCase):
    def test__basic(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=make_package())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), Plainfile(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        commands.cmake(packageroot=source.abspath(),
                       builddir=build.abspath(),
                       args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(builddir=build.abspath(), args=['install'])
        
        self.assertTrue(os.path.isfile(os.sep.join(
            self.rootpath()+['install', 'share', 'subdir', 'data', 'plainfile_data'])))
        self.assertTrue(os.path.isfile(os.sep.join(
            self.rootpath()+['install', 'subdir', 'prefix', 'plainfile_prefix'])))

        pass
    pass        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(PlainfileBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
