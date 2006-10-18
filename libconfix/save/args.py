# $Id: args.py,v 1.34 2006/07/18 10:43:16 jfasch Exp $

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
import types
import getopt

import const
import todo
import core.debug
import repo_automake
from configprofile import ConfigConfigure, ConfigMake
from configfile import ConfigFile
from core.error import Error

def initial_params():

    """ Get an initial parameter set. """

    # this is a pretty big hack, but it ought to work as long as
    # people don't go around messing with the relative locations of
    # installation dirs.

    base_m4dir = os.path.join(os.path.dirname(sys.argv[0]), os.pardir,
                              'share', 'confix', 'ac-m4')

    params = {}
    params[const.ARG_ADVANCED] = 0
    params[const.ARG_VERBOSITY] = 1
    params[const.ARG_CONFIGFILES] = []
    params[const.ARG_REPOSITORY] = []
    params[const.ARG_READONLY_PREFIXES] = []
    params[const.ARG_TRACE] = []
    params[const.ARG_PROFILE] = 'default'
    params[const.ARG_PACKAGEROOT] = os.getcwd()
    params[const.ARG_M4INCDIR] = [

        # for convenience, I incorporate the autoconf macro archive
        # and set the path to it if anybody wants it.

        os.path.join(base_m4dir, 'autoconf-archive2', 'm4source'),
        ]

    # I do not use libtool by default because I'm still not 100% sure
    # about it (especially with C++)

    params[const.ARG_USELIBTOOL] = 0

    # same for bulk-install

    params[const.ARG_USE_BULK_INSTALL] = 0

    # same for kde-hack

    params[const.ARG_USE_KDE_HACK] = 0

    # same for timings on/off

    params[const.ARG_PRINT_TIMINGS] = 0

    # same for message-prefix

    params[const.ARG_MESSAGE_PREFIX] = ''

    return params

def conffile(fullpaths, profilename):
    """
    Interpret profile "profilename" from configfiles given in "fullpaths".
    """

    # fill in default empty configuration objects so we can update
    # them with multiple configuration option sets below.

    dict = { const.ARG_CONFIGUREPARAMS : ConfigConfigure(),
             const.ARG_MAKEPARAMS : ConfigMake() }

    real_fullpaths = fullpaths[:]
    if len(real_fullpaths) == 0:
        tilde_confix = os.path.expanduser(os.path.expandvars('~/.confix'))
        if os.path.isfile(tilde_confix):
            real_fullpaths.append(tilde_confix)
            pass
        pass

    if len(real_fullpaths) == 0:
        if profilename != 'default':
            raise Error('Explicit profile name (other than "default") specified, but no configuration file')

    for fullpath in real_fullpaths:
        file = ConfigFile(fullpath)
        profile = file.get_profile(profilename)
        if not profile:
            continue

        if profile.prefix():
            dict[const.ARG_PREFIX] = profile.prefix()

        if profile.readonly_prefixes():
            dict[const.ARG_READONLY_PREFIXES] = profile.readonly_prefixes()

        if profile.confix().repository():
            dict[const.ARG_REPOSITORY] = profile.confix().repository()

        if profile.buildroot():
            dict[const.ARG_BUILDROOT] = profile.buildroot()

        if profile.use_libtool():
            dict[const.ARG_USELIBTOOL] = 1

        if profile.use_bulk_install():
            dict[const.ARG_USE_BULK_INSTALL] = 1

        if profile.use_kde_hack():
            dict[const.ARG_USE_KDE_HACK] = 1

        if profile.print_timings():
            dict[const.ARG_PRINT_TIMINGS] = 1

        if len(profile.message_prefix()) > 0:
            dict[const.ARG_MESSAGE_PREFIX] = profile.message_prefix()

        if profile.advanced():
            dict[const.ARG_ADVANCED] = 1

        dict[const.ARG_CONFIXPARAMS] = profile.confix()

        conf = profile.configure()
        dict[const.ARG_CONFIGUREPARAMS].add_args(conf.args())
        dict[const.ARG_CONFIGUREPARAMS].update_env(conf.env())

        conf = profile.make()
        dict[const.ARG_MAKEPARAMS].add_args(conf.args())
        dict[const.ARG_MAKEPARAMS].update_env(conf.env())

    return dict

