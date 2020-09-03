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

from libconfix.plugins.automake import bootstrap

from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import sys
import unittest

class AutoConfArchiveTest(PersistentTestCase):

    """ See if we set the aclocal path to the autoconf archive."""
    
    def test(self):
        fs = FileSystem(path=self.rootpath())
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('AutoConfArchiveTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["CONFIGURE_AC(lines=['AC_CXX_NAMESPACES'],",
                              "             order=AC_PROGRAMS)"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(packageroot=fs.rootdirectory().abspath(),
                            path=None,
                            use_kde_hack=False,
                            argv0=sys.argv[0])
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(AutoConfArchiveTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

