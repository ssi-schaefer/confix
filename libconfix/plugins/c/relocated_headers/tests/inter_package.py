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

from libconfix.core.utils import const

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory

def make_source(classname):
    common = Directory()
    common.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("'+classname+'-common")',
                          'PACKAGE_VERSION("2.3.4")']))
    common.add(
        name=const.CONFIX2_DIR,
        entry=File())
    common.add(
        name='common.h',
        entry=File(lines=['#ifndef COMMON_H',
                          '#define COMMON_H',
                          'void common(void);',
                          '#endif']))
    common.add(
        name='common.c',
        entry=File(lines=['#include "common.h"',
                          'void common(void) {}']))

    lo = Directory()
    lo.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("'+classname+'-lo")',
                          'PACKAGE_VERSION("6.6.6")']))
    lo.add(
        name=const.CONFIX2_DIR,
        entry=File())
    lo_include = lo.add(
        name='include',
        entry=Directory())
    lo_include.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['RELOCATE_HEADER(filename="lo.h", directory=["source"])',
                          '# require the header, begging for early',
                          '# errors',
                          'REQUIRE_H(filename="common.h", urgency=URGENCY_ERROR)']))
    lo_include.add(
        name='lo.h',
        entry=File(lines=['#ifndef LO_H',
                          '#define LO_H',
                          '/* just for fun (or if we dont test it elsewhere): */',
                          '/*   require something from a relocated header */',
                          '#include <common.h>',
                          'void lo(void);',
                          '#endif']))
    lo_source = lo.add(
        name='source',
        entry=Directory())
    lo_source.add(
        name=const.CONFIX2_DIR,
        entry=File(lines=['# require the header, begging for early',
                          '# errors',
                          'REQUIRE_H(filename="common.h", urgency=URGENCY_ERROR)',
                          '# this one is internal - requre it just for fun',
                          'REQUIRE_H(filename="lo.h", urgency=URGENCY_ERROR)']))
    lo_source.add(
        name='lo.c',
        entry=File(lines=['#include "lo.h"',
                          '#include <common.h>',
                          'void lo(void) {',
                          '    (void)common();',
                          '}']))


    hi = Directory()
    hi.add(
        name=const.CONFIX2_PKG,
        entry=File(lines=['PACKAGE_NAME("'+classname+'-hi")',
                          'PACKAGE_VERSION("1.2.3")']))
    hi.add(
        name=const.CONFIX2_DIR,
        entry=File())
    hi.add(
        name='hi.c',
        entry=File(lines=['#include <lo.h>',
                          '#include <common.h>'
                          'int main(void) {',
                          '    (void)lo();',
                          '    (void)common();',
                          '    return 0;'
                          '}']))

    return (common, lo, hi)
