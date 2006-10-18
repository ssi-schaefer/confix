# $Id: configprofile.py,v 1.17 2006/07/18 10:43:16 jfasch Exp $

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
import re

import const
import core.helper
from types import *
from core.error import Error
from core.require import Require
from buildable_mgr_bases import \
     BuildableCreator, \
     BuildableClusterer

class ConfigConfix:

    """ An abstraction of a dictionary type that contains
    configuration information for Confix in general. Currently the
    only significant Confix-specific information is the REPOSITORY
    argument, which tells Confix about a series of package
    repositories to use when resolving package dependencies. Also many
    of the Confix command line arguments can also be included, for
    example, PREFIX and BUILDROOT.  """

    def __init__(self, dict={}):

        if dict.has_key(const.CFG_PROF_CONFIX_REPOSITORY):
            if not type(dict[const.CFG_PROF_CONFIX_REPOSITORY]) is ListType:
                raise Error("'"+const.CFG_PROF_CONFIX_REPOSITORY+"' must be a list")
            self.repository_ = dict[const.CFG_PROF_CONFIX_REPOSITORY]
        else:
            self.repository_ = None

        if dict.has_key(const.CFG_PROF_CONFIX_GLOBAL_REQUIRES):
            if not type(dict[const.CFG_PROF_CONFIX_GLOBAL_REQUIRES]) is ListType:
                raise Error("'"+const.CFG_PROF_CONFIX_GLOBAL_REQUIRES+"' must be a list")
            for r in dict[const.CFG_PROF_CONFIX_GLOBAL_REQUIRES]:
                if not isinstance(r, Require):
                    raise Error("'"+const.CFG_PROF_CONFIX_GLOBAL_REQUIRES+"' must only contain "
                                "Require objects; use the confix API functions")
            self.global_requires_ = dict[const.CFG_PROF_CONFIX_GLOBAL_REQUIRES]
        else:
            self.global_requires_ = []

        if dict.has_key(const.CFG_PROF_CONFIX_BUILDABLECREATORS):
            if not type(dict[const.CFG_PROF_CONFIX_BUILDABLECREATORS]) is ListType:
                raise Error("'"+const.CFG_PROF_CONFIX_BUILDABLECREATORS+"' must be a list")
            for (regex, c) in dict[const.CFG_PROF_CONFIX_BUILDABLECREATORS]:
                try:
                    re.compile(regex)
                except Exception, e:
                    raise Error('Could not compile regex "'+regex+'"', [e])
                if not isinstance(c, BuildableCreator):
                    raise Error('Object for regex "'+regex+'" is not of type BuildableCreator')
            self.buildablecreators_ = dict[const.CFG_PROF_CONFIX_BUILDABLECREATORS]
        else:
            self.buildablecreators_ = []

        if dict.has_key(const.CFG_PROF_CONFIX_BUILDABLECLUSTERERS):
            if not type(dict[const.CFG_PROF_CONFIX_BUILDABLECLUSTERERS]) is ListType:
                raise Error("'"+const.CFG_PROF_CONFIX_BUILDABLECLUSTERERS+"' must be a list")
            for (c) in dict[const.CFG_PROF_CONFIX_BUILDABLECLUSTERERS]:
                if not isinstance(c, BuildableClusterer):
                    raise Error('Object is not of type BuildableClusterer')
            self.buildableclusterers_ = dict[const.CFG_PROF_CONFIX_BUILDABLECLUSTERERS]
        else:
            self.buildableclusterers_ = []

    def repository(self):
        return self.repository_

    def global_requires(self): return self.global_requires_

    def buildablecreators(self): return self.buildablecreators_

    def buildableclusterers(self): return self.buildableclusterers_

