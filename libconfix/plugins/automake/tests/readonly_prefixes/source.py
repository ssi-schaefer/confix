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

from libconfix.core.utils import const
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory

def source_tree(testname):
    ret = Directory()

    source_lo = ret.add(
        name='lo',
        entry=Directory())
    source_lo.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("'+testname+'-lo")',
                          'PACKAGE_VERSION("1.2.3")']))
    source_lo.add(
        name=const.CONFIX2_DIR,
        entry=File())
    source_lo.add(
        name='lo.h',
        entry=File(lines=['#ifndef lo_h',
                          '#define lo_h',
                          'int the_answer();',
                          '#endif']))
    source_lo.add(
        name='lo.cc',
        entry=File(lines=['#include "lo.h"',
                          'int the_answer() { return 42; }']))

    source_hi = ret.add(
        name='hi',
        entry=Directory())
    source_hi.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("'+testname+'-hi")',
                          'PACKAGE_VERSION("1.2.3")']))
    source_hi.add(
        name=const.CONFIX2_DIR,
        entry=File())
    source_hi.add(
        name='main.cc',
        entry=File(lines=['#include <lo.h>',
                          '#include <iostream>',
                          'int main() {',
                          '  std::cout << THE_ANSWER << std::endl;',
                          '}']))
    return ret
