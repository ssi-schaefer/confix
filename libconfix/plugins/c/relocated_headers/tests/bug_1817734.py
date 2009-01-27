# Copyright (C) 2007-2008 Joerg Faschingbauer

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.plugins.c.dependency import Require_CInclude
from libconfix.setups.explicit_setup import ExplicitSetup

import unittest

class Bug_1817734(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(Bug_1817734_Test('test'))
        pass
    pass

class Bug_1817734_Test(unittest.TestCase):
    def test(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['include'])",
                              "DIRECTORY(['source'])"]))

        include = rootdirectory.add(
            name='include',
            entry=Directory())
        include.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='file.h', relocate_to=['source'])"]))
        include.add(
            name='file.h',
            entry=File(lines=['#include <another_file.h>']))

        source = rootdirectory.add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[]))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        include_builder = package.rootbuilder().find_entry_builder(path=['include'])
        source_builder = package.rootbuilder().find_entry_builder(path=['source'])

        self.failIf(include_builder is None)
        self.failIf(source_builder is None)

        # the include directory must not require anything - the only
        # builder was relocated to the source directory.
        for r in include_builder.requires():
            self.failIf(isinstance(r, Require_CInclude), r)
            pass

        # whereas the source directory must require the header that
        # file.h includes.
        for r in source_builder.requires():
            if isinstance(r, Require_CInclude) and r.filename() == 'another_file.h':
                break
            pass
        else:
            self.fail()
            pass
            
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(Bug_1817734())
    pass

