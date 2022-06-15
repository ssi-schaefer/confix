# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from libconfix.setups.explicit_setup import ExplicitSetup

from libconfix.testutils.persistent import PersistentTestCase
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class MakeTest(PersistentTestCase):
    def test__CALL_MAKE_AND_RESCAN(self):
        fs = FileSystem(self.rootpath())
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CALL_MAKE_AND_RESCAN()']))
        fs.rootdirectory().add(
            name='Makefile',
            entry=File(lines=['all:',
                              '\t@touch the_file',
                              '']))

        fs.sync() # the make program needs something to hold on to
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])

        package.boil(external_nodes=[])

        self.assertTrue(fs.rootdirectory().find(['the_file']))
        pass

    def test__CALL_MAKE_AND_RESCAN_SYNC(self):

        # CALL_MAKE_AND_RESCAN_SYNC() is supposed to make files that
        # were created by the call to make immediately available to the
        # further code in Confix2.dir. We check this in the Confix2.dir,
        # and if we found the created file, we set a file property on
        # the Makefile which we evaluate later in the test routine. (We
        # could raise an exception in Confix2.dir as well, but that
        # makes the test result less obvious.

        fs = FileSystem(self.rootpath())
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        makefile = fs.rootdirectory().add(
            name='Makefile',
            entry=File(lines=['all:',
                              '\t@touch the_file_created_by_make']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CALL_MAKE_AND_RESCAN_SYNC()',
                              'if FIND_ENTRY("the_file_created_by_make"):',
                              '    SET_FILE_PROPERTY("Makefile", "saw_the_file_created_by_make", True)',
                              ]))

        fs.sync() # the make program needs something to hold on to
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])

        package.boil(external_nodes=[])

        self.assertTrue(makefile.get_property('saw_the_file_created_by_make') is True)
        pass
    pass        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(MakeTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
