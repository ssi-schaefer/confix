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
    rootdirectory.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("intra-package")',
                          'PACKAGE_VERSION("1.2.3")']))
    rootdirectory.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['DIRECTORY(["lo"])',
                          'DIRECTORY(["hi"])',
                          'DIRECTORY(["exe"])']))
    lo = rootdirectory.add(
        name='lo',
        entry=Directory())
    lo.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['LIBRARY(basename="lo",',
                          '        members=[H(filename="lo1.h"),',
                          '                 C(filename="lo1.c"),'
                          '                 H(filename="lo2.h"),'
                          '                 C(filename="lo2.c")])']))
    lo.add(
        name='lo1.h',
        entry=File(lines=['#ifndef LO1_h',
                          '#define LO1_h',
                          'extern void lo1();',
                          '#endif']))
    lo.add(
        name='lo1.c',
        entry=File(lines=['#include "lo1.h"',
                          'void lo1() {}']))
    lo.add(
        name='lo2.h',
        entry=File(lines=['#ifndef LO1_h',
                          '#define LO1_h',
                          'extern void lo2();',
                          '#endif']))
    lo.add(
        name='lo2.c',
        entry=File(lines=['#include "lo2.h"',
                          'void lo2() {}']))

    hi = rootdirectory.add(
        name='hi',
        entry=Directory())
    hi.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['LIBRARY(basename="hi",',
                          '        members=[H(filename="hi1.h"),',
                          '                 C(filename="hi1.c"),'
                          '                 H(filename="hi2.h"),'
                          '                 C(filename="hi2.c")])']))
    hi.add(
        name='hi1.h',
        entry=File(lines=['#ifndef HI1_H',
                          '#define HI1_H',
                          'extern void hi1();',
                          '#endif']))
    hi.add(
        name='hi1.c',
        entry=File(lines=['#include "hi1.h"',
                          '#include <lo1.h>',
                          'void hi1() { lo1(); }']))
    hi.add(
        name='hi2.h',
        entry=File(lines=['#ifndef HI2_H',
                          '#define HI2_H',
                          'extern void hi2();',
                          '#endif']))
    hi.add(
        name='hi2.c',
        entry=File(lines=['#include "hi2.h"',
                          '#include <lo2.h>',
                          'void hi2() { lo2(); }']))

    exe = rootdirectory.add(
        name='exe',
        entry=Directory())
    exe.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['EXECUTABLE(exename="exe",',
                          '           center=C(filename="main.c"),',
                          '           members=[H(filename="require_lo.h"),',
                          '                    C(filename="require_lo.c"),',
                          '                    H(filename="require_hi.h"),',
                          '                    C(filename="require_hi.c")])']))
    exe.add(
        name='require_lo.h',
        entry=File(lines=['#ifndef REQUIRE_LO_H',
                          '#define REQUIRE_LO_H',
                          'extern void require_lo1();',
                          'extern void require_lo2();',
                          '#endif']))
    exe.add(
        name='require_lo.c',
        entry=File(lines=['#include "require_lo.h"',
                          '#include <lo1.h>',
                          '#include <lo2.h>',
                          'void require_lo1() { lo1(); }',
                          'void require_lo2() { lo2(); }']))
    exe.add(
        name='require_hi.h',
        entry=File(lines=['#ifndef REQUIRE_HI_H',
                          '#define REQUIRE_HI_H',
                          'extern void require_hi1();',
                          'extern void require_hi2();',
                          '#endif']))
    exe.add(
        name='require_hi.c',
        entry=File(lines=['#include "require_hi.h"',
                          '#include <hi1.h>',
                          '#include <hi2.h>',
                          'void require_hi1() { hi1(); }',
                          'void require_hi2() { hi2(); }']))
    exe.add(
        name='main.c',
        entry=File(lines=['#include "require_lo.h"',
                          '#include "require_hi.h"',
                          'int main() {',
                          '    require_lo1();',
                          '    require_lo2();',
                          '    require_hi1();',
                          '    require_hi2();',
                          '}']))

    return rootdirectory
