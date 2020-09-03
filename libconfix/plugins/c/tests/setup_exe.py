# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2012 Joerg Faschingbauer

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

from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.core.filesys.file import File
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.testutils import dirhier
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class ExecutableSetupTest(unittest.TestCase):

    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=[]))
        fs.rootdirectory().add(
            name='file.c',
            entry=File(lines=[]))

        # main.c has file property MAIN set to True, and hence must
        # become the center of an executable.
        main_c = fs.rootdirectory().add(
            name='main.c',
            entry=File(lines=[]))
        main_c.set_property(name='MAIN', value=True)

        # main2.c's builder (CBuilder, in this case) sees the
        # EXENAME() call in its body, and must also become the center
        # of an executable.
        main2_c = fs.rootdirectory().add(
            name='main2.c',
            entry=File(lines=['// CONFIX:EXENAME("main2")']))
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        file_h_builder = None
        file_c_builder = None
        library_builder = None
        main_builder = None
        main2_builder = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, FileBuilder):
                if b.file().name() == 'file.h' and isinstance(b, HeaderBuilder):
                    file_h_builder = b
                    pass
                elif b.file().name() == 'file.c' and isinstance(b, CBuilder):
                    file_c_builder = b
                    pass
                pass
            elif isinstance(b, LibraryBuilder):
                library_builder = b
                pass
            elif isinstance(b, ExecutableBuilder):
                if b.center().file().name() == 'main.c':
                    main_builder = b
                    continue
                if b.center().file().name() == 'main2.c':
                    main2_builder = b
                    continue
                pass
            pass
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))
        self.failUnless(isinstance(file_c_builder, CBuilder))
        self.failUnless(library_builder is None)
        self.failUnless(isinstance(main_builder, ExecutableBuilder))
        self.failUnless(isinstance(main2_builder, ExecutableBuilder))
        self.failUnlessEqual(main2_builder.exename(), 'main2')

        pass

    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExecutableSetupTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
