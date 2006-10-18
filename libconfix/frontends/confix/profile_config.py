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

from config import Configuration

class ProfileConfiguration(Configuration):

    SETUPS = 'SETUPS'
    PREFIX = 'PREFIX'
    READONLY_PREFIXES = 'READONLY_PREFIXES'
    BUILDROOT = 'BUILDROOT'
    SHORT_LIBNAMES = 'SHORT_LIBNAMES'
    USE_LIBTOOL = 'USE_LIBTOOL'
    USE_BULK_INSTALL = 'USE_BULK_INSTALL'
    USE_KDE_HACK = 'USE_KDE_HACK'
    VERBOSITY = 'VERBOSITY'
    TRACE = 'TRACE'
    PRINT_TIMINGS = 'PRINT_TIMINGS'
    MESSAGE_PREFIX = 'MESSAGE_PREFIX'
    ADVANCED = 'ADVANCED'
    CONFIGURE = 'CONFIGURE'
    MAKE = 'MAKE'
    ARGS = 'ARGS'
    ENV = 'ENV'

    def __init__(self, dict):
        self.dictionary_ = dict
        pass

    def setups(self):
        return self.dictionary_.get(ProfileConfiguration.SETUPS)
    def prefix(self):
        return self.dictionary_.get(ProfileConfiguration.PREFIX)
    def readonly_prefixes(self):
        return self.dictionary_.get(ProfileConfiguration.READONLY_PREFIXES)
    def buildroot(self):
        return self.dictionary_.get(ProfileConfiguration.BUILDROOT)
    def short_libnames(self):
        return self.dictionary_.get(ProfileConfiguration.SHORT_LIBNAMES)
    def use_libtool(self):
        return self.dictionary_.get(ProfileConfiguration.USE_LIBTOOL)
    def use_bulk_install(self):
        return self.dictionary_.get(ProfileConfiguration.USE_BULK_INSTALL)
    def use_kde_hack(self):
        return self.dictionary_.get(ProfileConfiguration.USE_KDE_HACK)
    def verbosity(self):
        return self.dictionary_.get(ProfileConfiguration.VERBOSITY)
    def trace(self):
        return self.dictionary_.get(ProfileConfiguration.TRACE)
    def print_timings(self):
        return self.dictionary_.get(ProfileConfiguration.PRINT_TIMINGS)
    def message_prefix(self):
        return self.dictionary_.get(ProfileConfiguration.MESSAGE_PREFIX)
    def advanced(self):
        return self.dictionary_.get(ProfileConfiguration.ADVANCED)

    def configure_args(self):
        dict = self.dictionary_.get(ProfileConfiguration.CONFIGURE)
        if dict is None:
            return None
        return dict.get(ProfileConfiguration.ARGS)
    def configure_env(self):
        dict = self.dictionary_.get(ProfileConfiguration.CONFIGURE)
        if dict is None:
            return None
        return dict.get(ProfileConfiguration.ENV)

    def make_args(self):
        dict = self.dictionary_.get(ProfileConfiguration.MAKE)
        if dict is None:
            return None
        return dict.get(ProfileConfiguration.ARGS)
    def make_env(self):
        dict = self.dictionary_.get(ProfileConfiguration.MAKE)
        if dict is None:
            return None
        return dict.get(ProfileConfiguration.ENV)

    # we cannot say anything here because we are package-independent
    def packageroot(self): return None
    def packagename(self): return None
    def packageversion(self): return None
    def builddir(self): return None

    pass
