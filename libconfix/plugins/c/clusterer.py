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
import helper

from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.utils.error import Error

import itertools
import os
import types

class CClustererSetup(Setup):
    def __init__(self, linkednamefinder=None, has_undefined_symbols=True):
        assert linkednamefinder is None or isinstance(linkednamefinder, NameFinder)
        Setup.__init__(self)
        if linkednamefinder is None:
            self.__namefinder = LongNameFinder()
        else:
            self.__namefinder = linkednamefinder
            pass
        self.__has_undefined_symbols = has_undefined_symbols
        pass

    def setup(self, dirbuilder):
        clusterer = CClusterer(namefinder=self.__namefinder, has_undefined_symbols=self.__has_undefined_symbols)
        dirbuilder.add_builder(clusterer)
        dirbuilder.add_interface(CClustererInterfaceProxy(clusterer=clusterer))
        pass
    pass

class CClusterer(Builder):
    def __init__(self, namefinder, has_undefined_symbols=True):
        Builder.__init__(self)
        self.__namefinder = namefinder
        self.__libname = None
        self.__libtool_version_info = None
        self.__has_undefined_symbols = has_undefined_symbols
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
        for builder in self.parentbuilder().iter_builders():
            if isinstance(builder, LibraryBuilder):
                builder.set_basename(name)
                break
            pass
        pass

    def set_libtool_version_info(self, version_tuple):
        self.__libtool_version_info = version_tuple
        for builder in self.parentbuilder().iter_builders():
            if isinstance(builder, LibraryBuilder):
                builder.set_version(version_tuple)
                break
            pass
        pass

    def set_has_undefined_symbols(self, has_undefined_symbols):
        self.__has_undefined_symbols = has_undefined_symbols
        for builder in self.parentbuilder().iter_builders():
            if isinstance(builder, LibraryBuilder):
                builder.set_has_undefined_symbols(has_undefined_symbols)
                break
            pass
        pass

    def enlarge(self):
        super(CClusterer, self).enlarge()

        main_builders = []
        nomain_builders = []
        header_builders = []

        executables = []
        library = None

        for builder in self.parentbuilder().iter_builders():
            if type(builder) is ExecutableBuilder:
                executables.append(builder)
                continue
            if type(builder) is LibraryBuilder:
                assert library is None
                library = builder
                continue

            # attention: we use direct __class__ comparison for
            # performance. to check for CBaseBuilder we have to use
            # isinstance() though because it is a base class.
            if not isinstance(builder, CBaseBuilder):
                continue

            if type(builder) is HeaderBuilder:
                header_builders.append(builder)
                continue

            # same attention.
            if not isinstance(builder, CompiledCBuilder):
                continue

            if builder.is_main():
                main_builders.append(builder)
                continue
            nomain_builders.append(builder)
            pass

        if not self.__do_recluster(main_builders=main_builders,
                                   nomain_builders=nomain_builders,
                                   header_builders=header_builders,
                                   library=library,
                                   executables=executables):
            return

        self.force_enlarge()

        if library:
            self.parentbuilder().remove_builder(library)
        else:
            for exe in executables:
                self.parentbuilder().remove_builder(exe)
                pass
            pass

        if len(main_builders):
            for main in main_builders:
                exetype = self.__make_exe_type(main)
                exename = self.__make_exe_name(main)
                exe = self.parentbuilder().add_builder(ExecutableBuilder(center=main, exename=exename, what=exetype))
                for b in itertools.chain(nomain_builders, header_builders):
                    exe.add_member(b)
                    pass
                pass
            return

        if self.__libname is None:
            libname = self.__namefinder.find_libname(
                packagename=self.package().name(),
                path=self.parentbuilder().directory().relpath(self.package().rootdirectory()))
        else:
            libname = self.__libname
            pass
        library = self.parentbuilder().add_builder(
            LibraryBuilder(
                basename=libname,
                version=self.__libtool_version_info,
                default_version=self.package().version(),
                has_undefined_symbols=self.__has_undefined_symbols))
        for b in itertools.chain(nomain_builders, header_builders):
            library.add_member(b)
            pass
        pass

    def __do_recluster(self, main_builders, nomain_builders, header_builders, library, executables):
        if len(main_builders) > 0 and library:
            return True
        if len(main_builders) == 0 and len(nomain_builders) > 0 and not library:
            return True
        if library and len(nomain_builders) + len(header_builders) != len(library.members()):
            return True
        if len(main_builders) != len(executables):
            return True
        for exe in executables:
            if len(exe.members()) != len(nomain_builders) + len(header_builders) + 1:
                return True
            pass
        return False

    def __make_exe_type(self, main_builder):
        center_stem, center_ext = os.path.splitext(main_builder.file().name())
        if center_stem.startswith('_check'):
            return ExecutableBuilder.CHECK
        if center_stem.startswith('_'):
            return ExecutableBuilder.NOINST
        return ExecutableBuilder.BIN

    def __make_exe_name(self, main_builder):
        center_stem, center_ext = os.path.splitext(main_builder.file().name())
        exename = main_builder.exename()
        if exename is None:
            return self.__namefinder.find_exename(
                packagename=self.package().name(),
                path=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
                centername=center_stem)
        return exename

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
        for i in xrange(len(version)):
            if type(version[i]) is not types.IntType:
                raise Error("LIBRARY_VERSION(): part "+str(i)+" of version is not an integer")
            pass
        self.__clusterer.set_libtool_version_info(version)
        pass

    def HAS_UNDEFINED_SYMBOLS(self, has_undefined_symbols):
        if type(has_undefined_symbols) is not types.BooleanType:
            raise Error("HAS_UNDEFINED_SYMBOLS(): 'has_undefined_symbols' argument must be a boolean")
        self.__clusterer.set_has_undefined_symbols(has_undefined_symbols)
        pass

    pass

class NameFinder:
    def __init__(self):
        pass
    def find_exename(self, packagename, path, centername):
        assert 0, 'abstract'
        return 'some_string'
    def find_libname(self, packagename, path):
        assert 0, 'abstract'
        return 'some_string'
    pass

class LongNameFinder(NameFinder):
    def __init__(self):
        NameFinder.__init__(self)
        pass
    def find_exename(self, packagename, path, centername):
        return '_'.join([packagename] + path + [centername])
    def find_libname(self, packagename, path):
        return '_'.join([packagename] + path)
    pass
