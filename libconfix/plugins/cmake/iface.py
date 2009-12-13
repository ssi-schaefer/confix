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

from out_cmake import find_cmake_output_builder
from external_library import ExternalLibraryBuilder
from buildinfo import BuildInfo_Toplevel_CMakeLists_Include
from buildinfo import BuildInfo_Toplevel_CMakeLists_FindCall
from buildinfo import BuildInfo_CommandlineMacros_CMake
from buildinfo import BuildInfo_CMakeModule
from buildinfo import BuildInfo_IncludePath_External_CMake
from pkg_config import PkgConfigLibraryBuilder

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

class CMakeInterfaceSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(CMakeInterfaceProxy(dirbuilder=dirbuilder))
        pass
    pass

class CMakeInterfaceProxy(InterfaceProxy):

    CMAKE_BUILDINFO_PROPAGATE = 0
    CMAKE_BUILDINFO_LOCAL = 1

    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)

        self.__dirbuilder = dirbuilder

        self.add_global('CMAKE_BUILDINFO_PROPAGATE',
                        getattr(self, 'CMAKE_BUILDINFO_PROPAGATE'))
        self.add_global('CMAKE_BUILDINFO_LOCAL',
                        getattr(self, 'CMAKE_BUILDINFO_LOCAL'))

        self.add_global('CMAKE_CMAKELISTS_ADD_INCLUDE',
                        getattr(self, 'CMAKE_CMAKELISTS_ADD_INCLUDE'))
        self.add_global('CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY',
                        getattr(self, 'CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY'))
        self.add_global('CMAKE_CMAKELISTS_ADD_FIND_CALL',
                        getattr(self, 'CMAKE_CMAKELISTS_ADD_FIND_CALL'))
        self.add_global('CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT',
                        getattr(self, 'CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT'))
        self.add_global('CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET',
                        getattr(self, 'CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET'))
        
        self.add_global('CMAKE_ADD_MODULE_FILE',
                        getattr(self, 'CMAKE_ADD_MODULE_FILE'))
        self.add_global('CMAKE_CMDLINE_MACROS',
                        getattr(self, 'CMAKE_CMDLINE_MACROS'))
        self.add_global('CMAKE_EXTERNAL_LIBRARY',
                        getattr(self, 'CMAKE_EXTERNAL_LIBRARY'))
        self.add_global('CMAKE_PKG_CONFIG_LIBRARY',
                        getattr(self, 'CMAKE_PKG_CONFIG_LIBRARY'))
        pass

    def CMAKE_CMAKELISTS_ADD_INCLUDE(self, include, flags):
        """
        Add an INCLUDE(include) command to the toplevel CMakeLists.txt
        file.

        If CMAKE_BUILDINFO_LOCAL is in flags, then it is added to the
        toplevel CMakeLists.txt file of the local package. If
        CMAKE_BUILDINFO_PROPAGATE is in flags, then it is added to the
        toplevel CMakeLists.txt file of the receiving package.
        """
        if type(include) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE(): "include" parameter must be a string')
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE(): "flags" parameter must be list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).top_cmakelists().add_include(include)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_Toplevel_CMakeLists_Include(include=include))
            pass
        pass

    def CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY(self, directory, flags):
        """
        Add an INCLUDE_DIRECTORIES(directory) command to the toplevel
        CMakeLists.txt file.

        If CMAKE_BUILDINFO_LOCAL is in flags, then it is added to the
        CMakeLists.txt file of the calling module. If
        CMAKE_BUILDINFO_PROPAGATE is in flags, then it is added to the
        CMakeLists.txt file of the receiving module.
        """
        if type(directory) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY(): "directory" parameter must be a string')
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY(): "flags" parameter must be list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).local_cmakelists().add_include_directory(directory)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_IncludePath_External_CMake(incpath=[directory]))
            pass
        pass

    def CMAKE_CMAKELISTS_ADD_FIND_CALL(self, find_call, flags):
        """
        Add a find call to the toplevel CMakeLists.txt file. A find
        call is simply a string, and you can add just about
        anything. It's just that the position matters.

        If CMAKE_BUILDINFO_LOCAL is in flags, then it is added to the
        toplevel CMakeLists.txt file of the local package. If
        CMAKE_BUILDINFO_PROPAGATE is in flags, then it is added to the
        toplevel CMakeLists.txt file of the receiving package.
        """
        if type(find_call) not in (str, tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_FIND_CALL(): "find_call" parameter must be str, list, or tuple')
        if type(find_call) is str:
            find_call = [find_call]
            pass
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_FIND_CALL(): "flags" parameter must be int, list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).top_cmakelists().add_find_call(find_call)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_Toplevel_CMakeLists_FindCall(find_call=find_call))
            pass
        pass

    def CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(self, outputs, commands, depends, working_directory=None):
        """
        Add a ADD_CUSTOM_COMMAND (OUTPUT signature) to the
        CMakeLists.txt file of the current directory.
        """
        if type(outputs) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(): "outputs" parameter must be a list or tuple')
        if type(commands) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(): "commands" parameter must be a list or tuple')
        if type(depends) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(): "depends" parameter must be a list or tuple')
        if working_directory is not None and type(working_directory) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(): "working_directory" must be None os string')
        find_cmake_output_builder(self.__dirbuilder).local_cmakelists().add_custom_command__output(
            outputs=outputs,
            commands=commands,
            depends=depends,
            working_directory=working_directory,
            )
        pass

    def CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(self, name, all, depends):
        """
        Add a ADD_CUSTOM_TARGET to the CMakeLists.txt file of the
        current directory.
        """
        if type(name) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(): "name" parameter must be a string')
        if type(depends) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(): "depends" parameter must be a list or tuple')
        find_cmake_output_builder(self.__dirbuilder).local_cmakelists().add_custom_target(
            name=name,
            all=all,
            depends=depends,
            )
        pass

    def CMAKE_ADD_MODULE_FILE(self, name, lines, flags):
        """
        Add a module file to the package.

        If CMAKE_BUILDINFO_LOCAL is in flags, then it is added to the
        toplevel CMakeLists.txt file of the local package. If
        CMAKE_BUILDINFO_PROPAGATE is in flags, then it is added to the
        toplevel CMakeLists.txt file of the receiving package.
        """
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_ADD_MODULE_FILE(): "flags" parameter must be int, list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).add_module_file(name, lines)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_CMakeModule(name=name, lines=lines))
            pass
        pass

    def CMAKE_CMDLINE_MACROS(self, macros, flags):
        """
        Add commandline macros to the CMakeLists.txt file, in the form
        of a call to ADD_DEFINITIONS().

        If CMAKE_BUILDINFO_LOCAL is in flags, then it is added to the
        CMakeLists.txt file of the calling (local) module. If
        CMAKE_BUILDINFO_PROPAGATE is in flags, then it is added to the
        CMakeLists.txt file of the receiving module.
        """
        if type(macros) is not dict:
            raise Error('CMAKE_CMDLINE_MACROS(): "macros" parameter must be dictionary')
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMDLINE_MACROS(): "flags" parameter must be int, list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            for macro, value in macros.iteritems():
                if value is None:
                    definition = '-D%s' % macro
                else:
                    definition = '-D%s=%s' % (macro, value)
                    pass
                find_cmake_output_builder(self.__dirbuilder).local_cmakelists().add_definitions([definition])
                pass
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_CommandlineMacros_CMake(macros=macros))
            pass
        pass

    def CMAKE_EXTERNAL_LIBRARY(self, incpath=[], libpath=[], libs=[],
                               cmdlinemacros={}, cflags=[], cxxflags=[]):
        if type(incpath) not in (list, tuple):
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'incpath' argument must be list or tuple")
        if type(libpath) not in (list, tuple):
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'libpath' argument must be list or tuple")
        if type(libs) not in (list, tuple):
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'libs' argument must be list or tuple")
        if type(cmdlinemacros) is not dict:
            raise Error("EXTERNAL_LIBRARY(): 'cmdlinemacros' argument must be a dictionary")
        if type(cflags) not in (list, tuple):
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'cflags' argument must be list or tuple")
        if type(cxxflags) not in (list, tuple):
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'cxxflags' argument must be list or tuple")

        self.__dirbuilder.add_builder(
            ExternalLibraryBuilder(incpath=incpath, libpath=libpath, libs=libs,
                                   cmdlinemacros=cmdlinemacros, cflags=cflags, cxxflags=cxxflags))
        pass

    def CMAKE_PKG_CONFIG_LIBRARY(self, packagename):
        if type(packagename) is not str:
            raise Error("CMAKE_PKG_CONFIG_LIBRARY(): 'packagename' argument must be a string")
        self.__dirbuilder.add_builder(PkgConfigLibraryBuilder(packagename=packagename))
        pass

    def CMAKE_LOCAL_CMAKELISTS(self):
        """
        Returns the object representing the CMakeLists.txt file of the
        current directory.
        """
        return find_cmake_output_builder(self.__dirbuilder).local_cmakelists()
        
    def CMAKE_TOP_CMAKELISTS(self):
        """
        Returns the object representing the CMakeLists.txt file of the
        package's root directory.
        """
        return find_cmake_output_builder(self.__dirbuilder).top_cmakelists()
        
    pass
