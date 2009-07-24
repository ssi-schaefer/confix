# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.plugins.automake import makefile

from libconfix.core.utils.error import Error

import re

def find_list(elements, name):
    for e in elements:
        if isinstance(e, makefile.List):
            if e.name() == name:
                return e
            continue
        pass
    return None

def find_rule(elements, targets):
    for e in elements:
        if isinstance(e, makefile.Rule):
            if e.targets() == targets:
                return e
            continue
        pass
    return None

def parse_makefile(lines):
    elements = []
    my_lines = collapse_continuations(lines)
    while True:
        consume_white(my_lines)
        if len(my_lines) == 0:
            break
        if is_list(my_lines):
            elements.append(consume_list(my_lines))
            continue
        if is_rule(my_lines):
            elements.append(consume_rule(my_lines))
            continue
        if is_include(my_lines):
            elements.append(consume_include(my_lines))
            continue
        raise Error('Bad line: "'+my_lines[0]+'"')
    return elements

rex_list = re.compile(r'^([\w_\.]+)\s*=\s*(.*)$')
rex_listelem = re.compile(r'\S+')
def is_list(lines):
    return rex_list.search(lines[0])
def consume_list(lines):
    match = rex_list.search(lines[0])
    if match is None:
        raise Error('Error parsing list: '+lines[0])
    del lines[0]
    values = rex_listelem.findall(match.group(2))
    if len(values) > 0 and values[-1] == '$(CONFIX_BACKSLASH_MITIGATOR)':
        del values[-1]
        pass
    return makefile.List(name=match.group(1), values=values, mitigate=False)

rex_comment = re.compile(r'^\s*#')
rex_white = re.compile(r'^\s*$')
def consume_white(lines):
    if len(lines) == 0:
        return None
    white_lines = []
    while rex_comment.search(lines[0]) or rex_white.search(lines[0]):
        white_lines.append(lines[0])
        del lines[0]
        if len(lines) == 0:
            break
        pass
    if len(white_lines) > 0:
        return makefile.White(lines=white_lines)
    return None

rex_target_prerequisite = re.compile(r'^\s*(.*)\s*:\s*(.*)\s*$')
rex_command = re.compile(r'^\t(.*)$')
def is_rule(lines):
    return rex_target_prerequisite.search(lines[0])
def consume_rule(lines):
    match = rex_target_prerequisite.search(lines[0])
    if match is None:
        raise Error('Error parsing rule: '+lines[0])
    del lines[0]

    targets = rex_listelem.findall(match.group(1))
    prerequisites=rex_listelem.findall(match.group(2))
    
    rule = makefile.Rule(targets=targets,
                         prerequisites=prerequisites)
    while True:
        if len(lines) == 0:
            break
        match = rex_command.search(lines[0])
        if match is None:
            break
        del lines[0]
        rule.add_command(match.group(1))
        pass
    return rule

rex_include = re.compile(r'^\s*include\s+(.*)\s*$')
def is_include(lines):
    return rex_include.search(lines[0])
def consume_include(lines):
    match = rex_include.search(lines[0])
    if match is None:
        raise Error('Error parsing include: '+lines[0])
    del lines[0]
    return makefile.Include(file=match.group(1))

def collapse_continuations(lines):
    ret = []
    cur_line = None
    for l in lines:
        if cur_line:
            cur_line += l
        else:
            cur_line = l
            pass
        if not cur_line.endswith('\\'):
            ret.append(cur_line)
            cur_line = None
        else:
            cur_line = cur_line[0:-1]
            pass
        pass
    assert cur_line is None
    return ret
