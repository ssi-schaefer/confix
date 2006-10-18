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

from base import CBaseBuilder
import namespace

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

import os

class HeaderBuilder(CBaseBuilder):
    PROPERTY_INSTALLPATH = 'INSTALLPATH_CINCLUDE'
    
    def __init__(self, file, parentbuilder, package):
        # we exec the iface in the ctor, so the relevant members have
        # to be available before this.
        self.iface_install_path_ = None
        
        CBaseBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            package=package)

        self.namespace_install_path_ = None
        pass

    def iface_install_path(self):
        return self.iface_install_path_
    def set_iface_install_path(self, path):
        self.iface_install_path_ = path
        pass

    def namespace_install_path(self):
        if self.namespace_install_path_ is None:
            self.namespace_install_path_ = namespace.find_unique_namespace(self.file().lines())
            pass
        return self.namespace_install_path_

    def property_install_path(self):
        if self.file() is not None:
            return self.file().get_property(HeaderBuilder.PROPERTY_INSTALLPATH)
        return None
    
    def iface_pieces(self):
        return CBaseBuilder.iface_pieces(self) + [HeaderBuilderInterfaceProxy(object=self)]
    pass

class HeaderBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('INSTALLPATH', getattr(self, 'INSTALLPATH'))
        pass
    def INSTALLPATH(self, path):
        self.object_.set_iface_install_path(helper.make_path(path))
        pass
    pass
