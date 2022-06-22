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

from libconfix.core.machinery.buildinfo import BuildInformation
from libconfix.core.machinery.repo import Marshallable, update_marshalling_data

import types

class BuildInfo_IDL_Native(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_IDL_Native,
            attributes={'filename': self.filename_,
                        'includes': self.includes_},
            version={'BuildInfo_IDL_Native': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_IDL_Native']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.filename_ = data[Marshallable.ATTRIBUTES]['filename']
        self.includes_ = data[Marshallable.ATTRIBUTES]['includes']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self,
                 filename,
                 includes):
        BuildInformation.__init__(self)
        assert filename.__class__ is str
        self.filename_ = filename
        self.includes_ = includes
        pass
    def filename(self): return self.filename_
    def includes(self): return self.includes_

    def unique_key(self): return self.__class__.__name__ + ':' + self.filename_
    pass

class BuildInfo_IDL_NativeLocal(BuildInfo_IDL_Native):
    def __init__(self,
                 filename,
                 includes):
        BuildInfo_IDL_Native.__init__(self,
                                      filename=filename,
                                      includes=includes)
    def install(self):
        return BuildInfo_IDL_NativeInstalled(
            filename=self.filename(),
            includes=self.includes())
    pass

class BuildInfo_IDL_NativeInstalled(BuildInfo_IDL_Native):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInfo_IDL_Native.get_marshalling_data(self),
            generating_class=BuildInfo_IDL_NativeInstalled,
            attributes={},
            version={'BuildInfo_IDL_NativeInstalled': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_IDL_NativeInstalled']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        BuildInfo_IDL_Native.set_marshalling_data(self, data)
        pass

    def __init__(self,
                 filename,
                 includes):
        BuildInfo_IDL_Native.__init__(self,
                                      filename=filename,
                                      includes=includes)
        pass
    def install(self): assert 0
    pass
