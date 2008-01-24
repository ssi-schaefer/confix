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

class Configuration:
    def __init__(self): pass

    def setups(self): assert 0, str(self.__class__)
    
    def packageroot(self): assert 0, str(self.__class__)
    def overlayroot(self): assert 0, str(self.__class__)
    
    def packagename(self): assert 0, str(self.__class__)
    def packageversion(self): assert 0, str(self.__class__)
    def builddir(self): assert 0, str(self.__class__)
    
    def prefix(self): assert 0, str(self.__class__)
    def readonly_prefixes(self): assert 0, str(self.__class__)
    def buildroot(self): assert 0, str(self.__class__)
    def short_libnames(self): assert 0, str(self.__class__)
    def use_libtool(self): assert 0, str(self.__class__)
    def use_bulk_install(self): assert 0, str(self.__class__)
    def use_kde_hack(self): assert 0, str(self.__class__)
    def print_timings(self): assert 0, str(self.__class__)
    def verbosity(self): assert 0, str(self.__class__)
    def trace(self): assert 0, str(self.__class__)
    def debug(self): assert 0, str(self.__class__)
    def message_prefix(self): assert 0, str(self.__class__)
    def advanced(self): assert 0, str(self.__class__)

    def configure_args(self): assert 0, str(self.__class__)
    def configure_env(self): assert 0, str(self.__class__)

    def make_args(self): assert 0, str(self.__class__)
    def make_env(self): assert 0, str(self.__class__)

    pass
