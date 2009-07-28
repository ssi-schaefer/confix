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

class CMakeLists:
    def __init__(self):

        # {basename: [member-filename]}
        self.__library_definitions = {}

        pass

    def add_library_definition(self, basename, members):
        assert not self.__library_definitions.get(basename)
        self.__library_definitions[basename] = members
        pass

    def get_library_definition(self, basename):
        return self.__library_definitions.get(basename)

    def lines(self):
        lines = []
        for (basename, members) in self.__library_definitions.iteritems():
            lines.append('add_library(')
            lines.append('    '+basename)
            for m in members:
                lines.append('    '+m)
                pass
            lines.append(')')
            pass
        return lines

    pass
