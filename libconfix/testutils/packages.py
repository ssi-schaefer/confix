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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

def lo_hi1_hi2_highest_exe(name, version):
    ret = Directory()

    ret.add(name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+name+'")',
                              'PACKAGE_VERSION("'+version+'")']))
    ret.add(name=const.CONFIX2_DIR,
            entry=File())
            
    liblo = ret.add(name='lo', entry=Directory())
    liblo.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
    liblo.add(name='lo.h',
              entry=File(lines=['#ifndef LO_H',
                                '#  define LO_H',
                                '#endif',
                                'void lo();']))
    liblo.add(name='lo.c',
              entry=File(lines=['void lo() {}']))

    libhi1 = ret.add(name='hi1', entry=Directory())
    libhi1.add(name=const.CONFIX2_DIR, entry=File(lines={}))
    libhi1.add(name='hi1.h',
               entry=File(lines=['#ifndef HI1_H',
                                 '#  define HI1_H',
                                 '#endif',
                                 'void hi1();']))
    libhi1.add(name='hi1.c',
               entry=File(lines=['#include <hi1.h>',
                                 '#include <lo.h>',
                                 'void hi1() { lo(); }']))

    libhi2 = ret.add(name='hi2', entry=Directory())
    libhi2.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
    libhi2.add(name='hi2.h',
               entry=File(lines=['#ifndef HI2_H',
                                 '#  define HI2_H',
                                 '#endif',
                                 'void hi2();']))
    libhi2.add(name='hi2.c',
               entry=File(lines=['#include <hi2.h>',
                                 '#include <lo.h>',
                                 'void hi2() { lo(); }']))

    highest = ret.add(name='highest', entry=Directory())
    highest.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
    highest.add(name='highest.c',
                entry=File(lines=['#include <hi1.h>',
                                  '#include <hi2.h>',
                                  'void highest() {',
                                  '    hi1();',                                    
                                  '    hi2();',
                                  '}']))

    exe = ret.add(name='exe', entry=Directory())
    exe.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
    exe.add(name='main.c',
            entry=File(lines=['#include <hi1.h>',
                              '#include <hi2.h>',
                              'int main(void) {',
                              '    hi1();',
                              '    hi2();',
                              '    return 0;',
                              '}']))
    return ret
