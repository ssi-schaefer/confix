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

from .config import Configuration

class CommandlineConfiguration(Configuration):
    def __init__(self,
                 configdir,
                 configfile,
                 profile,
                 packageroot,
                 overlayroot,
                 packagename,
                 packageversion,
                 prefix,
                 readonly_prefixes,
                 buildroot,
                 builddir,
                 short_libnames,
                 use_libtool,
                 use_bulk_install,
                 use_kde_hack,
                 print_timings,
                 verbosity,
                 trace,
                 debug,
                 message_prefix,
                 advanced,
                 make_args
                 ):
        self.__configdir = configdir
        self.__configfile = configfile
        self.__profile = profile
        self.__packageroot = packageroot
        self.__overlayroot = overlayroot
        self.__packagename = packagename
        self.__packageversion = packageversion
        self.__prefix = prefix
        self.__readonly_prefixes = readonly_prefixes
        self.__buildroot = buildroot
        self.__builddir = builddir
        self.__short_libnames = short_libnames
        self.__use_libtool = use_libtool
        self.__use_bulk_install = use_bulk_install
        self.__use_kde_hack = use_kde_hack
        self.__print_timings = print_timings
        self.__verbosity = verbosity
        self.__trace = trace
        self.__debug = debug
        self.__message_prefix = message_prefix
        self.__advanced = advanced
        self.__make_args = make_args
        pass

    # things that we read in order for other to have entry points into
    # *their* configuration
    def configdir(self): return self.__configdir
    def configfile(self): return self.__configfile
    def profile(self): return self.__profile
    def debug(self): return self.__debug

    # Configuration interface
    def packageroot(self): return self.__packageroot
    def overlayroot(self): return self.__overlayroot
    def packagename(self): return self.__packagename
    def packageversion(self): return self.__packageversion
    def prefix(self): return self.__prefix
    def readonly_prefixes(self): return self.__readonly_prefixes
    def buildroot(self): return self.__buildroot
    def builddir(self): return self.__builddir
    def short_libnames(self): return self.__short_libnames
    def use_libtool(self): return self.__use_libtool
    def use_bulk_install(self): return self.__use_bulk_install
    def use_kde_hack(self): return self.__use_kde_hack
    def print_timings(self): return self.__print_timings
    def verbosity(self): return self.__verbosity
    def trace(self): return self.__trace
    def message_prefix(self): return self.__message_prefix
    def advanced(self): return self.__advanced

    def configure_args(self): return None
    def configure_env(self): return None
    
    def make_args(self): return self.__make_args
    def make_env(self): return None
    
    pass
