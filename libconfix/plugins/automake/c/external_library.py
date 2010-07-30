# Copyright (C) 2008-2009 Joerg Faschingbauer

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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.buildinfo import BuildInformation
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.machinery.repo import \
     update_marshalling_data, \
     MarshalledVersionUnknownError, \
     Marshallable

import types

class BuildInfo_IncludePath_External_AM(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_IncludePath_External_AM,
            attributes={'incpath': self.incpath_},
            version={'BuildInfo_IncludePath_External_AM': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_IncludePath_External_AM']
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

class BuildInfo_CFLAGS_AM(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CFLAGS_AM,
            attributes={'cflags': self.__cflags},
            version={'BuildInfo_CFLAGS_AM': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CFLAGS_AM']
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
        return self.__class__.__name__ + ':' + ','.join(self.__cflags)
    def cflags(self): return self.__cflags
    def install(self): return self
    pass

class BuildInfo_CXXFLAGS_AM(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CXXFLAGS_AM,
            attributes={'cxxflags': self.__cxxflags},
            version={'BuildInfo_CXXFLAGS_AM': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CXXFLAGS_AM']
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
        return self.__class__.__name__ + ':' + ','.join(self.__cxxflags)
    def cxxflags(self): return self.__cxxflags
    def install(self): return self
    pass

class BuildInfo_CommandlineMacros_AM(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_CommandlineMacros_AM,
            attributes={'macros': self.__macros},
            version={'BuildInfo_CommandlineMacros_AM': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_CommandlineMacros_AM']
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

class BuildInfo_Library_External_AM(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Library_External_AM,
            attributes={'libpath': self.__libpath,
                        'libs': self.__libs},
            version={'BuildInfo_Library_External_AM': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Library_External_AM']
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
    def __str__(self): return unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + ','.join(self.__libpath) + ':' + ','.join(self.__libs)
    def libpath(self): return self.__libpath
    def libs(self): return self.__libs
    def install(self): return self
    pass

class ExternalLibraryBuilder(Builder):
    def __init__(self,
                 name=None,
                 incpath=[],
                 cflags=[],
                 cxxflags=[],
                 cmdlinemacros={},
                 libpath=[],
                 libs=[]):
        Builder.__init__(self)

        self.__name = name
        self.__incpath = incpath
        self.__cflags = cflags
        self.__cxxflags = cxxflags
        self.__cmdlinemacros = cmdlinemacros
        self.__libpath = libpath
        self.__libs = libs
        pass

    def locally_unique_id(self):
        id = str(self.__class__)
        if self.__name is not None:
            id += ':'+self.__name
            pass
        return id

    def iter_buildinfos(self):
        for bi in super(ExternalLibraryBuilder, self).iter_buildinfos():
            yield bi
            pass
        
        if len(self.__incpath) > 0:
            yield BuildInfo_IncludePath_External_AM(incpath=self.__incpath)
            pass
        if len(self.__cflags) > 0:
            yield BuildInfo_CFLAGS_AM(cflags=self.__cflags)
            pass
        if len(self.__cxxflags) > 0:
            yield BuildInfo_CXXFLAGS_AM(cxxflags=self.__cxxflags)
            pass
        if len(self.__cmdlinemacros) > 0:
            yield BuildInfo_CommandlineMacros_AM(macros=self.__cmdlinemacros)
            pass
        if len(self.__libpath) > 0 or len(self.__libs) > 0:
            yield BuildInfo_Library_External_AM(libpath=self.__libpath, libs=self.__libs)
            pass

        pass
    
    pass

class EXTERNAL_LIBRARY(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('EXTERNAL_LIBRARY', getattr(self, 'EXTERNAL_LIBRARY'))
        pass
    def EXTERNAL_LIBRARY(self,
                         incpath=[],
                         cflags=[],
                         cxxflags=[],
                         cmdlinemacros={},
                         libpath=[],
                         libs=[]):

        if type(incpath) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'incpath' argument must be a list")
        if type(cflags) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'cflags' argument must be a list")
        if type(cxxflags) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'cxxflags' argument must be a list")
        if type(cmdlinemacros) is not types.DictionaryType:
            raise Error("EXTERNAL_LIBRARY(): 'cmdlinemacros' argument must be a dictionary")
        if type(libpath) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'libpath' argument must be a list")
        if type(libs) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'libs' argument must be a list")
                         
        self.__dirbuilder.add_builder(ExternalLibraryBuilder(incpath=incpath,
                                                             cflags=cflags,
                                                             cxxflags=cxxflags,
                                                             cmdlinemacros=cmdlinemacros,
                                                             libpath=libpath,
                                                             libs=libs))
        pass
    pass

class ExternalLibrarySetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(EXTERNAL_LIBRARY(dirbuilder=dirbuilder))
        pass
    pass
