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
from .c import CBuilder
from .cxx import CXXBuilder
from .lex import LexBuilder
from .yacc import YaccBuilder
from .library import LibraryBuilder
from .executable import ExecutableBuilder
from .clusterer import LongNameFinder
from .relocated_headers.master import Master

from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

import os

class ExplicitInterfaceProxy(InterfaceProxy):

    def __init__(self, dirbuilder):
        assert isinstance(dirbuilder, DirectoryBuilder)

        InterfaceProxy.__init__(self)

        self.__dirbuilder = dirbuilder

        self.add_global('H', getattr(self, 'H'))
        self.add_global('C', getattr(self, 'C'))
        self.add_global('CXX', getattr(self, 'CXX'))
        self.add_global('LEX', getattr(self, 'LEX'))
        self.add_global('YACC', getattr(self, 'YACC'))
        self.add_global('LIBRARY', getattr(self, 'LIBRARY'))

        self.add_global('EXECUTABLE_BIN', ExecutableBuilder.BIN)
        self.add_global('EXECUTABLE_CHECK', ExecutableBuilder.CHECK)
        self.add_global('EXECUTABLE_NOINST', ExecutableBuilder.NOINST)
        self.add_global('EXECUTABLE', getattr(self, 'EXECUTABLE'))
        pass

    def H(self, filename, install=[], public=None, relocate_to=None):
        if install is not None and type(install) is not list:
            raise Error("H(): 'install' parameter must be None or a list of strings")
        if type(filename) is not str:
            raise Error("H(): 'filename' parameter must be string")

        if public is not None and type(public) is not bool:
            raise Error("H(): 'public' parameter must be bool")
        
        h = HeaderBuilder(file=self.__find_file(filename))
        if install is not None:
            h.set_visibility(install)
            pass
        if public is not None:
            h.set_public(public)
            pass

        self.__dirbuilder.add_builder(h)

        if relocate_to is not None:
            try:
                the_path_to_relocate_to = helper.make_path(relocate_to)
            except Error as e:
                raise Error('H(): invalid "relocate_to" value', [e])
            self.__dirbuilder.add_builder(
                Master(filename=filename, directory=the_path_to_relocate_to))
            pass
        return h

    def C(self, filename):
        c = CBuilder(file=self.__find_file(filename))
        self.__dirbuilder.add_builder(c)
        return c

    def CXX(self, filename):
        cxx = CXXBuilder(file=self.__find_file(filename))
        self.__dirbuilder.add_builder(cxx)
        return cxx

    def LEX(self, filename):
        lex = LexBuilder(file=self.__find_file(filename))
        self.__dirbuilder.add_builder(lex)
        return lex

    def YACC(self, filename):
        yacc = YaccBuilder(file=self.__find_file(filename))
        self.__dirbuilder.add_builder(yacc)
        return yacc

    def LIBRARY(self, members, basename=None, version=None, undefined_symbols=True):
        the_basename = basename
        if the_basename is None:
            the_basename=LongNameFinder().find_libname(
                packagename=self.__dirbuilder.package().name(),
                path=self.__dirbuilder.directory().relpath(from_dir=self.__dirbuilder.package().rootdirectory()))
            pass
        library = LibraryBuilder(basename=the_basename,
                                 version=version,
                                 default_version=self.__dirbuilder.package().version(),
                                 has_undefined_symbols=undefined_symbols)
        for m in members:
            library.add_member(m)
            pass
        self.__dirbuilder.add_builder(library)
        return library

    def EXECUTABLE(self, center, members=[], exename=None, what=ExecutableBuilder.BIN):
        the_exename = exename
        if the_exename is None:
            center_stem, center_ext = os.path.splitext(center.file().name())
            the_exename = LongNameFinder().find_exename(
                packagename=self.__dirbuilder.package().name(),
                path=self.__dirbuilder.directory().relpath(from_dir=self.__dirbuilder.package().rootdirectory()),
                centername=center_stem)
            pass
        executable = ExecutableBuilder(center=center,
                                       exename=the_exename,
                                       what=what)
        for m in members:
            executable.add_member(m)
            pass
        self.__dirbuilder.add_builder(executable)
        return executable
    
    def __find_file(self, filename):
        for name, entry in self.__dirbuilder.directory().entries():
            if name == filename:
                return entry
            pass
        else:
            raise Error('File '+filename+' not found')
        pass

    pass
