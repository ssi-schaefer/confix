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

import types

class CMakeLists:
    def __init__(self):

        # CMake: project()
        # string
        self.__project = None

        # CMake: cmake_minimum_required()
        # {"name": "value"}
        self.__cmake_minimum_required = {}

        # CMake: include()
        # set("cmake-package-name")
        self.__includes = set()

        # CMake: add_subdirectory()
        # ["directory-name"]
        self.__subdirectories = []

        # CMake: add_library()
        # {"basename": ["member-filename"]}
        self.__libraries = {}

        # CMake: add_executable()
        # {"exename": ["member-filename"]}
        self.__executables = {}

        # CMake: target_link_libraries()
        # {"target": ["link-library"]}
        self.__target_link_libraries = {}

        # CMake: include_directories()
        # ["directory-name"]
        self.__include_directories = []

        # CMake: add_custom_command(OUTPUT ...)
        # [(['output'], ['command'], ['depends'], 'working_directory')]
        self.__custom_commands__output = []

        # CMake: add_custom_target()
        # [('name', bool all, ['depends'])]
        self.__custom_targets = []

        # CMake: set()
        # { "name": "value" }
        self.__sets = {}

        pass

    def set_project(self, project):
        self.__project = project
        pass
    def project(self):
        return self.__project

    def add_cmake_minimum_required(self, name, value):
        assert name not in self.__cmake_minimum_required
        self.__cmake_minimum_required[name] = value
        pass
    def get_cmake_minimum_required(self, name):
        return self.__cmake_minimum_required.get(name)

    def add_include(self, include):
        assert include not in self.__includes
        self.__includes.add(include)
        pass
    def includes(self):
        return self.__includes

    def add_subdirectory(self, directoryname):
        assert type(directoryname) is types.StringType
        self.__subdirectories.append(directoryname)
        pass
    def subdirectories(self):
        return self.__subdirectories

    def add_library(self, basename, members):
        assert basename not in self.__libraries
        self.__libraries[basename] = members
        pass
    def get_library(self, basename):
        return self.__libraries.get(basename)

    def add_executable(self, exename, members):
        assert exename not in self.__executables
        self.__executables[exename] = members
        pass
    def get_executable(self, exename):
        return self.__executables.get(exename)

    def target_link_libraries(self, target, basenames):
        assert target not in self.__target_link_libraries
        self.__target_link_libraries[target] = basenames
        pass
    def get_target_link_libraries(self, target):
        return self.__target_link_libraries.get(target)

    def add_include_directory(self, directoryname):
        assert type(directoryname) is types.StringType
        if directoryname in self.__include_directories:
            return
        self.__include_directories.append(directoryname)
        pass
    def include_directories(self):
        return self.__include_directories

    def add_custom_command__output(self, outputs, commands, depends, working_directory):
        assert len(outputs)
        self.__custom_commands__output.append((outputs, commands, depends, working_directory))
        pass

    def add_custom_target(self, name, all, depends):
        self.__custom_targets.append((name, all, depends))
        pass

    def add_set(self, name, value):
        assert not name in self.__sets
        self.__sets[name] = value
        pass
    def get_set(self, name):
        return self.__sets.get(name)

    def lines(self):
        lines = []

        # PROJECT()
        if self.__project is not None: # supposed to only be set in
                                       # toplevel file.
            lines.append('PROJECT('+self.__project+')')
            pass

        # CMAKE_MINIMUM_REQUIRED()
        for (name, value) in self.__cmake_minimum_required.iteritems():
            lines.append('CMAKE_MINIMUM_REQUIRED('+name+' '+value+')')
            pass

        # INCLUDE()
        for include in self.__includes:
            lines.append('INCLUDE('+include+')')
            pass

        # ADD_SUBDIRECTORY()
        for d in self.__subdirectories:
            lines.append('ADD_SUBDIRECTORY('+d+')')
            pass

        # ADD_LIBRARY()
        for (basename, members) in self.__libraries.iteritems():
            lines.append('ADD_LIBRARY(')
            lines.append('    '+basename)
            for m in members:
                lines.append('    '+m)
                pass
            lines.append(')')
            pass

        # ADD_EXECUTABLE()
        for (exename, members) in self.__executables.iteritems():
            lines.append('ADD_EXECUTABLE(')
            lines.append('    '+exename)
            for m in members:
                lines.append('    '+m)
                pass
            lines.append(')')
            pass

        # TARGET_LINK_LIBRARIES()
        for (target, libraries) in self.__target_link_libraries.iteritems():
            lines.append('TARGET_LINK_LIBRARIES(')
            lines.append('    '+target)
            for library in libraries:
                lines.append('    '+library)
                pass
            lines.append(')')
            pass

        # INCLUDE_DIRECTORIES()
        for directoryname in self.__include_directories:
            lines.append('INCLUDE_DIRECTORIES('+directoryname+')')
            pass

        # ADD_CUSTOM_COMMAND(OUTPUT ...)
        for (outputs, commands, depends, working_directory) in self.__custom_commands__output:
            lines.append('ADD_CUSTOM_COMMAND(')
            lines.append('    OUTPUT '+' '.join(outputs))
            for c in commands:
                lines.append('    COMMAND '+c)
                pass
            if len(depends):
                lines.append('    DEPENDS '+' '.join(depends))
                pass
            lines.append(')')
            pass

        # ADD_CUSTOM_TARGET()
        for (name, all, depends) in self.__custom_targets:
            lines.append('ADD_CUSTOM_TARGET(')
            lines.append('    '+name)
            if all:
                lines.append('    ALL')
                pass
            if len(depends):
                lines.append('    DEPENDS '+' '.join(depends))
                pass
            lines.append(')')
            pass

        # SET()
        for (name, value) in self.__sets.iteritems():
            lines.append('SET('+name+' '+value+')')
            pass
        
        return lines

    pass