def parse_cmdline():

    """ Parse the commandline. Extract parameters actions. Return a
    tuple (params, actions). """
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', [
            # parameters
            'advanced',
            'configfile=',
            'readonly-prefixes=',
            'profile=',
            'prefix=',
            'packageroot=',
            'packagename=',
            'packageversion=',
            'buildroot=',
            'builddir=',
            'targets=',
            'trace=',
            'message-prefix=',
            'debug=',
            'repository=',
            'use-libtool',
            'use-bulk-install',
            'use-kde-hack',
            'print-timings',
            'quiet',
            'verbose',

            # actions
            'help',
            'version',
            'bootstrap',
            'dumpgraph',
            'configure',
            'make',
            'resolve',
            'output'])
    except getopt.error, e:
        raise Error('Command line error: ', [e])

    params = {}
    actions = []

    # this is a gross hack and should be removed once we have a better
    # config concept
    params[const.ARG_REPOSITORY] = []

    for o,a in opts:
        if o == '--advanced': params[const.ARG_ADVANCED] = 1
        if o == '--configfile': params[const.ARG_CONFIGFILES] = a.split(',')
        if o == '--readonly-prefixes': params[const.ARG_READONLY_PREFIXES] = a.split(',')
        if o == '--profile': params[const.ARG_PROFILE] = a
        if o == '--prefix': params[const.ARG_PREFIX] = a
        if o == '--packageroot': params[const.ARG_PACKAGEROOT] = a
        if o == '--packagename': params[const.ARG_PACKAGENAME] = a
        if o == '--packageversion': params[const.ARG_PACKAGEVERSION] = a
        if o == '--buildroot': params[const.ARG_BUILDROOT] = a
        if o == '--builddir': params[const.ARG_BUILDDIR] = a
        if o == '--targets': params[const.ARG_TARGETS] = a
        if o == '--use-libtool': params[const.ARG_USELIBTOOL] = 1
        if o == '--use-bulk-install': params[const.ARG_USE_BULK_INSTALL] = 1
        if o == '--use-kde-hack': params[const.ARG_USE_KDE_HACK] = 1
        if o == '--print-timings': params[const.ARG_PRINT_TIMINGS] = 1
        if o == '--message-prefix': params[const.ARG_MESSAGE_PREFIX] = a
        if o == '--quiet': params[const.ARG_VERBOSITY] = -1
        if o == '--verbose': params[const.ARG_VERBOSITY] = +1
        if o == '--trace': params[const.ARG_TRACE] = a.split(',')
        if o == '--debug': params[const.ARG_DEBUG] = int(a)

        # this parameter can come multiple times since it makes up a
        # list
        if o == '--repository': params[const.ARG_REPOSITORY].append(a)

        if o == '--help': actions.append(todo.HELP)
        if o == '--version': actions.append(todo.VERSION)
        if o == '--bootstrap': actions.append(todo.BOOTSTRAP)
        if o == '--configure': actions.append(todo.CONFIGURE)
        if o == '--make': actions.append(todo.MAKE)
        if o == '--resolve': actions.append(todo.RESOLVE)
        if o == '--dumpgraph': actions.append(todo.DUMPGRAPH)
        if o == '--output': actions.append(todo.OUTPUT)
        pass

    return (params, actions)

