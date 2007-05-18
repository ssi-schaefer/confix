# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

def make_package_source(package_name):
    sourcedir = Directory()
    sourcedir.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=["PACKAGE_NAME('"+package_name+"')",
                          "PACKAGE_VERSION('1.2.3')"]))
    sourcedir.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["DIRECTORY(['include'])",
                          "DIRECTORY(['lib_implementation'])",
                          "DIRECTORY(['exe'])"]))

    include = sourcedir.add(
        name='include',
        entry=Directory())
    include.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["H(filename='lib.h', relocate_to=['lib_implementation'])"]))
    include.add(
        name='lib.h',
        entry=File(lines=['#ifndef LIB_H',
                          '#define LIB_H',
                          'void lib();',
                          '#endif']))

    lo_implementation = sourcedir.add(
        name='lib_implementation',
        entry=Directory())
    lo_implementation.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["CXX(filename='lib.cc')"]))
    lo_implementation.add(
        name='lib.cc',
        entry=File(lines=["#include <lib.h>",
                          "void lib() {}"]))

    exe = sourcedir.add(
        name='exe',
        entry=Directory())
    exe.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["CXX(filename='main.cc')"]))
    exe.add(
        name='main.cc',
        entry=File(lines=["#include <lib.h>",
                          "int main() {",
                          "    lib();",
                          "}"]))
    return sourcedir
    

