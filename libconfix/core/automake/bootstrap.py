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

import autoconf_archive

def bootstrap(packageroot, path, use_libtool, argv0):
    aclocal_incdirs = []
    aclocal_incdirs.append(autoconf_archive.include_path(argv0))
    
    if use_libtool:
        libtoolize_prog = external_cmd.search_program('libtoolize', path)
        if libtoolize_prog is None:
            raise Error('libtoolize not found along path')
        aclocal_incdirs.append(os.path.join(os.path.dirname(libtoolize_prog), '../share/aclocal'))
        external_cmd.exec_program(program=libtoolize_prog, dir=packageroot, args=['--force', '--copy'], path=path)
        pass

    aclocal(packageroot=packageroot, includedirs=aclocal_incdirs, path=path)
    autoheader(packageroot=packageroot, path=path)
    automake(packageroot=packageroot, path=path)
    autoconf(packageroot=packageroot, path=path)
    pass

def aclocal(packageroot, includedirs, path):
    aclocal_args = []
    for d in includedirs:
        aclocal_args.extend(['-I', d])
        pass
    external_cmd.exec_program(program='aclocal', args=aclocal_args, dir=packageroot, path=path)
    pass

def autoheader(packageroot, path):
    external_cmd.exec_program(program='autoheader', dir=packageroot, path=path)
    pass

def automake(packageroot, path):
    external_cmd.exec_program(program='automake',
                              args=['--foreign', '--add-missing', '--copy'],
                              dir=packageroot,
                              path=path)
    pass

def autoconf(packageroot, path):
    external_cmd.exec_program(program='autoconf', dir=packageroot, path=path)
    pass