def merge_params(lhs, rhs):

    """ Merge parameter set rhs into parameter set lhs. rhs is not
    changed whereas lhs is. Behaves similar to rhs.update(lhs), with
    the exception that there are some exceptions. """

    for k in rhs.keys():

        # verbosity (ARG_VERBOSITY) is an integer value which is
        # incremented with every --verbose and decremented with every
        # --quiet.

        if k == const.ARG_VERBOSITY:
            assert lhs.has_key(const.ARG_VERBOSITY)
            lhs[const.ARG_VERBOSITY] += rhs[const.ARG_VERBOSITY]
            continue

        # trace (ARG_TRACE) is a list of strings with append semantics
        # (rather than overwriting).

        if k == const.ARG_TRACE:
            if not lhs.has_key(const.ARG_TRACE):
                lhs[const.ARG_TRACE] = []
            lhs[const.ARG_TRACE] += rhs[const.ARG_TRACE]
            continue

        # config files (ARG_CONFIGFILES) is a list of filenames with
        # append semantics.

        if k == const.ARG_CONFIGFILES:
            if not lhs.has_key(const.ARG_CONFIGFILES):
                lhs[const.ARG_CONFIGFILES] = []
            lhs[const.ARG_CONFIGFILES] += rhs[const.ARG_CONFIGFILES]
            continue

        # everything else is overwritten.

        lhs[k] = rhs[k]

def merge_actions(lhs, rhs):

    """ Merge action list rhs into action set lhs. rhs is not changed
    whereas lhs is. Basically, we perform list addition, with the
    exception that there are exceptions. """

    # if rhs contains HELP (--help), then we perform only HELP. else,
    # if rhs contains VERSION (--version), then we perform only
    # VERSION. (note that we have to edit lhs in-place.)

    if todo.HELP in rhs:
        lhs[:] = [todo.HELP]
        return

    if todo.VERSION in rhs:
        lhs[:] = [todo.VERSION]
        return

    lhs += rhs

def finalize_params(params):

    # expand user and env on repo directories

    if params.has_key(const.ARG_REPOSITORY):
        for i in range(len(params[const.ARG_REPOSITORY])):
            params[const.ARG_REPOSITORY][i] = os.path.expanduser(
                os.path.expandvars(params[const.ARG_REPOSITORY][i]))

    # same with readonly-prefixes

    if params.has_key(const.ARG_READONLY_PREFIXES):
        for i in range(len(params[const.ARG_READONLY_PREFIXES])):
            params[const.ARG_READONLY_PREFIXES][i] = os.path.expanduser(
                os.path.expandvars(params[const.ARG_READONLY_PREFIXES][i]))

    # configure parameters: this is not a single value, but an object
    # which has its own intelligence. we do not know anything of its
    # internals, except that we know that it might be interested in
    # the prefix. FIXME: does it want to know more than that?

    if params.has_key(const.ARG_CONFIGUREPARAMS) \
       and params.has_key(const.ARG_PREFIX):
        params[const.ARG_CONFIGUREPARAMS].eat_prefix(params[const.ARG_PREFIX])

    # make parameters: same rationale as with configure parameters...

    if params.has_key(const.ARG_MAKEPARAMS)\
       and params.has_key(const.ARG_PREFIX):
        params[const.ARG_MAKEPARAMS].eat_prefix(params[const.ARG_PREFIX])

    # substitute user and path into all strings. probably we should do
    # this more selectively.

    for k in params.keys():
        if type(params[k]) is types.StringType:
            params[k] = os.path.expanduser(os.path.expandvars(params[k]))

    # further, we know that ARG_CONFIGFILES is a list of filenames, so
    # we substitute here as well.

    for i in range(len(params[const.ARG_CONFIGFILES])):
        params[const.ARG_CONFIGFILES][i] = os.path.expanduser(os.path.expandvars(params[const.ARG_CONFIGFILES][i]))

def execute_params(params):

    """ Make parameters that deserve special treatment settle in their
    final destination. """

    if params.has_key(const.ARG_TRACE):
        debug.set_trace(params[const.ARG_TRACE])
        pass

    if params.has_key(const.ARG_MESSAGE_PREFIX):
        debug.set_message_prefix(params[const.ARG_MESSAGE_PREFIX])
        pass
