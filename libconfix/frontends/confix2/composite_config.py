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

class CompositeConfiguration(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        self.configurations_ = []
        pass

    def add(self, config):
        self.configurations_.append(config)
        pass

    def packageroot(self): return self.search_param_('packageroot')
    def overlayroot(self): return self.search_param_('overlayroot')
    def packagename(self): return self.search_param_('packagename')
    def packageversion(self): return self.search_param_('packageversion')
    def prefix(self): return self.search_param_('prefix')
    def readonly_prefixes(self): return self.search_param_('readonly_prefixes')
    def buildroot(self): return self.search_param_('buildroot')
    def builddir(self): return self.search_param_('builddir')
    def short_libnames(self): return self.search_param_('short_libnames')
    def use_libtool(self): return self.search_param_('use_libtool')
    def use_bulk_install(self): return self.search_param_('use_bulk_install')
    def use_kde_hack(self): return self.search_param_('use_kde_hack')
    def verbosity(self): return self.search_param_('verbosity')
    def trace(self): return self.search_param_('trace')
    def debug(self): return self.search_param_('debug')
    def print_timings(self): return self.search_param_('print_timings')
    def message_prefix(self): return self.search_param_('message_prefix')
    def advanced(self): return self.search_param_('advanced')
    def configure_args(self): return self.search_param_('configure_args')
    def configure_env(self): return self.search_param_('configure_env')
    def make_args(self): return self.search_param_('make_args')
    def make_env(self): return self.search_param_('make_env')

    def search_param_(self, methodname):
        for config in self.configurations_:
            ret = getattr(config, methodname)()
            if ret is not None:
                return ret
            pass
        else:
            return ret
        pass
    pass
