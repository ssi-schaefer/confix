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

import helper

from libconfix.core.utils.error import Error

import types
import re

class MakefileElement:
    def __init__(self):
        pass
    def lines(self):
        assert 0, 'abstract'
        pass
    pass

class White(MakefileElement):
    def __init__(self, lines):
        MakefileElement.__init__(self)
        self.lines_ = lines
        pass
    def lines(self):
        return self.lines_
    pass

class Include(MakefileElement):
    def __init__(self, file):
        MakefileElement.__init__(self)
        self.__file = file
        pass
    def __str__(self):
        return 'include '+self.__file
    def file(self):
        return self.__file
    def lines(self):
        return ['include '+self.__file]
    pass

""" BACKSLASH_MITIGATOR: we wrap long lines with backslashes, so that
various tools are happy. for example, config.status scans Makefile.in
using grep. on several Unices (AIX, HP-UX I seem to remember), grep
does not accept lines of infinite length.

certain make macros - AM_CPPFLAGS for example - end up being long
lists of items most of which are autoconf @blah@ substitutions, some
of which end up being substituted with the empty string. if such an
empty substitution is on a single line at the end of such a long list,
the previous line contains a trailing backslash, followed by an empty
line. some make implementations (HP-UX, again) handle this kind of
consciousless and scan through until they find something meaningful,
which they then consider part of th list. argh.

however, the solution is to terminate every list with a macro that
expands to nothing, just to make bogus make's scan algorithm happy."""

BACKSLASH_MITIGATOR = '$(CONFIX_BACKSLASH_MITIGATOR)'

class List(MakefileElement):
    def __init__(self, name, values, mitigate):
        self.name_ = name
        self.values_ = values[:]
        self.mitigate_ = mitigate
        pass
    def __str__(self):
        return self.name_ + '=' + str(self.values_)
    def __iter__(self):
        return self.values_.__iter__()
    def __len__(self):
        return self.values_.__len__()
    def __getitem__(self, index):
        return self.values_.__getitem__(index)
    def name(self):
        return self.name_
    def values(self):
        return self.values_
    def append(self, value):
        self.values_.append(value)
        pass
    def lines(self):
        if len(self.values_) == 0:
            return []
        wordlist = [self.name_+' ='] + self.values_
        if self.mitigate_:
            wordlist.append(BACKSLASH_MITIGATOR)
            pass
        return helper.format_word_list(wordlist)
    pass

class Set(MakefileElement):
    def __init__(self, name, values, mitigate):
        self.name_ = name
        self.values_ = set(values)
        self.mitigate_ = mitigate
        pass
    def __str__(self):
        return self.name_ + '=' + str(self.values_)
    def __iter__(self):
        return self.values_.__iter__()
    def __len__(self):
        return self.values_.__len__()
    def __contains__(self, value):
        return self.values_.__contains__(value)
    def name(self):
        return self.name_
    def values(self):
        return self.values_
    def add(self, value):
        self.values_.add(value)
        pass
    def lines(self):
        if len(self.values_) == 0:
            return []
        values = list(self.values_)
        values.sort()
        wordlist = [self.name_+' ='] + values
        if self.mitigate_:
            wordlist.append('$(CONFIX_BACKSLASH_MITIGATOR)')
            pass
        return helper.format_word_list(wordlist)
    pass

class Rule(MakefileElement):
    def __init__(self, targets, prerequisites=[], commands=[]):
        assert type(targets) is types.ListType
        assert len(targets)
        self.targets_ = targets[:]
        self.prerequisites_ = prerequisites[:]
        self.commands_ = commands[:]
        pass

    def targets(self):
        return self.targets_

    def prerequisites(self):
        return self.prerequisites_
    def add_prerequisite(self, p):
        self.prerequisites_.append(p)
        pass

    def commands(self):
        return self.commands_
    def add_command(self, c):
        self.commands_.append(c)
        pass
        
    def lines(self):
        targ_prereqlist = self.targets_[:]
        targ_prereqlist[-1] = targ_prereqlist[-1] + ':'
        targ_prereqlist.extend(self.prerequisites_)

        commandlist = []
        if self.commands_ is not None:
            for c in self.commands_:
                if type(c) is types.StringType:
                    commandlist.append('\t'+c)
                elif (type(c) is types.ListType) or (type(c) is types.TupleType):
                    commandlist.extend(['\t'+l for l in helper.format_word_list(c)])
                else: assert 0
                pass
            pass
        
        return helper.format_word_list(targ_prereqlist) + commandlist
    pass



def find_list(elements, name):
    for e in elements:
        if isinstance(e, List):
            if e.name() == name:
                return e
            continue
        pass
    return None

def find_rule(elements, targets):
    for e in elements:
        if isinstance(e, Rule):
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
    return List(name=match.group(1), values=values, mitigate=False)

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
        return White(lines=white_lines)
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
    
    rule = Rule(targets=targets,
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
    return Include(file=match.group(1))

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
