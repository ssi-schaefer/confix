# $Id: pkg_installed.py,v 1.10 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2004 Salomon Automation

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

from package import Package
from core.marshalling import Marshallable, update_marshalling_data

class InstalledPackage(Package):

    def get_marshalling_data(self):
        assert self.name_ is not None
        return update_marshalling_data(
            marshalling_data=Package.get_marshalling_data(self),
            generating_class=InstalledPackage,
            attributes={'modules': self.modules_},
            version={'InstalledPackage': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['InstalledPackage']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.modules_ = data[Marshallable.ATTRIBUTES]['modules']
        Package.set_marshalling_data(self, data)
        pass

    def __init__(self, name, version, modules):

        Package.__init__(self,
                         name=name,
                         version=version)

        self.modules_ = modules
        pass

    def modules(self):

        """ Implementation of the abstract (sigh - wish I had a true
        language) base class method. """

        return self.modules_
        
