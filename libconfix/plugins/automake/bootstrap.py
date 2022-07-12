# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

#import autoconf_archive
import kde_hack

from libconfix.core.utils.error import Error
from libconfix.core.utils import external_cmd
from libconfix.core.utils import helper
from libconfix.core.utils import debug

import time
import os

def bootstrap(packageroot, use_kde_hack, argv0, path=None):
    aclocal_incdirs = []
    #aclocal_incdirs.append(autoconf_archive.include_path(argv0))

    # if package's configure.ac looks like using libtool, then we
    # assume that the package must be libtoolize'd.
    if (_using_libtool(packageroot)):
        libtoolize_prog = external_cmd.search_program('libtoolize', path)
        if libtoolize_prog is None:
            raise Error('libtoolize not found along path')
        aclocal_incdirs.append(os.path.join(os.path.dirname(libtoolize_prog), '../share/aclocal'))
        args = ['--force', '--copy']
        debug.message('libtoolize ...')
        before = time.time()
        external_cmd.exec_program(program=libtoolize_prog, dir=packageroot, args=args, path=path, print_cmdline=True)
        debug.message('done libtoolize ('+str(time.time()-before)+' seconds)')
        pass

    debug.message('aclocal ...')
    before = time.time()
    aclocal(packageroot=packageroot, includedirs=aclocal_incdirs, path=path)
    debug.message('done aclocal ('+str(time.time()-before)+' seconds)')

    debug.message('autoheader ...')
    before = time.time()
    autoheader(packageroot=packageroot, path=path)
    debug.message('done autoheader ('+str(time.time()-before)+' seconds)')

    debug.message('automake ...')
    before = time.time()
    automake(packageroot=packageroot, path=path)
    debug.message('done automake ('+str(time.time()-before)+' seconds)')

    if use_kde_hack:
        # somehow autoconf will not create a new configure script when
        # it decides that this is not necessary (still don't know how
        # it would decide that). anyway, if it leaves the old script
        # around which we have already patched, then conf.change.pl
        # (the patch is about calling conf.change.pl) will complain
        # about something I don't quite understand. solution: remove
        # configure before re-creating it.
        configure_script = os.sep.join(packageroot+['configure'])
        if os.path.isfile(configure_script):
            debug.message('KDE hack: removing existing configure script')
            os.remove(configure_script)
            pass
        pass
    
    debug.message('autoconf ...')
    before = time.time()
    autoconf(packageroot=packageroot, path=path)
    debug.message('done autoconf ('+str(time.time()-before)+' seconds)')

    if use_kde_hack:
        debug.message('KDE hack: patching configure script...')            
        kde_hack.patch_configure_script(packageroot=packageroot)
        pass
    
    pass

def aclocal(packageroot, includedirs, path):
    aclocal_args = []
    for d in includedirs:
        aclocal_args.extend(['-I', d])
        pass
    external_cmd.exec_program(program='aclocal', args=aclocal_args, dir=packageroot, path=path, print_cmdline=True)
    pass

def autoheader(packageroot, path):
    external_cmd.exec_program(program='autoheader', dir=packageroot, path=path, print_cmdline=True)
    pass

def automake(packageroot, path):
    args = ['--foreign', '--add-missing', '--copy']
    external_cmd.exec_program(program='automake',
                              args=args,
                              dir=packageroot,
                              path=path,
                              print_cmdline=True)
    pass

def autoconf(packageroot, path):
    external_cmd.exec_program(program='autoconf', dir=packageroot, path=path, print_cmdline=True)
    pass

def _using_libtool(packageroot):
    try:
        configure_ac_lines = helper.lines_of_file(os.sep.join(packageroot+['configure.ac']))
    except Error, e:
        raise Error('Determining whether to libtoolize or not', [e])

    for l in configure_ac_lines:
        if l.find('AC_PROG_LIBTOOL') >= 0:
            return True
        pass

    return False
        
