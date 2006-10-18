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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy.setup import DirectorySetup

import unittest

class InterfaceSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CONFIGURE_AC_ACINCLUDE_M4('test_local'))
        self.addTest(CONFIGURE_AC_ACINCLUDE_M4('test_propagate'))
        self.addTest(CONFIGURE_AC_ACINCLUDE_M4('test_defaults'))
        pass
    pass

class CONFIGURE_AC_ACINCLUDE_M4(unittest.TestCase):
    def test_local(self):

        """ We pass flags=[LOCAL] explicitly, to both ACINCLUDE_M4()
        and CONFIGURE_AC(), and check if both go into acinclude.m4 and
        configure.ac. """
        
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["CONFIGURE_AC(lines=['the_token_for_configure_ac'],",
                              "             order=AC_PROGRAMS,",
                              "             flags=[LOCAL])",
                              "ACINCLUDE_M4(lines=['the_token_for_acinclude_m4'],",
                              "             flags=[LOCAL])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.failIf(configure_ac is None)
        self.failIf(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass
    
    def test_propagate(self):

        """ We pass flags=[PROPAGATE] explicitly, to both
        ACINCLUDE_M4() and CONFIGURE_AC(), propagate it to a dependent
        node,"hi", and check if both go into acinclude.m4 and configure.ac."""

        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_SYMBOL("lo")',
                              'CONFIGURE_AC(lines=["the_token_for_configure_ac"],',
                              '             order=AC_PROGRAMS,',
                              '             flags=[PROPAGATE])',
                              'ACINCLUDE_M4(lines=["the_token_for_acinclude_m4"],',
                              '             flags=[PROPAGATE])']))
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['REQUIRE_SYMBOL("lo", URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup()])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.failIf(configure_ac is None)
        self.failIf(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_defaults(self):

        """ We do not pass any of flags, propagate it, and ..."""
        
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_SYMBOL("lo")',
                              'CONFIGURE_AC(lines=["the_token_for_configure_ac"],',
                              '             order=AC_PROGRAMS)',
                              'ACINCLUDE_M4(lines=["the_token_for_acinclude_m4"])']))
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['REQUIRE_SYMBOL("lo", URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup()])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.failIf(configure_ac is None)
        self.failIf(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass

    
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterfaceSuite())
    pass


