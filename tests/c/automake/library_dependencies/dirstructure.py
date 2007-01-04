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
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

class DirectoryStructure:
    def __init__(self, path):
        self.__root = FileSystem(path=path)
        self.__source = self.__root.rootdirectory().add(
            name='source',
            entry=Directory())
        self.__build = self.__root.rootdirectory().add(
            name='build',
            entry=Directory())
        self.__install = self.__root.rootdirectory().add(
            name='install',
            entry=Directory())

        self.__first_source = self.__source.add(
            name='first',
            entry=Directory())
        self.__first_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('FirstPackage')",
                              "PACKAGE_VERSION('1.2.3')"]))
        self.__first_source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        self.__first_source.add(
            name='first.h',
            entry=File(lines=['void first();']))
        self.__first_source.add(
            name='first.c',
            entry=File(lines=['void first() {}']))

        self.__second_source = self.__source.add(
            name='second',
            entry=Directory())
        self.__second_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('SecondPackage')",
                              "PACKAGE_VERSION('1.2.3')"]))
        self.__second_source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        self.__second_source.add(
            name='second.h',
            entry=File(lines=['void second();']))
        self.__second_source.add(
            name='second.c',
            entry=File(lines=['#include "second.h"',
                              '// CONFIX:REQUIRE_H("first.h", REQUIRED)',
                              '#include <first.h>',
                              'void second() {first();}']))

        self.__third_source = self.__source.add(
            name='third',
            entry=Directory())
        self.__third_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ThirdPackage')",
                              "PACKAGE_VERSION('1.2.3')"]))
        self.__third_source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        self.__third_library=self.__third_source.add(
            name='library',
            entry=Directory())
        self.__third_library.add(
            name=const.CONFIX2_DIR,
            entry=File())
        self.__third_library.add(
            name='third.h',
            entry=File(lines=['void third();']))
        self.__third_library.add(
            name='third.c',
            entry=File(lines=['#include "third.h"',
                              '// CONFIX:REQUIRE_H("second.h", REQUIRED)',
                              '#include <second.h>',
                              'void third() {second();}']))
        
        self.__third_exe = self.__third_source.add(
            name='exe',
            entry=Directory())
        self.__third_exe.add(
            name=const.CONFIX2_DIR,
            entry=File())
        self.__third_exe.add(
            name='exe.c',
            entry=File(lines=['// CONFIX:REQUIRE_H("third.h", REQUIRED)',
                              '#include <third.h>',
                              'int main() {third();}']))
        # add a second executable to see if two library dependency
        # calculator objects behave well if they live in the same
        # directory.
        self.__third_exe.add(
            name='exe2.c',
            entry=File(lines=['int main() {return 0;}']))

        self.__first_build = self.__build.add(
            name='first',
            entry=Directory())
        self.__second_build = self.__build.add(
            name='second',
            entry=Directory())
        self.__third_build = self.__build.add(
            name='third',
            entry=Directory())
        
        self.__first_install = self.__install.add(
            name='first',
            entry=Directory())
        self.__second_install = self.__install.add(
            name='second',
            entry=Directory())
        self.__third_install = self.__install.add(
            name='third',
            entry=Directory())
        
        pass

    def first_source(self): return self.__first_source
    def first_build(self): return self.__first_build
    def first_install(self): return self.__first_install
    def second_source(self): return self.__second_source
    def second_build(self): return self.__second_build
    def second_install(self): return self.__second_install
    def third_source(self): return self.__third_source
    def third_build(self): return self.__third_build
    def third_install(self): return self.__third_install

    def sync(self):
        self.__root.sync()
        pass

    pass
