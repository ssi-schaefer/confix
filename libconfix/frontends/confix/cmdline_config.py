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

class CommandlineConfiguration(Configuration):
    def __init__(self,
                 configdir,
                 configfile,
                 profile,
                 packageroot,
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
                 message_prefix,
                 advanced,
                 make_args
                 ):
        self.configdir_ = configdir
        self.configfile_ = configfile
        self.profile_ = profile
        self.packageroot_ = packageroot
        self.packagename_ = packagename
        self.packageversion_ = packageversion
        self.prefix_ = prefix
        self.readonly_prefixes_ = readonly_prefixes
        self.buildroot_ = buildroot
        self.builddir_ = builddir
        self.short_libnames_ = short_libnames
        self.use_libtool_ = use_libtool
        self.use_bulk_install_ = use_bulk_install
        self.use_kde_hack_ = use_kde_hack
        self.print_timings_ = print_timings
        self.verbosity_ = verbosity
        self.trace_ = trace
        self.message_prefix_ = message_prefix
        self.advanced_ = advanced
        self.make_args_ = make_args
        pass

    # things that we read in order for other to have entry points into
    # *their* configuration
    def configdir(self): return self.configdir_
    def configfile(self): return self.configfile_
    def profile(self): return self.profile_

    # Configuration interface
    def setups(self): return None
    def packageroot(self): return self.packageroot_
    def packagename(self): return self.packagename_
    def packageversion(self): return self.packageversion_
    def prefix(self): return self.prefix_
    def readonly_prefixes(self): return self.readonly_prefixes_
    def buildroot(self): return self.buildroot_
    def builddir(self): return self.builddir_
    def short_libnames(self): return self.short_libnames_
    def use_libtool(self): return self.use_libtool_
    def use_bulk_install(self): return self.use_bulk_install_
    def use_kde_hack(self): return self.use_kde_hack_
    def print_timings(self): return self.print_timings_
    def verbosity(self): return self.verbosity_
    def trace(self): return self.trace_
    def message_prefix(self): return self.message_prefix_
    def advanced(self): return self.advanced_

    def configure_args(self): return None
    def configure_env(self): return None
    
    def make_args(self): return self.make_args_
    def make_env(self): return None
    
    pass
