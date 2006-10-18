# $Id: package.py,v 1.84 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2002 Salomon Automation

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

from core.marshalling import Marshallable

class Package(Marshallable):

    def get_marshalling_data(self):
        assert self.name_ is not None
        return {Marshallable.GENERATING_CLASS: Package,
                Marshallable.VERSIONS: {'Package': 1},
                Marshallable.ATTRIBUTES: {'name': self.name_,
                                          'version': self.version_}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Package']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.name_ = data[Marshallable.ATTRIBUTES]['name']
        self.version_ = data[Marshallable.ATTRIBUTES]['version']
        pass

    def __init__(self,
                 name = None,
                 version = None):

        self.name_ = name
        self.version_ = version

    def name(self): return self.name_
    def version(self): return self.version_
    def modules(self): assert 0, 'Package.modules() is abstract'

    def set_name_(self, name):

        """ If the name was left None in the constructor, then derived
        classes may call this method to set the name afterwards. The
        name is not subject to change, so this be called only
        once. """

        assert self.name_ is None
        self.name_ = name

    def set_version_(self, version):

        """ If the version was left None in the constructor, then
        derived classes may call this method to set the version
        afterwards. The name is not subject to change, so this be
        called only once. """

        assert self.version_ is None
        self.version_ = version
