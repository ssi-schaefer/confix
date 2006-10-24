# Copyright (C) 2002-2006 Salomon Automation
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

import unittest

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import find


class GraphInstallerSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(GraphInstallerTest('test_basic'))
        pass
    pass

class GraphInstallerTest(unittest.TestCase):
    def test_basic(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["from libconfix.plugins.c.setup import GraphSetup",
                              "PACKAGE_NAME('GraphInstallerTest')",
                              "PACKAGE_VERSION('1.2.3')",
                              "SETUPS([GraphSetup(use_libtool=False, short_libnames=False)])"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLED_HEADER_ENTRYPOINT(filename='entry.h', dir=['some', 'subdir'])"]))

        fs.rootdirectory().add(
            name='entry.h',
            entry=File(lines=["#include <level1a.h>",
                              "#include <level1b.h>"]))
        fs.rootdirectory().add(
            name='level1a.h',
            entry=File(lines=["#include <level2.h>"]))
        fs.rootdirectory().add(
            name='level1b.h',
            entry=File(lines=["#include <level2.h>"]))
        fs.rootdirectory().add(
            name='level2.h',
            entry=File())
        fs.rootdirectory().add(
            name='intern.h',
            entry=File())

        package=LocalPackage(rootdirectory=fs.rootdirectory(),
                             # we set setups form inside the package
                             # def.file.
                             setups=[])
        package.boil(external_nodes=[])

        installer = find.find_graph_installer(rootbuilder=package.rootbuilder(), path=[])
        self.failIf(installer is None)
        self.failUnlessEqual(installer.installpath_of_headerfile('entry.h'), ['some', 'subdir'])
        self.failUnlessEqual(installer.installpath_of_headerfile('level1a.h'), ['some', 'subdir'])
        self.failUnlessEqual(installer.installpath_of_headerfile('level1b.h'), ['some', 'subdir'])
        self.failUnlessEqual(installer.installpath_of_headerfile('level2.h'), ['some', 'subdir'])
        self.failIfEqual(installer.installpath_of_headerfile('intern.h'), ['some', 'subdir'])

        pass


if __name__ == '__main__':
    unittest.TextTestRunner().run(GraphInstallerSuite())
    pass

