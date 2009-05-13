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

from libconfix.core.utils import external_cmd

import os
import types

def configure(packageroot, builddir, prefix, readonly_prefixes=None, args=None, env=None):
    """ Calls configure. Returns the time taken, in seconds."""
    
    assert type(packageroot) in [types.ListType, types.TupleType]
    assert type(builddir) in [types.ListType, types.TupleType]
    assert type(prefix) in [types.NoneType, types.ListType, types.TupleType]
    assert type(readonly_prefixes) in [types.NoneType, types.ListType, types.TupleType]
    
    argv = []
    if prefix is not None:
        argv.append('--prefix='+os.sep.join(prefix))
        pass
    if readonly_prefixes is not None:
        ro_args = []
        for rp in readonly_prefixes:
            assert type(rp) in [types.ListType, types.TupleType], rp
            ro_args.append(os.sep.join(rp))
            pass
        if len(ro_args):
            argv.append('--with-readonly-prefixes='+','.join(ro_args))
            pass
        pass
    if args is not None:
        argv.extend(args)
        pass

    return external_cmd.exec_program(program=os.sep.join(packageroot + ['configure']),
                                     args=argv,
                                     env=env,
                                     dir=builddir,
                                     print_cmdline=True)
