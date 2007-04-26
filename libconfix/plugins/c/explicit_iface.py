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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error

from h import HeaderBuilder
from c import CBuilder
from cxx import CXXBuilder

class ExplicitInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('H', getattr(self, 'H'))
        self.add_global('C', getattr(self, 'C'))
        self.add_global('CXX', getattr(self, 'CXX'))
        pass

    def H(self, filename, install=[]):
        h = HeaderBuilder(file=self.__find_file(filename))
        if install is not None:
            h.set_external_install_path(install)
            pass

        self.__object.add_builder(h)
        return h

    def C(self, filename):
        c = CBuilder(file=self.__find_file(filename))
        self.__object.add_builder(c)
        return c

    def CXX(self, filename):
        cxx = CXXBuilder(file=self.__find_file(filename))
        self.__object.add_builder(cxx)
        return cxx

    def LIBRARY(self, members):
        argh

    def __find_file(self, filename):
        for f in self.__object.parentbuilder().entries():
            if f.name() == filename:
                return f
            pass
        else:
            raise Error('File '+filename+' not found')
        pass

    pass
