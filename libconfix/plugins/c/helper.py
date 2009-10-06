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

def iter_includes(lines):
    """
    From lines (a list of strings), extract the possible
    require-candidates - i.e. the files which are #include<>d. Return
    them as list of strings.
    """
    for l in lines:
        m = _re_include.match(l)
        if m:
            yield m.group(1)
            pass
        pass
    pass

def search_main(lines):
    for l in lines:
        # no main found at all
        if not _re_main.search(l): continue

        # a preprocessor directive (likely "#error")
        if _re_cpp.search(l): continue

        if _re_befstr_main.search(l): continue
        if _re_aftstr_main.search(l): continue
        if not _re_main_openparen_after.search(l): continue

        comment = _re_comment.search(l)

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