class ConfigExternal:

    """ An abstract base class for storing configuration information
    for external commands (currently limited to "make" and
    "configure").  """

    def __init__(self, dict={}):
        self.env_ = {}
        env = None
        if dict.has_key(const.CFG_PROF_EXT_ENV):
            env = dict[const.CFG_PROF_EXT_ENV]

        if env is not None:
            if not type(env) is DictionaryType:
                raise Error("'"+const.CFG_PROF_EXT_ENV+"' must be a dictionary")
            for k in env.keys():
                if not type(env[k]) is StringType:
                    raise Error(const.CFG_PROF_EXT_ENV+"["+k+"] must be a string")
            self.env_ = env

        self.args_ = []
        args = None
        if dict.has_key(const.CFG_PROF_EXT_ARGS):
            args = dict[const.CFG_PROF_EXT_ARGS]

        if args is not None:
            if type(args) is TupleType:
                raise Error("'"+const.CFG_PROF_EXT_ARGS+"' must be a list (but rather is a tuple)")
            if not type(args) is ListType:
                raise Error("'"+const.CFG_PROF_EXT_ARGS+"' must be a list")
            self.args_ = args

    def eat_prefix(self, prefix):
        pass

    def args(self):
        return self.args_

    def env(self):
        return self.env_

    def add_args(self, args):
        """
        Add a list of arguments to the existing list.

        @type  args: list
        @param args: a list of arguments to add to the existing argument list.
        """

        assert type(args) is ListType
        self.args_ = self.args_ + args

    def update_env(self, dict, append_flags = 1):

        """ Update the environment based on the values in a new
        environment. Old environment values will be updated (replaced
        or appended as desired) with values in the new environment.

        @type dict: dictionary

        @param dict: the new environment variables and values to use.

        @type append_flags: boolean

        @param append_flags: if true, this will cause all environment
        variables ending with 'flags' or 'libs' (case insensitive) to
        have the new values appended instead of the new values
        completely replacing the old values.  """

        assert type(dict) is DictionaryType
        for k, v in dict.items():
            if append_flags and \
                   (k.lower().endswith('flags') or k.lower().endswith('libs')):
                if k not in self.env_.keys(): self.env_[k] = ''
                envs = []
                if len(self.env_[k]):
                    envs.append(self.env_[k])
                    pass
                if len(dict[k]):
                    envs.append(dict[k])
                    pass
                self.env_[k] = ' '.join(envs)
            else:
                self.env_[k] = dict[k]

    def replace_env(self, dict):

        """ Completely replace the environment dictionary with a new
        one.

        @type  dict: dictionary
        @param dict: the new environment variables and their associated values.
          The old environment will be completely replaced with this new
          environment.
        """

        assert type(dict) is DictionaryType
        self.env_ = dict

class ConfigConfigure(ConfigExternal):

    """ An abstraction of a dictionary that stores configuration
    information for running the standard GNU "configure" command
    before building a package.  Configuration information includes
    environment variables and command line arguments.  """

    def __init__(self, dict={}):
        ConfigExternal.__init__(self, dict)

    def eat_prefix(self, prefix):
        if not prefix: return
        for arg in self.args_:
            if arg.find('--prefix=') >= 0:
                return
        self.args_.append('--prefix='+os.path.expanduser(\
             os.path.expandvars(prefix)))

class ConfigMake(ConfigExternal):

    """ A dictionary abstraction to store configuration information
    for using the "make" command. Configuration information is
    basically a hash of environment information and arguments to
    provide to "make".  """

    def __init__(self, dict={}):
        ConfigExternal.__init__(self, dict)

    def make(self):
        return None

