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

from libconfix.core.filesys.filesys import FileSystem
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
        entry=File(lines=["DIRECTORY(['lolibrary'])",
                          "DIRECTORY(['hilibrary'])",
                          "DIRECTORY(['executable'])"]))

    lolibrary_dir = sourcedir.add(
        name='lolibrary',
        entry=Directory())
    hilibrary_dir = sourcedir.add(
        name='hilibrary',
        entry=Directory())
    executable_dir = sourcedir.add(
        name='executable',
        entry=Directory())

    lolibrary_dir.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["LIBRARY(members=[H(filename='lo.h'),",
                          "                 C(filename='lo1.c'),",
                          "                 C(filename='lo2.c')],",
                          "        basename='hansi')"]))
    lolibrary_dir.add(
        name='lo.h',
        entry=File(lines=['#ifndef LO_H',
                          '#define LO_H',
                          '#ifdef __cplusplus',
                          'extern "C" {',
                          '#endif',
                          'void lo1(void);',
                          'void lo2(void);',
                          '#ifdef __cplusplus',
                          '}',
                          '#endif',
                          '#endif']))
    lolibrary_dir.add(
        name='lo1.c',
        entry=File(lines=['#include "lo.h"',
                          'void lo1(void) { lo2(); }']))
    lolibrary_dir.add(
        name='lo2.c',
        entry=File(lines=['#include "lo.h"',
                          'void lo2(void) {}']))

    hilibrary_dir.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["LIBRARY(members=[H(filename='hi.h', install=['hi']),",
                          "                 CXX(filename='hi.cc')])"]))
    hilibrary_dir.add(
        name='hi.h',
        entry=File(lines=["#ifndef HI_HI_H",
                          "#define HI_HI_H",
                          "void hi();",
                          "#endif"]))
    hilibrary_dir.add(
        name='hi.cc',
        entry=File(lines=['#include "hi.h"',
                          '#include <lo.h>',
                          'void hi() { lo1(); }']))

    executable_dir.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=["EXECUTABLE(exename='the_executable',",
                          "           center=CXX(filename='main.cc'))"]))
    executable_dir.add(
        name='main.cc',
        entry=File(lines=['#include <hi/hi.h>',
                          'int main() {',
                          '    hi();',
                          '    return 0;',
                          '}']))

    return sourcedir
    
