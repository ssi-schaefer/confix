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

from h import HeaderBuilder
from c import CBuilder
from cxx import CXXBuilder
from library import LibraryBuilder
from executable import ExecutableBuilder
from namefinder import LongNameFinder

class ExplicitInterfaceProxy(InterfaceProxy):

    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('H', getattr(self, 'H'))
        self.add_global('C', getattr(self, 'C'))
        self.add_global('CXX', getattr(self, 'CXX'))
        self.add_global('LIBRARY', getattr(self, 'LIBRARY'))
        self.add_global('EXECUTABLE', getattr(self, 'EXECUTABLE'))
        pass

    def H(self, filename, install=[]):
        h = HeaderBuilder(file=self.__find_file(filename))
        if install is not None:
            h.set_external_install_path(install)
            pass

        self.__object.parentbuilder().add_builder(h)
        return h

    def C(self, filename):
        c = CBuilder(file=self.__find_file(filename))
        self.__object.parentbuilder().add_builder(c)
        return c

    def CXX(self, filename):
        cxx = CXXBuilder(file=self.__find_file(filename))
        self.__object.parentbuilder().add_builder(cxx)
        return cxx

    def LIBRARY(self, members, basename=None, libtool_version_info=None):
        the_basename = basename
        if the_basename is None:
            the_basename=LongNameFinder().find_libname(
                packagename=self.__object.package().name(),
                path=self.__object.parentbuilder().directory().relpath(dir=self.__object.package().rootdirectory()))
            pass
        library = LibraryBuilder(basename=the_basename,
                                 use_libtool=False, # todo: pass this
                                                    # from the setup
                                 libtool_version_info=libtool_version_info,
                                 libtool_release_info=self.__object.package().version())
        self.__object.parentbuilder().add_builder(library)
        return library

    def EXECUTABLE(self, center, exename=None, what=ExecutableBuilder.BIN):
        the_exename = exename
        if the_exename is None:
            the_exename = LongNameFinder().find_exename(
                packagename=self.__object.package().name(),
                path=self.__object.parentbuilder().directory().relpath(dir=self.__object.package().rootdirectory()),
                centername=center.file().name(),
                what=what,
                use_libtool=False # todo: pass this from the setup
                )
            pass
        # FIXME: libtool from setup object
        executable = ExecutableBuilder(center=center, exename=the_exename, what=what, use_libtool=False)
        return executable
    
    def __find_file(self, filename):
        for name, entry in self.__object.parentbuilder().entries():
            if name == filename:
                return entry
            pass
        else:
            raise Error('File '+filename+' not found')
        pass

    pass
