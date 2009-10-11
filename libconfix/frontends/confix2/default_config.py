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

import os

from config import Configuration

class DefaultConfiguration(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        pass

    def packageroot(self): return os.getcwd()
    def overlayroot(self): return None
    def packagename(self): return None
    def packageversion(self): return None
    def prefix(self): return None
    def readonly_prefixes(self): return []
    def buildroot(self): return None
    def builddir(self): return None
    def short_libnames(self): return False
    def use_libtool(self): return False
    def use_bulk_install(self): return False
    def use_kde_hack(self): return False
    def verbosity(self): return 0
    def trace(self): return []
    def debug(self): return None
    def print_timings(self): return False
    def message_prefix(self): return None
    def advanced(self): return False

    def configure_args(self): return None
    def configure_env(self): return None

    def make_args(self): return None
    def make_env(self): return None

    pass
