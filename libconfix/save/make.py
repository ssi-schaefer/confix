# $Id: make.py,v 1.12 2006/07/18 10:43:16 jfasch Exp $

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

def make(args, targets, destdir_arg, verbosity = 1):

    destdir = os.path.expanduser(os.path.expandvars(destdir_arg))

    curdir = os.getcwd()

    try:
        os.chdir(destdir)
    except Exception, e:
        raise Error("Could not chdir to compile directory "+destdir, [e])

    arglist = args.args() + targets

    env = {}
    for k in os.environ.keys():
        env[k] = os.environ[k]
    env.update(args.env())

    # expand all of the environment variables

    for k in env.keys():
        env[k] = os.path.expandvars(os.path.expanduser(env[k]))

    if args.make():
        program = args.make()
    else:
        program = 'make'

        # have to search PATH manually (stubbornly, I don't want to
        # exec make via the shell to have the shell find make for me)

        path = ''
        if env.has_key('PATH'): path = env['PATH']
        else: path = ['/usr/bin']

        for dir in path.split(os.pathsep):
            file = os.path.join(dir, program)
            if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.X_OK):
                program = file
                break

    debug.message('+ MAKE')
    debug.message('+ Current working directory: ' + destdir)

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

    rv = 1

    try:
        rv = os.spawnve(os.P_WAIT, program, [program] + arglist, env)
    except Exception, e:
        os.chdir(curdir)
        raise Error("Could not execute "+program, [e])

    os.chdir(curdir)

    if rv != 0:
        raise Error("spawn("+program+") returned non-null ("+str(rv)+")")
