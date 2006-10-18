# $Id: helper.py,v 1.1 2005/12/20 15:39:58 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

import re
import os

_re_beg_mod = re.compile(r'^\s*module(.*){')
_re_beg_mod_named = re.compile(r'^\s*(\w+)')
_re_end_mod = re.compile(r'^\s*}\s*;?\s*//.*(end of|/)\s*module')

def parse_modules(lines, filename):

    stack_growth = 0
    stack = []
    found_modules = []

    lineno = 0
    for l in lines:
        lineno = lineno + 1
        m = _re_beg_mod.search(l)
        if m:
            n = _re_beg_mod_named.search(m.group(1))
            mod_name = n and n.group(1) or ''
            stack.append(mod_name)
            stack_growth = 1
            continue

        m = _re_end_mod.search(l)            
        if m:
            if len(stack) == 0:
                raise Error(filename + ':' + str(lineno) + ': error: '
                            'end of module found though none was begun')
            if stack_growth == 1 and len(stack[-1]) > 0:
                found_modules.append(stack[0:]) # copy, not just ref
            del stack[-1]
            stack_growth = 0
            continue

    if len(stack):
        raise Error(filename+': error: '
                    'module \''+'::'.join(stack)+'\' was opened but not closed '
                    '(remember, you have to close it with a line like \'} // /module\')')

    return found_modules

def install_path(lines, filename):

    paths = parse_modules(lines=lines, filename=filename)

    if len(paths) > 1:
        raise Error('Found multiple modules, ' + ', '.join(['::'.join(p) for p in paths]))

    install_path = ''
    if len(paths):
        for p in paths[0]:
            install_path = os.path.join(install_path, p)
            pass
        pass

    return install_path
