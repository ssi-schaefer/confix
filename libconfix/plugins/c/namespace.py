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


from libconfix.core.utils.error import Error

import re

_re_beg_ns = re.compile(r'^\s*namespace(.*){')
_re_beg_ns_named = re.compile(r'^\s*(\w+)')
_re_end_ns = re.compile(r'^\s*}\s*;?\s*//.*(end of|/)\s*namespace')

class AmbiguousNamespace(Error):
    def __init__(self, namespaces):
        Error.__init__(self, 'Multiple namespaces: '+str(['::'.join(ns) for ns in namespaces]))
        pass
    pass

def find_namespaces(lines):

    stack_growth = 0
    stack = []
    found_namespaces = []

    lineno = 0
    for l in lines:
        lineno = lineno + 1
        m = _re_beg_ns.search(l)
        if m:
            n = _re_beg_ns_named.search(m.group(1))
            ns_name = n and n.group(1) or ''
            stack.append(ns_name)
            stack_growth = 1
            continue

        m = _re_end_ns.search(l)            
        if m:
            if len(stack) == 0:
                raise Error('error at line '+str(lineno)+': '
                            'end of namespace found though none was begun')
            if stack_growth == 1 and len(stack[-1]) > 0:
                found_namespaces.append(stack[0:]) # copy, not just ref
            del stack[-1]
            stack_growth = 0
            continue

    if len(stack):
        raise Error('namespace \''+'::'.join(stack)+'\' was opened but not closed '
                    '(remember, you have to close it with a line like \'} // /namespace\')')

    return found_namespaces

def find_unique_namespace(lines):
    namespaces = find_namespaces(lines)
    if len(namespaces) == 1:
        return namespaces[0]
    if len(namespaces) > 1:
        raise AmbiguousNamespace(namespaces)
    if len(namespaces) == 0:
        return []
        
    
