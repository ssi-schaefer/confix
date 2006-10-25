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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

class BoilSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ConfigureCalledOnlyOnce('test'))
        pass
    pass

class ConfigureCalledOnlyOnce(unittest.TestCase):
    class ConfigureWatcher(Builder):
        def __init__(self):
            Builder.__init__(self)
            self.__configure_called = False
            pass
        def configure(self):
            if self.__configure_called:
                raise "already called"
            super(ConfigureCalledOnlyOnce.ConfigureWatcher, self).configure()
            self.__configure_called = True
            pass
        pass
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ConfigureCalledOnlyOnce')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        package.rootbuilder().add_builder(self.ConfigureWatcher())
        package.boil(external_nodes=[])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BoilSuite())
    pass
