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

import re

_re_include = re.compile('^\s*#\s*include\s*[<"]\s*(\S+)\s*[>"]')
_re_comment = re.compile('//');
_re_main = re.compile('\\bmain\\b')
_re_befstr_main = re.compile('["`\']main')
_re_aftstr_main = re.compile('main["`\']')
_re_main_openparen_after = re.compile('main\s*\\(')
_re_cpp = re.compile('^s*#')

def extract_requires(lines):

    """ From lines (a list of strings), extract the possible
    require-candidates - i.e. the files which are #include<>d. Return
    them as list of strings. """

    reqs = []
    for l in lines:
        m = _re_include.match(l)
        if not m: continue
        reqs.append(m.group(1))

    return reqs

def search_main(lines):
    for l in lines:
        main = _re_main.search(l)
        comment = _re_comment.search(l)
        cpp = _re_cpp.search(l)
        befstr = _re_befstr_main.search(l)
        aftstr = _re_aftstr_main.search(l)
        open_paren_after = _re_main_openparen_after.search(l)

        # no main found at all
        if not main:
            continue

        # a preprocessor directive (likely "#error")
        if cpp:
            continue

        if befstr: continue
        if aftstr: continue
        if not open_paren_after: continue

        # main found and no comment in the line
        if not comment:
            return True

        # if comment comes before main, then main is inside the
        # comment, else the comment is after main
        if comment.start() < main.start():
            continue
        else:
            return True

    return False
