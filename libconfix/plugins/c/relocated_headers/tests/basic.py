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

from libconfix.plugins.c.relocated_headers.setup import RelocatedHeadersSetup

from libconfix.plugins.c.creator import CreatorSetup
from libconfix.plugins.c.clusterer import CClustererSetup
from libconfix.plugins.c.explicit_install import ExplicitInstallerSetup

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup

import unittest

class BasicSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicTest('test'))
        self.addTest(RelocatedHeaderRequiresRelocatedHeaderTest('test'))
        pass
    pass

class BasicTest(unittest.TestCase):

    # We have two modules, a and b. These modules have non-local
    # headers in include, a_interface.h and b_interface.h.

    #   package
    #   +--  include
    #   |   +-- a_interface.h
    #   |   +-- b_interface.h
    #   +-- a
    #   |   +-- a.cc
    #   +-- b
    #   |   +-- b.cc
    #   +-- c
    #   |   +-- c.h
    #   |   +-- c.cc
    #   +-- exe
    #       +-- main.cc

    # That is, whenever somebody includes one of these headers
    # (a_interface.h, for example), he must not get a dependency on
    # include (he won't get a's library there), but rather a
    # dependency on a (which in turn has a dependency on include, of
    # course, so the user will point the include path at wherever
    # a_interface.h is visible).

    # To make the long story short: the dependency graph that results
    # when exe includes a_interface.h and b_interface.h will look as
    # follows. (c comes in just to make sure everything else is still
    # right :-)

    #                 a ---- include
    #               /   \  /
    #   exe (user) /     \/
    #              \     /\
    #               \   /  \
    #                 b ---- c

    def test(self):
        fs = FileSystem(path=['dont\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        include = fs.rootdirectory().add(
            name='include',
            entry=Directory())
        include.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('interface')",
                              "RELOCATE_HEADER(filename='a_interface.h',",
                              "                directory=['a'])",
                              "RELOCATE_HEADER(filename='b_interface.h',",
                              "                directory=['b'])"]))
        include.add(
            name='a_interface.h',
            entry=File(lines=['#ifndef A_INTERFACE_H',
                              '#define A_INTERFACE_H',
                              'void a(void);'
                              '#endif']))
        include.add(
            name='b_interface.h',
            entry=File(lines=['#ifndef B_INTERFACE_H',
                              '#define B_INTERFACE_H',
                              'void b(void);'
                              '#endif']))

        a = fs.rootdirectory().add(
            name='a',
            entry=Directory())
        a.add(
            name=const.CONFIX2_DIR,
            entry=File())
        a.add(
            name='a.cc',
            entry=File(lines=["#include <interface/a.h>",
                              "#include <c.h>",
                              "// CONFIX:REQUIRE_H('interface/a_interface.h', REQUIRED)",
                              "// CONFIX:REQUIRE_H('c.h', REQUIRED)",
                              "void a(void) {",
                              "    c();",
                              "}"]))

        b = fs.rootdirectory().add(
            name='b',
            entry=Directory())
        b.add(
            name=const.CONFIX2_DIR,
            entry=File())
        b.add(
            name='b.cc',
            entry=File(lines=["#include <interface/b_interface.h>",
                              "#include <c.h>",
                              "// CONFIX:REQUIRE_H('interface/b_interface.h', REQUIRED)",
                              "// CONFIX:REQUIRE_H('c.h', REQUIRED)",
                              "void b(void) {",
                              "    c();",
                              "}"]))

        c = fs.rootdirectory().add(
            name='c',
            entry=Directory())
        c.add(
            name=const.CONFIX2_DIR,
            entry=File())
        c.add(
            name='c.h',
            entry=File(lines=["#ifndef C_H",
                              "#define C_H",
                              "void c(void);",
                              "#endif"]))
        c.add(
            name='c.cc',
            entry=File(lines=["#include <c.h>",
                              "void c(void) {}"]))

        exe = fs.rootdirectory().add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File())
        exe.add(
            name='main.cc',
            entry=File(lines=["#include <interface/a_interface.h>",
                              "#include <interface/b_interface.h>",
                              "// CONFIX:REQUIRE_H('interface/a_interface.h', REQUIRED)",
                              "// CONFIX:REQUIRE_H('interface/b_interface.h', REQUIRED)",
                              "int main(void) {",
                              "    a();",
                              "    b();",
                              "}"]))

        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[
            # recognize subdirectories
            DefaultDirectorySetup(),
            # create C and Header builders
            CreatorSetup(),
            # cluster them together in libraries and executables, and
            # don't care about libtool and names.
            CClustererSetup(short_libnames=False, use_libtool=False),
            # install headers as everybody likes (not).
            ExplicitInstallerSetup(),
            # And finally: make the relocated header stuff work.
            RelocatedHeadersSetup()])

        package.boil(external_nodes=[])

        include_builder = package.rootbuilder().find_entry_builder(['include'])
        a_builder = package.rootbuilder().find_entry_builder(['a'])
        b_builder = package.rootbuilder().find_entry_builder(['b'])
        c_builder = package.rootbuilder().find_entry_builder(['c'])
        exe_builder = package.rootbuilder().find_entry_builder(['exe'])

        self.failIf(include_builder is None)
        self.failIf(a_builder is None)
        self.failIf(b_builder is None)
        self.failIf(c_builder is None)
        self.failIf(exe_builder is None)

        # verify dependency graph

        # these two are crucial because they come from the relocated
        # headers a_interface.h and b_interface.h, respectively.
        self.failUnless(a_builder in package.digraph().successors(exe_builder))
        self.failUnless(b_builder in package.digraph().successors(exe_builder))

        # a and b depend on include ...
        self.failUnless(include_builder in package.digraph().successors(a_builder))
        self.failUnless(include_builder in package.digraph().successors(b_builder))

        # ... and on c, of course.
        self.failUnless(c_builder in package.digraph().successors(a_builder))
        self.failUnless(c_builder in package.digraph().successors(b_builder))

        pass
    pass

