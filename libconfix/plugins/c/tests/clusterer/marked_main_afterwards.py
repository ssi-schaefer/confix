# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.clusterer import CClusterer
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.namefinder import LongNameFinder
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.provide_symbol import Provide_Symbol
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class MarkedMainAfterwardsSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(MarkedMainAfterwardsTest('test_interface'))
        self.addTest(MarkedMainAfterwardsTest('test_explicit'))
        pass
    pass

class MarkedMainAfterwardsTest(unittest.TestCase):

    # this is the reason why I implement that feature - marking a C
    # file executable after it has been added to another executable -
    # at all. Builder.configure() is called explicitly, somewhere
    # after the ctor, but before Builder.enlarge() is called. This
    # leads to unconfigured Builder objects seen by the
    # Clusterer. Unconfigured means: they do not yet know whether they
    # carry main() or not. They are not configured before they are
    # seen by the Clusterer because they have just been created. Only
    # before the next round they will be configured, evaluate their
    # interface code, and they will know that they carry the
    # executable mark.

    def test_interface(self):
        fs = FileSystem(path=['dont', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("MarkedMainAfterwardsTest.test_interface")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        # main1.c has file property MAIN set to True, and hence must
        # become the center of an executable.
        main1_c = fs.rootdirectory().add(
            name='main1.c',
            entry=File(lines=[]))
        main1_c.set_property(name='MAIN', value=True)

        # main2.c's builder (CBuilder, in this case) sees the
        # EXENAME() call in its body, and must also become the center
        # of an executable.
        main2_c = fs.rootdirectory().add(
            name='main2.c',
            entry=File(lines=['// CONFIX:EXENAME("main2")']))
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False, use_libtool=False)])

        package.boil(external_nodes=[])

        main1_exe_builder = None
        main2_exe_builder = None

        for b in package.rootbuilder().iter_builders():
            if not isinstance(b, ExecutableBuilder):
                continue
            if b.center().file().name() == 'main1.c':
                main1_exe_builder = b
                continue
            if b.center().file().name() == 'main2.c':
                main2_exe_builder = b
                continue
            pass

        self.failIf(main1_exe_builder is None)
        self.failIf(main2_exe_builder is None)

        self.failUnlessEqual(len(main1_exe_builder.members()), 1)
        self.failUnlessEqual(len(main2_exe_builder.members()), 1)

        pass

    # this one ismore complicated, but actually more to the point of
    # testing the CClusterer's exact behavior. we add a specialized
    # governor to the builders that drives the actions and observes
    # and verifies that the actions are correct.

    def test_explicit(self):

        fs = FileSystem(path=['dont', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("MarkedMainAfterwardsTest.test_explicit")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        main1_c = fs.rootdirectory().add(
            name='main1.c',
            entry=File())

        main2_c = fs.rootdirectory().add(
            name='main2.c',
            entry=File())
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[])
        package.rootbuilder().add_builder(CBuilder(file=main1_c))
        package.rootbuilder().add_builder(CBuilder(file=main2_c))
        package.rootbuilder().add_builder(CClusterer(namefinder=LongNameFinder()))

        # this is our special kind of builder. he does the whole
        # checking work.
        package.rootbuilder().add_builder(TestHelper())

        try:
            package.boil(external_nodes=[])
        except TestHelper.Error, e:
            self.fail(str(e))
            pass
        pass
    pass

class TestHelper(Builder):

    # in every round, do something depending on the state of the
    # constellation. the following is a linear sequence of the states
    # that this builder takes in order. we can sit in most of the
    # states for more than one round, because of the non-deterministic
    # ordering of fellow builders.

    # completely new; we expect two normal C builder objects (and
    # maybe a library, but this dependes on the internal ordering of
    # fellow builders - we see a library only if the clusterer is our
    # predecessor and has had the chance to create the library before
    # we could take a look).
    INIT = 0

    # we have seen the library.
    LIBRARY_SEEN = 1

    # we have flagged the first C builder as "main". we sit in this
    # state until we see an executable. when we see it, we verify that
    # there is no library anymore.
    FIRST_C_FLAGGED_AS_MAIN = 2

    # after we have flagged the first executable, we finally saw it.
    FIRST_EXECUTABLE_SEEN = 3

    # we have flagged the remaining C builder as "main", and are
    # waiting to see the effect - our second executable.
    SECOND_C_FLAGGED_AS_MAIN = 4
    
    SECOND_EXECUTABLE_SEEN = 5

    class Error:
        def __init__(self, msg):
            self.__msg = msg
            pass
        def __str__(self): return self.__msg
        pass

    def __init__(self):
        Builder.__init__(self)
        self.__round = 0
        self.__state = TestHelper.INIT
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def enlarge(self):
        super(TestHelper, self).enlarge()

        self.__round += 1
        if self.__round == 100:
            raise TestHelper.Error(str(self.__round)+' rounds; stopping')

        if self.__state == TestHelper.INIT:
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, LibraryBuilder):
                    self.__state = TestHelper.LIBRARY_SEEN
                    break
                pass
            self.__force_next_round()
            return

        if self.__state == TestHelper.LIBRARY_SEEN:
            # set one C builder as "main"
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, CBuilder) and b.file().name() == 'main1.c':
                    if b.is_main():
                        raise TestHelper.Error('main1.c is marked main')
                    b.file().set_property('MAIN', True)
                    break
                pass
            else:
                raise TestHelper.Error('main1.c not found')
                pass
            self.__state = TestHelper.FIRST_C_FLAGGED_AS_MAIN
            self.__force_next_round()
            return

        if self.__state == TestHelper.FIRST_C_FLAGGED_AS_MAIN:
            # verify that we see *one* executable.
            exe = None
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, ExecutableBuilder):
                    if exe:
                        raise TestHelper.Error('two exes found; marked only one so far')
                    exe = b
                    pass
                pass

            if exe is None:
                # still no executable; wait until next round.
                self.__force_next_round()
                return

            if exe.center().file().name() != 'main1.c':
                raise TestHelper.Error('found '+exe.center().file().name()+' and not main1.c')

            # the exe must have two members, and the library must have
            # been dissolved.
            if len(exe.members()) != 2:
                raise TestHelper.Error('main1.c does not have 2 members')
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, LibraryBuilder):
                    raise TestHelper.Error('library not dissolved')
                pass
            self.__state = TestHelper.FIRST_EXECUTABLE_SEEN
            self.__force_next_round()
            return

        if self.__state == TestHelper.FIRST_EXECUTABLE_SEEN:
            # mark next C builder as main
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, CBuilder) and not b.is_main():
                    b.file().set_property('MAIN', True)
                    break
                pass
            else:
                raise TestHelper.Error('no second non-main C builder found')
            self.__state = TestHelper.SECOND_C_FLAGGED_AS_MAIN
            self.__force_next_round()
            return

        if self.__state == TestHelper.SECOND_C_FLAGGED_AS_MAIN:
            # wait for two executables with one member each. no
            # library of course.
            exe1 = exe2 = None
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, ExecutableBuilder):
                    if b.center().file().name() == 'main1.c':
                        exe1 = b
                    elif b.center().file().name() == 'main2.c':
                        exe2 = b
                        pass
                    else:
                        raise TestHelper.Error('not-asked-for executable '+b.center().file().name())
                    pass
                pass
            # we have verified that before, and there is no reason for
            # main1 to go away.
            if not exe1:
                raise TestHelper.Error('main1.c executable disappeared')

            if not exe2:
                # main2 executable still not seen; wait for next
                # round.
                self.__force_next_round()
                return

            # final verification: exe1 has lost its second member,
            # main2.c; both executables have only one member, namely
            # their centers.
            if len(exe1.members()) != 1:
                raise TestHelper.Error('main1.c executable does not have exactly one member')
            if len(exe2.members()) != 1:
                raise TestHelper.Error('main2.c executable does not have exactly one member')
            self.__state = TestHelper.SECOND_EXECUTABLE_SEEN
            return

        if self.__state == TestHelper.SECOND_EXECUTABLE_SEEN:
            # nothing more to do; sit and wait for termination.
            return

        raise TestHelper.Error('invalid state '+str(self.__state))
                
    def __force_next_round(self):
        self.add_provide(Provide_Symbol(str(self.__round)))
        pass
        
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MarkedMainAfterwardsSuite())
    pass

            
