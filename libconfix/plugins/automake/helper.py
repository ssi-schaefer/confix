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

import types

def automake_name(name):

    """ If name contains letters which do not appear to be valid
    automake identifiers (m4 macros?), substitute them with
    '_'. automake complains (because of the '-') something like::

      12: bad macro name `libentitycontainer_xmi-nsuml_a_SOURCES'

    :todo: are there more characters which are invalid?

    :return: a copy of the input parameter with all the offending
       characters replaced

    """

    clean = name.replace('-', '_')
    clean = clean.replace('.', '_')
    clean = clean.replace('@', '_')
    clean = clean.replace('$', '_')
    clean = clean.replace('/', '_')
    clean = clean.replace('+', '_')
    clean = clean.replace('<', '_')
    clean = clean.replace('>', '_')
    clean = clean.replace(':', '_')
    return clean.replace('%', '_')

def format_word_list(words):
    bare_lines = []

    line = ''
    for w in words:
        if len(line) + len(w) + 1 < 70:
            # word won't overflow the current line; consume word
            if len(line): line = line + ' ' + w
            else: line = w
        else:
            if len(line) > 0:
                # line is already full; flush it and consume word
                bare_lines.append(line)
                line = w
            else:
                # word is longer than max line length. make a single
                # line of it.
                line = w
                pass
            pass
        pass

    if len(line):
        bare_lines.append(line)
        pass

    # prepend spaces to all but the first line. append '\' to all but
    # the last line. add line to return value.

    ret_lines = []

    for i in range(len(bare_lines)):
        line = bare_lines[i]
        if i != 0: line = '    ' + line
        if i < len(bare_lines)-1:
            line = line + ' \\'
        ret_lines.append(line)
        pass

    return ret_lines

