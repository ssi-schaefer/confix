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

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.core.utils import const
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class BasicLocalInstallSuite(unittest.TestSuite):

    """ Tests that have been used to implement the feature."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicLocalInstallTest('test'))
        pass
    pass

class BasicLocalInstallTest(unittest.TestCase):

    """ Two modules lo and hi where hi.h includes lo.h. Both header
    files are made visible with no prefix directory. These files
    should not be locally installed into $(prefix)/confix_include. A
    user module should get an appropriate build info that contains the
    relative source paths of each of the files, and should compose its
    include path appropriately."""

    def test(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        lodir = rootdirectory.add(
            name='lo',
            entry=Directory())
        lodir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lodir.add(
            name='lo.h',
            entry=File())

        hidir = rootdirectory.add(
            name='hi',
            entry=Directory())
        hidir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hidir.add(
            name='hi.h',
            entry=File(lines=['#include <lo.h>']))

        user = rootdirectory.add(
            name='user',
            entry=Directory())
        user.add(
            name=const.CONFIX2_DIR,
            entry=File())
        user.add(
            name='user.c',
            entry=File(lines=['#include <hi.h>']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=[])

        user_c_builder = package.rootbuilder().find_entry_builder(['user', 'user.c'])
        self.failIf(user_c_builder is None)

        hi_pos = lo_pos = None
        for i in range(len(user_c_builder.native_local_include_dirs())):
            if user_c_builder.native_local_include_dirs()[i] == ['hi']:
                self.failUnless(hi_pos is None)
                hi_pos = i
                continue
            if user_c_builder.native_local_include_dirs()[i] == ['lo']:
                self.failUnless(lo_pos is None)
                lo_pos = i
                continue
            pass

        self.failIf(hi_pos is None)
        self.failIf(lo_pos is None)
        self.failIf(hi_pos > lo_pos)
        
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BasicLocalInstallSuite())
    pass
