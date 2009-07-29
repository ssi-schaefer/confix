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
        self.__project = '[project-name-not-set]'

        # CMake: include()
        # set("cmake-package-name")
        self.__includes = set()

        # CMake: add_subdirectory()
        # ["directory-name"]
        self.__subdirectories = []

        # CMake: add_library()
        # {"basename": ["member-filename"]}
        self.__libraries = {}

        # CMake: target_link_libraries()
        # {"target": ["link-library"]}
        self.__target_link_libraries = {}

        # CMake: set()
        # { "name": "value" }
        self.__sets = {}

        pass

    def set_project(self, project):
        self.__project = project
        pass
    def project(self):
        return self.__project

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

    def target_link_libraries(self, target, basenames):
        assert target not in self.__target_link_libraries
        self.__target_link_libraries[target] = basenames
        pass
    def get_target_link_libraries(self, target):
        return self.__target_link_libraries.get(target)

    def add_set(self, name, value):
        assert not name in self.__sets
        self.__sets[name] = value
        pass
    def get_set(self, name):
        return self.__sets.get(name)

    def lines(self):
        lines = []

        # project()
        lines.append('project('+self.__project+')')

        # include()
        for include in self.__includes:
            lines.append('include('+include+')')
            pass

        # add_subdirectory()
        for d in self.__subdirectories:
            lines.append('add_subdirectory('+d+')')
            pass

        # add_library()
        for (basename, members) in self.__libraries.iteritems():
            lines.append('add_library(')
            lines.append('    '+basename)
            for m in members:
                lines.append('    '+m)
                pass
            lines.append(')')
            pass

        # target_link_libraries()
        for (target, libraries) in self.__target_link_libraries.iteritems():
            lines.append('target_link_libraries(')
            lines.append('    '+target)
            for library in libraries:
                lines.append('    '+library)
                pass
            lines.append(')')
            pass

        # set()
        for (name, value) in self.__sets.iteritems():
            lines.append('set('+name+' '+value+')')
            pass
        
        return lines

    pass
