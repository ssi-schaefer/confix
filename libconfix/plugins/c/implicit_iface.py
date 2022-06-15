# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from .h import HeaderBuilder

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

import fnmatch
import re

class ExplicitInstaller(Builder):
    """
    Sit around and wait for user requests like,
    "Ey man, tell all HeaderBuilders that come along to install their files to 'some/directory'".

    User requests are usually those from an interface proxy sitting in
    Confix2.dir.
    """

    def __init__(self, installdir):
        Builder.__init__(self)
        self.__installdir = installdir
        self.__seen_header_builders = set()
        pass

    def locally_unique_id(self):
        return str(self.__class__.__name__)

    def enlarge(self):
        super(ExplicitInstaller, self).enlarge()
        if self.__installdir is None:
            return
        for b in self.parentbuilder().iter_builders():
            if type(b) is not HeaderBuilder:
                continue
            if b in self.__seen_header_builders:
                continue
            b.set_visibility(self.__installdir)
            self.__seen_header_builders.add(b)
            # we just have modified dependency information, so another
            # round must be made.
            self.force_enlarge()
            pass
        pass
    pass

class INSTALLDIR_H(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('INSTALLDIR_H', getattr(self, 'INSTALLDIR_H'))
        pass
    def INSTALLDIR_H(self, dir):
        try:
            the_dir = helper.make_path(dir)
        except Error as e:
            raise Error('INSTALLDIR_H(): dir argument must either '
                        'be a string or a list of path components', [e])
        self.__dirbuilder.add_builder(ExplicitInstaller(installdir=the_dir))
        pass
    pass

class SetHeaderPublic(Builder):
    def __init__(self, public, shellmatch=None, regex=None):
        Builder.__init__(self)
        self.__shellmatch = shellmatch
        if regex is not None:
            self.__regex = re.compile(regex)
        else:
            self.__regex = None
            pass
        self.__public = public
        self.__seen_headers = set()

        self.__id = str(self.__class__) + '(' + str(shellmatch) + ',' + str(regex) + ',' + str(self.__public) + ')'
        pass
    def locally_unique_id(self):
        return self.__id
    def enlarge(self):
        for header in self.parentbuilder().iter_builders():
            if type(header) is not HeaderBuilder:
                continue
            if header in self.__seen_headers:
                continue
            self.__seen_headers.add(header)
            if self.__shellmatch is not None and fnmatch.fnmatchcase(header.file().name(), self.__shellmatch):
                header.set_public(self.__public)
                pass
            if self.__regex is not None and self.__regex.search(header.file().name()):
                header.set_public(self.__public)
                pass
            pass
        pass
    pass

class SET_HEADER_PUBLIC(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('SET_HEADER_PUBLIC', getattr(self, 'SET_HEADER_PUBLIC'))
        pass
    def SET_HEADER_PUBLIC(self, public, regex=None, shellmatch=None):
        self.__dirbuilder.add_builder(SetHeaderPublic(shellmatch=shellmatch, regex=regex, public=public))
        pass
    pass

class ImplicitInterfaceSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(INSTALLDIR_H(dirbuilder=dirbuilder))
        dirbuilder.add_interface(SET_HEADER_PUBLIC(dirbuilder=dirbuilder))
        pass
    pass
