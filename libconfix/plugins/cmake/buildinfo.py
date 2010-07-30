# Copyright (C) 2009 Joerg Faschingbauer

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
from libconfix.core.machinery.repo import \
     update_marshalling_data, \
     MarshalledVersionUnknownError, \
     Marshallable
from libconfix.core.utils import helper

class BuildInfo_IncludePath_External_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_IncludePath_External_CMake,
            attributes={'incpath': self.__incpath},
            version={'BuildInfo_IncludePath_External_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_IncludePath_External_CMake']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__incpath = data[Marshallable.ATTRIBUTES]['incpath']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, incpath):
        BuildInformation.__init__(self)
        self.__incpath = incpath
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + '.'.join(self.__incpath)
    def incpath(self): return self.__incpath
    def install(self): return self
    pass

class BuildInfo_LibraryPath_External_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_LibraryPath_External_CMake,
            attributes={'libpath': self.__libpath},
            version={'BuildInfo_LibraryPath_External_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_LibraryPath_External_CMake']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__libpath = data[Marshallable.ATTRIBUTES]['libpath']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, libpath):
        BuildInformation.__init__(self)
        self.__libpath = libpath
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + '.'.join(self.__libpath)
    def libpath(self): return self.__libpath
    def install(self): return self
    pass

class BuildInfo_Library_External_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Library_External_CMake,
            attributes={'libs': self.__libs},
            version={'BuildInfo_Library_External_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Library_External_CMake']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__libs = data[Marshallable.ATTRIBUTES]['libs']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, libs):
        BuildInformation.__init__(self)
        self.__libs = libs
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + '.'.join(self.__libs)
    def libs(self): return self.__libs
    def install(self): return self
    pass

class BuildInfo_CommandlineMacros_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CommandlineMacros_CMake,
            attributes={'macros': self.__macros},
            version={'BuildInfo_CommandlineMacros_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CommandlineMacros_CMake']
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
    def __str__(self): return unique_key()
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

class BuildInfo_Toplevel_CMakeLists_Include(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Toplevel_CMakeLists_Include,
            attributes={'include': self.__include},
            version={'BuildInfo_Toplevel_CMakeLists_Include': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Toplevel_CMakeLists_Include']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__include = data[Marshallable.ATTRIBUTES]['include']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, include):
        BuildInformation.__init__(self)
        self.__include = include
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return '%s:%s' %  (self.__class__.__name__, self.__include)
    def include(self): return self.__include
    def install(self): return self
    pass

class BuildInfo_Toplevel_CMakeLists_FindCall(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Toplevel_CMakeLists_FindCall,
            attributes={'find_call': self.__find_call},
            version={'BuildInfo_Toplevel_CMakeLists_FindCall': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Toplevel_CMakeLists_FindCall']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__find_call = data[Marshallable.ATTRIBUTES]['find_call']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, find_call):
        assert type(find_call) is list
        BuildInformation.__init__(self)
        self.__find_call = find_call
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return '%s:%s' %  (self.__class__.__name__, str(self.__find_call))
    def find_call(self): return self.__find_call
    def install(self): return self
    pass

class BuildInfo_CFLAGS_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CFLAGS_CMake,
            attributes={'cflags': self.__cflags},
            version={'BuildInfo_CFLAGS_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CFLAGS_CMake']
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
    def __str__(self): return unique_key()
    def unique_key(self):
        return '%s:%s' % (self.__class__.__name__, str(self.__cflags))
    def cflags(self): return self.__cflags
    def install(self): return self
    pass

class BuildInfo_CXXFLAGS_CMake(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CXXFLAGS_CMake,
            attributes={'cxxflags': self.__cxxflags},
            version={'BuildInfo_CXXFLAGS_CMake': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CXXFLAGS_CMake']
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
    def __str__(self): return unique_key()
    def unique_key(self):
        return '%s:%s' % (self.__class__.__name__, str(self.__cxxflags))
    def cxxflags(self): return self.__cxxflags
    def install(self): return self
    pass

class BuildInfo_CMakeModule(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CMakeModule,
            attributes={'name': self.__name,
                        'lines': self.__lines},
            version={'BuildInfo_CMakeModule': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CMakeModule']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__name = data[Marshallable.ATTRIBUTES]['name']
        self.__lines = data[Marshallable.ATTRIBUTES]['lines']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, name, lines):
        BuildInformation.__init__(self)
        self.__name = name
        self.__lines = lines
        pass
    def __str__(self): return unique_key()
    def unique_key(self):
        return '%s:%s:%s' % (self.__class__.__name__, self.__name, helper.md5_hexdigest_from_lines(self.__lines))
    def name(self): return self.__name
    def lines(self): return self.__lines
    def install(self): return self
    pass

