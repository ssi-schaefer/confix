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

from base import CBaseBuilder
from compiled import CompiledCBuilder
from executable import ExecutableBuilder
from h import HeaderBuilder
from library import LibraryBuilder
from namefinder import ShortNameFinder, LongNameFinder
import helper

from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

import os
import types

class CClusterer(Builder):
    def __init__(self, namefinder):
        Builder.__init__(self)
        self.__namefinder = namefinder
        self.__libname = None
        self.__libtool_version_info = None

        self.__library = None
        # ExecutableBuilder objects, indexed by their center builders
        self.__executables = {}
        pass

    def shortname(self):
        return 'C.Clusterer'

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def set_libname(self, name):
        self.__libname = name
        if self.__library is not None:
            self.__library.set_basename(name)
            pass
        pass

    def set_libtool_version_info(self, version_tuple):
        self.__libtool_version_info = version_tuple
        if self.__library is not None:
            self.__library.set_version(version_tuple)
            pass
        pass

    def enlarge(self):
        super(CClusterer, self).enlarge()
        # copy what we will be iterating over because we will change
        # its size
        builders = []
        for b in self.parentbuilder().iter_builders():
            builders.append(b)
            pass
        for b in builders:
            if not isinstance(b, CBaseBuilder):
                continue

            # add headers to library if any
            if isinstance(b, HeaderBuilder):
                if self.__library is not None:
                    if b not in self.__library.members():
                        self.__library.add_member(b)
                        pass
                    pass
                continue

            # main C file. wrap an ExecutableBuilder around
            # it. liquidate a library in favor of the executable. if
            # the main C file is member of another executable that I
            # maintain, pull it out from there.
            if b.is_main():
                if self.__executables.has_key(b):
                    # already got that one.
                    continue

                # remove my center b from any other executables which
                # it happens to be a member of. (rationale: b may not
                # have been marked executable from the
                # beginning. rather, it is possible that anyone in the
                # game marks any C file executable, though that file
                # has been made the member of another executable
                # before.)
                for e in self.__executables.itervalues():
                    if b in e.members():
                        e.remove_member(b)
                        pass
                    pass
                
                center_stem, center_ext = os.path.splitext(b.file().name())
                if center_stem.startswith('_check'):
                    what = ExecutableBuilder.CHECK
                elif center_stem.startswith('_'):
                    what = ExecutableBuilder.NOINST
                else:
                    what = ExecutableBuilder.BIN
                    pass
                exename = b.exename()
                if exename is None:
                    exename = self.__namefinder.find_exename(
                        packagename=self.package().name(),
                        path=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
                        centername=center_stem)
                    pass
                exe = ExecutableBuilder(
                    center=b,
                    exename=exename,
                    what=what)
                self.parentbuilder().add_builder(exe)
                self.__executables[b] = exe

                # liquidate library, if any.
                if self.__library is not None:
                    self.parentbuilder().remove_builder(self.__library)
                    for m in self.__library.members():
                        exe.add_member(m)
                        pass
                    self.__library = None
                    pass

                continue

            # a compiled C builder
            assert not (self.__library and len(self.__executables))
            if not self.__library and len(self.__executables) == 0:
                if self.__libname is None:
                    libname = self.__namefinder.find_libname(
                        packagename=self.package().name(),
                        path=self.parentbuilder().directory().relpath(self.package().rootdirectory()))
                else:
                    libname = self.__libname
                    pass
                
                self.__library = LibraryBuilder(
                    basename=libname,
                    version=self.__libtool_version_info,
                    default_version=self.package().version())
                self.parentbuilder().add_builder(self.__library)
                pass
            if self.__library is not None:
                if b not in self.__library.members():
                    self.__library.add_member(b)
                    pass
                pass
            for e in self.__executables.itervalues():
                if b not in e.members():
                    e.add_member(b)
                    pass
                pass
            pass
        pass

    pass

class CClustererInterfaceProxy(InterfaceProxy):
    def __init__(self, clusterer):
        InterfaceProxy.__init__(self)
        self.__clusterer = clusterer
        self.add_global('LIBNAME', getattr(self, 'LIBNAME'))
        self.add_global('LIBRARY_VERSION', getattr(self, 'LIBRARY_VERSION'))
        pass

    def LIBNAME(self, name):
        if type(name) is not types.StringType:
            raise Error("LIBNAME(): 'name' argument must be a string")
        self.__clusterer.set_libname(name)
        pass

    def LIBRARY_VERSION(self, version):
        if type(version) not in [types.ListType, types.TupleType]:
            raise Error("LIBRARY_VERSION(): 'version' argument must be a tuple")
        if len(version) != 3:
            raise Error("LIBRARY_VERSION(): 'version' argument must be a tuple of 3 integers")
        for i in range(len(version)):
            if type(version[i]) is not types.IntType:
                raise Error("LIBRARY_VERSION(): part "+str(i)+" of version is not an integer")
            pass
        self.__clusterer.set_libtool_version_info(version)
        pass
    pass

class CClustererSetup(Setup):
    def __init__(self, short_libnames):
        Setup.__init__(self)
        if short_libnames == True:
            self.__namefinder = ShortNameFinder()
        else:
            self.__namefinder = LongNameFinder()
            pass
        pass

    def setup(self, dirbuilder):
        clusterer = CClusterer(namefinder=self.__namefinder)
        dirbuilder.add_builder(clusterer)
        dirbuilder.add_interface(CClustererInterfaceProxy(clusterer=clusterer))
        pass
    pass
