# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

def make_source_tree():
    rootdirectory = Directory()

    lo_source = rootdirectory.add(
        name='lo',
        entry=Directory())
    lo_source.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("lo")',
                          'PACKAGE_VERSION("1.2.3")']))
    lo_source.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['LIBRARY(basename="lo", members=[H(filename="lo.h"), C(filename="lo.c")])']))
    lo_source.add(
        name='lo.h',
        entry=File(lines=['#ifndef LO_H',
                          '#define LO_H',
                          'void lo();',
                          '#endif']))
    lo_source.add(
        name='lo.c',
        entry=File(lines=['#include "lo.h"',
                          'void lo() {}']))

    mid_source = rootdirectory.add(
        name='mid',
        entry=Directory())
    mid_source.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("mid")',
                          'PACKAGE_VERSION("6.6.6")']))
    mid_source.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['LIBRARY(basename="mid", members=[H(filename="mid.h"), C(filename="mid.c")])']))
    mid_source.add(
        name='mid.h',
        entry=File(lines=['#ifndef MID_H',
                          '#define MID_H',
                          'void mid();',
                          '#endif']))
    mid_source.add(
        name='mid.c',
        entry=File(lines=['#include "mid.h"',
                          # spot bugs *really* early
                          '// CONFIX:REQUIRE_H("lo.h", REQUIRED)',
                          '#include <lo.h>',
                          'void mid() { lo(); }']))

    hi_source = rootdirectory.add(
        name='hi',
        entry=Directory())
    hi_source.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("hi")',
                          'PACKAGE_VERSION("2.3.4")']))
    hi_source.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['EXECUTABLE(exename="exe", center=C(filename="main.c"))']))
    hi_source.add(
        name='main.c',
        entry=File(lines=['#include <mid.h>',
                          '#include <lo.h>',
                          '#include <stdio.h>',
                          '',
                          # spot bugs *really* early
                          '// CONFIX:REQUIRE_H("mid.h", REQUIRED)',
                          '// CONFIX:REQUIRE_H("lo.h", REQUIRED)',
                          '',
                          'int main(void) {',
                          r'    printf("main was here\n");',
                          '    mid();',
                          '}']))

    return rootdirectory
