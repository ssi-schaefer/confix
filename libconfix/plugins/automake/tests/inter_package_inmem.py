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

from libconfix.plugins.automake.setup import AutomakeSetup
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier

import unittest

class InterPackageInMemoryTest(unittest.TestCase):

    """ This test assert fundamental behavior: relating the
    nodes. Unfortunately, the test is tied together with the C plugin
    - it should have been written using core objects. (The excuse is
    that C was long considered to be core)."""
    
    def test__repo_install(self):
        rootdir = Directory()
        rootdir.add(name=const.CONFIX2_PKG,
                    entry=File(lines=["PACKAGE_NAME('blah')",
                                      "PACKAGE_VERSION('1.2.3')"]))
        rootdir.add(name=const.CONFIX2_DIR,
                    entry=File())

        package = LocalPackage(rootdirectory=rootdir, setups=[ExplicitDirectorySetup(), AutomakeSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)

        self.failUnless('confixrepo' in rootdir_output_builder.makefile_am().install_directories())

        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(InterPackageInMemoryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
        
