# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.plugins.c.dependency import Require_CInclude
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.installed_package import InstalledPackage
from libconfix.core.machinery.installed_node import InstalledNode
from libconfix.core.machinery.require import Require
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class Bug1713807(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(Bug1713807Test('test'))
        pass
    pass

class Bug1713807Test(unittest.TestCase):
    """ [ 1713807 ] Full graph computed even for unused installed packages """
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo.add(
            name='lo.h',
            entry=File())

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi.add(
            name='hi.c',
            entry=File(lines=['#include <lo.h>']))

        installed_package = InstalledPackage(name='blah-package',
                                             version='1.2.3',
                                             nodes=[InstalledNode(name=['blah'],
                                                                  provides=[],
                                                                  requires=[Require_CInclude(filename='notexist.h',
                                                                                             found_in=[],
                                                                                             urgency=Require.URGENCY_ERROR)],
                                                                  buildinfos=[])])

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=installed_package.nodes())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(Bug1713807())
    pass

