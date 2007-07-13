# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

from h import HeaderBuilder
from c import CBuilder
from cxx import CXXBuilder
from library import LibraryBuilder
from executable import ExecutableBuilder
from namefinder import LongNameFinder
from relocated_headers.master import Master

import os

class ExplicitInterfaceProxy(InterfaceProxy):

    def __init__(self, object, use_libtool):
        InterfaceProxy.__init__(self, object=object)

        self.__use_libtool = use_libtool
        
        self.add_global('H', getattr(self, 'H'))
        self.add_global('C', getattr(self, 'C'))
        self.add_global('CXX', getattr(self, 'CXX'))
        self.add_global('LIBRARY', getattr(self, 'LIBRARY'))

        self.add_global('EXECUTABLE_BIN', ExecutableBuilder.BIN)
        self.add_global('EXECUTABLE_CHECK', ExecutableBuilder.CHECK)
        self.add_global('EXECUTABLE_NOINST', ExecutableBuilder.NOINST)
        self.add_global('EXECUTABLE', getattr(self, 'EXECUTABLE'))
        pass

    def H(self, filename, install=[], relocate_to=None):
        h = HeaderBuilder(file=self.__find_file(filename))
        if install is not None:
            h.set_external_install_path(install)
            pass

        self.object().add_builder(h)

        if relocate_to is not None:
            try:
                the_path_to_relocate_to = helper.make_path(relocate_to)
            except Error, e:
                raise Error('H(): invalid "relocate_to" value', [e])
            self.object().add_builder(
                Master(filename=filename, directory=the_path_to_relocate_to))
        return h

    def C(self, filename):
        c = CBuilder(file=self.__find_file(filename))
        self.object().add_builder(c)
        return c

    def CXX(self, filename):
        cxx = CXXBuilder(file=self.__find_file(filename))
        self.object().add_builder(cxx)
        return cxx

    def LIBRARY(self, members, basename=None, libtool_version_info=None):
        the_basename = basename
        if the_basename is None:
            the_basename=LongNameFinder().find_libname(
                packagename=self.object().package().name(),
                path=self.object().directory().relpath(dir=self.object().package().rootdirectory()))
            pass
        library = LibraryBuilder(basename=the_basename,
                                 use_libtool=self.__use_libtool,
                                 libtool_version_info=libtool_version_info,
                                 libtool_release_info=self.object().package().version())
        for m in members:
            library.add_member(m)
            pass
        self.object().add_builder(library)
        return library

    def EXECUTABLE(self, center, members=[], exename=None, what=ExecutableBuilder.BIN):
        the_exename = exename
        if the_exename is None:
            center_stem, center_ext = os.path.splitext(center.file().name())
            the_exename = LongNameFinder().find_exename(
                packagename=self.object().package().name(),
                path=self.object().directory().relpath(dir=self.object().package().rootdirectory()),
                centername=center_stem)
            pass
        executable = ExecutableBuilder(center=center,
                                       exename=the_exename,
                                       what=what,
                                       use_libtool=self.__use_libtool)
        for m in members:
            executable.add_member(m)
            pass
        self.object().add_builder(executable)
        return executable
    
    def __find_file(self, filename):
        for name, entry in self.object().entries():
            if name == filename:
                return entry
            pass
        else:
            raise Error('File '+filename+' not found')
        pass

    pass
