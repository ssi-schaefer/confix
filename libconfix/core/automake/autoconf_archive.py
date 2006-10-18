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

import os

from libconfix.core.utils.error import Error
from libconfix.core.utils import external_cmd

def find_archive_root(argv0):
    dir = os.path.dirname(argv0)

    # accommodate for relative paths.
    if not os.path.isabs(dir):
        dir = os.path.normpath(os.path.join(os.getcwd(), dir))
        pass

    # first the uninstalled case. (we know programs to be either in
    # the tests subdirectory or in the scripts subdirectory.)
    idx = dir.find(os.path.join('confix', 'tests'))
    if idx == -1:
        idx = dir.find(os.path.join('confix', 'scripts'))
        pass
    if idx != -1:
        retdir = os.path.join(dir[0:idx], 'confix', 'share', 'confix', 'autoconf-archive')
        if not os.path.isdir(retdir):
            raise Error('"'+retdir+'" is not a directory '
                        '(searching the autoconf macro archive the uninstalled way)')
        return retdir

    # ... and then the installed case. this is a pretty big hack, but
    # it ought to work as long as people don't go around messing with
    # the relative locations of installation dirs.
    if dir.endswith('bin'):
        prefixdir = os.path.dirname(dir)
        retdir = os.path.join(prefixdir, 'share', 'confix', 'autoconf-archive')
        if not os.path.isdir(retdir):
            raise Error('"'+retdir+'" is not a directory '
                        '(searching the autoconf macro archive the installed way)')
        return retdir

    # we seem to be running completely outside confix's world.
    confix2_py = external_cmd.search_program(program='confix2.py', path=None)
    if confix2_py is None:
        raise Error('Autoconf macro archive not found (no confix2.py in $PATH)')
    return find_archive_root(argv0=confix2_py)

    raise Error('Autoconf macro archive not found (installation error?)')

def include_path(argv0):
    return os.path.join(find_archive_root(argv0), 'm4src')