class ConfigProfile:

    """ A class that encapsulates the information from a particular
    configuration profile in a particular L{configuration file
    <configfile.ConfigFile>}. A profile stores configuration
    information for Confix in general (see the L{ConfigConfix} class),
    and for the "configure" and "make" commands (L{ConfigConfigure}
    and L{ConfigMake}, respectively).  """

    def __init__(self, dict):
        """
        Initialize a new profile based on the information in the dictionary.

        @type  dict: dictionary (hash table)
        @param dict: the configuration information from a particular
          configuration file profile.
        """

        if dict.has_key(const.CFG_PROF_PREFIX):
            self.prefix_ = dict[const.CFG_PROF_PREFIX]
        else:
            self.prefix_ = None

        if dict.has_key(const.CFG_PROF_CONFIX_READONLY_PREFIXES):
            if not type(dict[const.CFG_PROF_CONFIX_READONLY_PREFIXES]) is ListType:
                raise Error("'"+const.CFG_PROF_CONFIX_READONLY_PREFIXES+"' must be a list")
            self.readonly_prefixes_ = dict[const.CFG_PROF_CONFIX_READONLY_PREFIXES]
        else:
            self.readonly_prefixes_ = None

        if dict.has_key(const.CFG_PROF_BUILDROOT):
            self.buildroot_ = dict[const.CFG_PROF_BUILDROOT]
        else:
            self.buildroot_ = None

        if dict.has_key(const.CFG_PROF_USE_LIBTOOL):
            try:
                self.use_libtool_ = core.helper.read_boolean(dict[const.CFG_PROF_USE_LIBTOOL])
            except Error, e:
                raise Error("Could not read boolean value '"+const.CFG_PROF_USE_LIBTOOL+"'")
        else:
            self.use_libtool_ = None

        if dict.has_key(const.CFG_PROF_USE_BULK_INSTALL):
            try:
                self.use_bulk_install_ = helper.read_boolean(dict[const.CFG_PROF_USE_BULK_INSTALL])
            except Error, e:
                raise Error("Could not read boolean value '"+const.CFG_PROF_USE_BULK_INSTALL+"'")
        else:
            self.use_bulk_install_ = None

        if dict.has_key(const.CFG_PROF_USE_KDE_HACK):
            try:
                self.use_kde_hack_ = helper.read_boolean(dict[const.CFG_PROF_USE_KDE_HACK])
            except Error, e:
                raise Error("Could not read boolean value '"+const.CFG_PROF_USE_KDE_HACK+"'")
        else:
            self.use_kde_hack_ = None

        if dict.has_key(const.CFG_PROF_MESSAGE_PREFIX):
            self.message_prefix_ = dict[const.CFG_PROF_MESSAGE_PREFIX]
        else:
            self.message_prefix_ = ''

        if dict.has_key(const.CFG_PROF_PRINT_TIMINGS):
            try:
                self.print_timings_ = helper.read_boolean(dict[const.CFG_PROF_PRINT_TIMINGS])
            except Error, e:
                raise Error("Could not read boolean value '"+const.CFG_PROF_PRINT_TIMINGS+"'")
        else:
            self.print_timings_ = None

        if dict.has_key(const.CFG_PROF_ADVANCED):
            try:
                self.advanced_ = core.helper.read_boolean(dict[const.CFG_PROF_ADVANCED])
            except Error, e:
                raise Error("Could not read boolean value '"+const.CFG_PROF_ADVANCED+"'")
        else:
            self.advanced_ = None

        if dict.has_key(const.CFG_PROF_CONFIX):
            try:
                self.confix_ = ConfigConfix(dict[const.CFG_PROF_CONFIX])
            except Error, e:
                raise Error("Error in '"+const.CFG_PROF_CONFIX+"' section", [e])
        else:
            self.confix_ = ConfigConfix()

        if dict.has_key(const.CFG_PROF_CONFIGURE):
            try:
                self.configure_ = ConfigConfigure(dict[const.CFG_PROF_CONFIGURE])
            except Error, e:
                raise Error("Error in '"+const.CFG_PROF_CONFIGURE+"' section", [e])
        else:
            self.configure_ = ConfigConfigure()

        if dict.has_key(const.CFG_PROF_MAKE):
            try:
                self.make_ = ConfigMake(dict[const.CFG_PROF_MAKE])
            except Error, e:
                raise Error("Error in '"+const.CFG_PROF_MAKE+"' section", [e])
        else:
            self.make_ = ConfigMake()

    def prefix(self):
        return self.prefix_

    def readonly_prefixes(self):
        return self.readonly_prefixes_

    def buildroot(self):
        return self.buildroot_

    def use_libtool(self):
        return self.use_libtool_

    def use_bulk_install(self):
        return self.use_bulk_install_

    def use_kde_hack(self):
        return self.use_kde_hack_

    def message_prefix(self):
        return self.message_prefix_

    def print_timings(self):
        return self.print_timings_

    def advanced(self):
        return self.advanced_

    def confix(self):
        return self.confix_

    def configure(self):
        return self.configure_

    def make(self):
        return self.make_
