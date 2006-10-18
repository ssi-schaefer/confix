# $Id: configure.py,v 1.17 2006/07/18 10:43:16 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
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

import os
import sys

import core.debug
from core.error import Error

def configure(cmdline, environment, srcdir, destdir, create_dirs, verbosity):

    """ Call srcdir/configure with args (a dictionary, to be
    interpreted), with the cwd being destdir. """

    if not srcdir:
        raise Error("Cannot call configure because source directory not specified")
    if not destdir:
        raise Error("Cannot call configure because compilation directory not specified")

    srcdir_expanded = os.path.expanduser(os.path.expandvars(srcdir))
    destdir_expanded = os.path.expanduser(os.path.expandvars(destdir))

    assert os.path.isabs(srcdir)

    program = os.path.join(srcdir_expanded, 'configure')

    curdir = os.getcwd() # remember to change back to

    if create_dirs and not os.path.isdir(destdir_expanded):
        if os.path.exists(destdir_expanded):
            raise Error("Compile directory %s exists but is not a directory"
                        % destdir_expanded, [])
        try:
            os.makedirs(destdir_expanded)
        except Exception, e:
            raise Error("Cannot create compile directory "+destdir_expanded, [e])

    try:
        os.chdir(destdir_expanded)
    except Exception, e:
        raise Error("Could not chdir to compile directory "+destdir_expanded, [e])

    # expand environment variables in the argument list

    arglist = []

    for a in cmdline:
        arglist.append(os.path.expandvars(a))

    env = {}
    for k in os.environ.keys():
        env[k] = os.environ[k]
    env.update(environment)

    # expand all of the environment variables

    for k in env.keys():
        env[k] = os.path.expandvars(os.path.expanduser(env[k]))

    debug.message('+ CONFIGURE')
    debug.message('+ Current working directory: ' + destdir_expanded)
    debug.message('+ Calling: ' + program)
    if len(arglist):
        debug.message('+ Arguments:')
    for a in arglist:
        debug.message('+ ' + 2 * ' ' + a)
    if debug.has_trace('env'):
        if len(env.keys()):
            debug.message('+ Environment:')
        for k in env.keys():
            debug.message('+ ' + 2 * ' ' + k + '=' + env[k])

    try:
        rv = os.spawnve(os.P_WAIT, program, [program] + arglist, env)
    except Exception, e:
        os.chdir(curdir)
        raise Error("Could not execute "+program, [e])

    os.chdir(curdir)

    if rv != 0:
        raise Error("spawn("+program+") returned non-null ("+str(rv)+")")
