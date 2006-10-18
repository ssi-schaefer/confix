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

from libconfix.core.buildinfo import BuildInformation
from libconfix.core.repo.marshalling import \
     update_marshalling_data, \
     Marshallable, \
     MarshalledVersionUnknownError

import types

class BuildInfo_CIncludePath_NativeLocal(BuildInformation):
    def __init__(self): BuildInformation.__init__(self)
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__
    def install(self): return singleton_buildinfo_cincludepath_nativeinstalled
    pass
singleton_buildinfo_cincludepath_nativelocal = BuildInfo_CIncludePath_NativeLocal()

class BuildInfo_CIncludePath_NativeInstalled(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CIncludePath_NativeInstalled,
            attributes={},
            version={'BuildInfo_CIncludePath_NativeInstalled': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CIncludePath_NativeInstalled']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self): BuildInformation.__init__(self)
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__
    def install(self): assert 0
    pass
singleton_buildinfo_cincludepath_nativeinstalled = BuildInfo_CIncludePath_NativeInstalled()

class BuildInfo_CIncludePath_External(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CIncludePath_External,
            attributes={'incpath': self.incpath_},
            version={'BuildInfo_CIncludePath_External': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CIncludePath_External']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.incpath_ = data[Marshallable.ATTRIBUTES]['incpath']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, incpath):
        BuildInformation.__init__(self)
        self.incpath_ = incpath
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + '.'.join(self.incpath_)
    def incpath(self): return self.incpath_
    def install(self): return self
    pass

class BuildInfo_CLibrary_NativeLocal(BuildInformation):
    def __init__(self, dir, name):
        BuildInformation.__init__(self)
        assert type(dir) is types.ListType
        self.dir_ = dir
        self.name_ = name
        self.unique_key_ = self.__class__.__name__ + ':' + '.'.join(self.dir_) + ':' + self.name_
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.unique_key_
    def dir(self): return self.dir_
    def name(self): return self.name_
    def install(self):
        return BuildInfo_CLibrary_NativeInstalled(self.name())
    pass

class BuildInfo_CLibrary_NativeInstalled(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CLibrary_NativeInstalled,
            attributes={'name': self.name_},
            version={'BuildInfo_CLibrary_NativeInstalled': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CLibrary_NativeInstalled']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.name_ = data[Marshallable.ATTRIBUTES]['name']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, name):
        BuildInformation.__init__(self)
        self.name_ = name
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + self.name_
    def name(self): return self.name_
    def install(self): assert 0
    pass

class BuildInfo_CLibrary_External(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CLibrary_External,
            attributes={'libpath': self.libpath_,
                        'libs': self.libs_},
            version={'BuildInfo_CLibrary_External': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CLibrary_External']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.libpath_ = data[Marshallable.ATTRIBUTES]['libpath']
        self.libs_ = data[Marshallable.ATTRIBUTES]['libs']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, libpath, libs):
        BuildInformation.__init__(self)
        self.libpath_ = libpath
        self.libs_ = libs
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.libpath_) + ':' + ','.join(self.libs_)
    def libpath(self): return self.libpath_
    def libs(self): return self.libs_
    def install(self): return self
    pass

class BuildInfo_CommandlineMacros(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CommandlineMacros,
            attributes={'macros': self.macros_},
            version={'BuildInfo_CommandlineMacros': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CommandlineMacros']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.macros_ = data[Marshallable.ATTRIBUTES]['macros']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, macros):
        BuildInformation.__init__(self)
        self.macros_ = macros
        pass
    def unique_key(self):
        ret = self.__class__.__name__ + ':'
        for k, v in self.macros_.iteritems():
            ret += k
            if v is not None:
                ret += v
                pass
            pass
        pass
    def macros(self): return self.macros_
    def install(self): return self
    pass

class BuildInfo_CFLAGS(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CFLAGS,
            attributes={'cflags': self.cflags_},
            version={'BuildInfo_CFLAGS': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CFLAGS']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.cflags_ = data[Marshallable.ATTRIBUTES]['cflags']
        BuildInformation.set_marshalling_data(self, data)
        pass
    
    def __init__(self, cflags):
        BuildInformation.__init__(self)
        self.cflags_ = cflags
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.cflags_)
    def cflags(self): return self.cflags_
    def install(self): return self
    pass

class BuildInfo_CXXFLAGS(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CXXFLAGS,
            attributes={'cxxflags': self.cxxflags_},
            version={'BuildInfo_CXXFLAGS': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CXXFLAGS']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.cxxflags_ = data[Marshallable.ATTRIBUTES]['cxxflags']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, cxxflags):
        BuildInformation.__init__(self)
        self.cxxflags_ = cxxflags
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.cxxflags_)
    def cxxflags(self): return self.cxxflags_
    def install(self): return self
    pass