class RelocatedHeaderRequiresRelocatedHeaderTest(unittest.TestCase):

    #   package
    #   +-- include
    #   |   +-- a.h  #include <b.h>
    #   |   +-- b.h
    #   +-- src
    #   |   +-- a.cc #include <a.h>
    #       +-- b.cc #include <b.h>

    # both headers a.h and b.h are relocated to src. a.h requires
    # b.h. this test makes sure that there is no cycle like follows,
    
    # src  --------------------------> include ---------------------------------> src
    #      [relocation of a.h and b.h]         [a.h requires b.h which is in src]

    def test(self):
        fs = FileSystem(path=['dont\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        include = fs.rootdirectory().add(
            name='include',
            entry=Directory())
        include.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["RELOCATE_HEADER(filename='a.h',",
                              "                directory=['src'])",
                              "RELOCATE_HEADER(filename='b.h',",
                              "                directory=['src'])"]))
        include.add(
            name='a.h',
            entry=File(lines=['#ifndef A_H',
                              '#define A_H',
                              '// CONFIX:REQUIRE_H("b.h", REQUIRED)',
                              '#include "b.h"',
                              'void a(void);'
                              '#endif']))
        include.add(
            name='b.h',
            entry=File(lines=['#ifndef B_H',
                              '#define B_H',
                              'void b(void);'
                              '#endif']))

        src = fs.rootdirectory().add(
            name='src',
            entry=Directory())
        src.add(
            name=const.CONFIX2_DIR,
            entry=File())
        src.add(
            name='a.c',
            entry=File(lines=['#include <a.h>',
                              '// CONFIX:REQUIRE_H("a.h", REQUIRED)',
                              'void a(void) {}']))
        src.add(
            name='b.c',
            entry=File(lines=['#include <b.h>',
                              '// CONFIX:REQUIRE_H("b.h", REQUIRED)',
                              'void b(void) {}']))

        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[
            # recognize subdirectories
            DefaultDirectorySetup(),
            # create C and Header builders
            CreatorSetup(),
            # cluster them together in libraries and executables, and
            # don't care about libtool and names.
            CClustererSetup(short_libnames=False, use_libtool=False),
            # install headers as everybody likes (not).
            ExplicitInstallerSetup(),
            # And finally: make the relocated header stuff work.
            RelocatedHeadersSetup()])

        package.boil(external_nodes=[])

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BasicSuite())
    pass

