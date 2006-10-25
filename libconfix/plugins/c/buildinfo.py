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

from libconfix.core.machinery.buildinfo import BuildInformation
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
        self.__dir = dir
        self.__name = name
        self.__unique_key = self.__class__.__name__ + ':' + '.'.join(self.__dir) + ':' + self.__name
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__unique_key
    def dir(self): return self.__dir
    def name(self): return self.__name
    def install(self):
        return BuildInfo_CLibrary_NativeInstalled(self.name())
    pass

class BuildInfo_CLibrary_NativeInstalled(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CLibrary_NativeInstalled,
            attributes={'name': self.__name},
            version={'BuildInfo_CLibrary_NativeInstalled': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CLibrary_NativeInstalled']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__name = data[Marshallable.ATTRIBUTES]['name']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, name):
        BuildInformation.__init__(self)
        self.__name = name
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + self.__name
    def name(self): return self.__name
    def install(self): assert 0
    pass

class BuildInfo_CLibrary_External(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CLibrary_External,
            attributes={'libpath': self.__libpath,
                        'libs': self.__libs},
            version={'BuildInfo_CLibrary_External': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CLibrary_External']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__libpath = data[Marshallable.ATTRIBUTES]['libpath']
        self.__libs = data[Marshallable.ATTRIBUTES]['libs']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, libpath, libs):
        BuildInformation.__init__(self)
        self.__libpath = libpath
        self.__libs = libs
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.__libpath) + ':' + ','.join(self.__libs)
    def libpath(self): return self.__libpath
    def libs(self): return self.__libs
    def install(self): return self
    pass

class BuildInfo_CommandlineMacros(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CommandlineMacros,
            attributes={'macros': self.__macros},
            version={'BuildInfo_CommandlineMacros': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CommandlineMacros']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__macros = data[Marshallable.ATTRIBUTES]['macros']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, macros):
        BuildInformation.__init__(self)
        self.__macros = macros
        pass
    def unique_key(self):
        ret = self.__class__.__name__ + ':'
        for k, v in self.__macros.iteritems():
            ret += k
            if v is not None:
                ret += v
                pass
            pass
        pass
    def macros(self): return self.__macros
    def install(self): return self
    pass

class BuildInfo_CFLAGS(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CFLAGS,
            attributes={'cflags': self.__cflags},
            version={'BuildInfo_CFLAGS': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CFLAGS']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__cflags = data[Marshallable.ATTRIBUTES]['cflags']
        BuildInformation.set_marshalling_data(self, data)
        pass
    
    def __init__(self, cflags):
        BuildInformation.__init__(self)
        self.__cflags = cflags
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.__cflags)
    def cflags(self): return self.__cflags
    def install(self): return self
    pass

class BuildInfo_CXXFLAGS(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CXXFLAGS,
            attributes={'cxxflags': self.__cxxflags},
            version={'BuildInfo_CXXFLAGS': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CXXFLAGS']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__cxxflags = data[Marshallable.ATTRIBUTES]['cxxflags']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, cxxflags):
        BuildInformation.__init__(self)
        self.__cxxflags = cxxflags
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.__cxxflags)
    def cxxflags(self): return self.__cxxflags
    def install(self): return self
    pass
