# Copyright (C) 2002-2007 Salomon Automation
# Copyright (C) 2007-2009 Joerg Faschingbauer
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import os

_indentation = 0
debug_level = 0
_levels = {}

_message_prefix = ''

def _get_indent():
    ret = ''
    for i in xrange(_indentation):
        ret = ret + ' '
    return ret

def set_debug_level(l):
    global debug_level
    debug_level = l

def set_trace(levels):
    for l in levels:
        _levels[l] = 1

def set_message_prefix(prefix):
    global _message_prefix
    _message_prefix = prefix
    pass

def has_trace(level):
    return _levels.has_key(level) or _levels.has_key('all')

def indent():
    global _indentation
    _indentation = _indentation + 2

def outdent():
    global _indentation
    _indentation = _indentation - 2

def debug(msg):
    global debug_level
    if debug_level > 0:
        sys.stderr.write(_get_indent() + _message_prefix + msg + '\n')

def trace(levels, msg):
    do_output = 0
    if _levels.has_key('all'):
        do_output = 1
    else:
        for l in levels:
            if _levels.has_key(l):
                do_output = 1
                break

    if do_output:
        sys.stderr.write(_get_indent() + _message_prefix + msg + '\n')

def message(msg, verbosity = 1):
    if verbosity > 0:
        sys.stderr.write(_get_indent() + _message_prefix + msg + "\n")

def warn(msg):
    sys.stderr.write(_get_indent() + _message_prefix + '%s: WARNING: %s\n' % (os.path.basename(sys.argv[0]), msg))

def die(msg):
    sys.stderr.write(_get_indent() + _message_prefix + '%s: ERROR: %s\n' % (os.path.basename(sys.argv[0]), msg))
    sys.exit(101)

def abstract(meth):
    assert 0, meth + " is abstract"
