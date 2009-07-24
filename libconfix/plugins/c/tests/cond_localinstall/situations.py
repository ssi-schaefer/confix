# Copyright (C) 2007-2009 Joerg Faschingbauer

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

from libconfix.plugins.c.h import HeaderBuilder

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup

from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class SituationsSuite(unittest.TestSuite):

    """ Test various situations that may arise. Written for
    completeness, after implementation."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LocalInstallStillWorks('testFromRootDirectory'))
        pass
    pass

class LocalInstallStillWorks(unittest.TestCase):

    """See if a local install still works."""

    def testFromRootDirectory(self):

        """Local install from root directory (pathologic situation :-)"""
        
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        file_h = rootdirectory.add(
            name='file.h',
            entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['x', 'y'])

        user = rootdirectory.add(
            name='user',
            entry=Directory())
        user.add(
            name=const.CONFIX2_DIR,
            entry=File())
        user.add(
            name='user.cc',
            entry=File(lines=['#include <x/y/file.h>',
                              '// CONFIX:REQUIRE_H(filename="x/y/file.h", urgency=REQUIRED)']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ConfixSetup(short_libnames=False,
                                                   use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        local_visibility = file_h_builder.local_visibility()

        self.failUnless(local_visibility[0] is HeaderBuilder.LOCAL_INSTALL)
        self.failUnless(local_visibility[1] == ['x', 'y'])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(SituationsSuite())
    pass

