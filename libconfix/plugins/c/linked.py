# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.digraph import algorithm

from libconfix.plugins.c.buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled

class LinkedBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__members = set()
        # toplogically sorted list of build infos for all libraries
        # that we depend on.
        self.__buildinfo_topo_dependent_native_libs = []
        # build information for the libraries that we directly depend
        # on.
        self.__buildinfo_direct_dependent_native_libs = []
        pass

    def members(self):
        return self.__members

    def add_member(self, b):
        assert isinstance(b, FileBuilder)
        self.__members.add(b)
        pass

    def direct_libraries(self):
        """
        List of BuildInfo_CLibrary_NativeLocal and
        BuildInfo_CLibrary_NativeInstalled objects that describe the
        libraries that we directly depend upon.
        """
        return self.__buildinfo_direct_dependent_native_libs
    def topo_libraries(self):
        """
        List of BuildInfo_CLibrary_NativeLocal and
        BuildInfo_CLibrary_NativeInstalled objects that describe the
        libraries that we depend upon, topologically sorted.
        """
        return self.__buildinfo_topo_dependent_native_libs

    def relate(self, node, digraph, topolist):
        """
        Builder method. As a service (we do not do anthing meaningful
        with the information ourselves), we remember both the
        topologically sorted list of the libraries that we depend on,
        as well as the libraries that we directly depend on.
        """
        Builder.relate(self, node, digraph, topolist)

        self.__buildinfo_topo_dependent_native_libs = []
        self.__buildinfo_direct_dependent_native_libs = []

        nodes_with_library = algorithm.nearest_property(digraph=digraph, entrypoint=node, property=self.HaveLibraryProperty())
        for n in nodes_with_library:
            for bi in n.iter_buildinfos():
                if type(bi) in (BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_direct_dependent_native_libs.append(bi)
                    pass
                pass
            pass
        
        for n in topolist:
            for bi in n.iter_buildinfos():
                if type(bi) in (BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_topo_dependent_native_libs.insert(0, bi)
                    pass
                pass
            pass
        pass

    class HaveLibraryProperty:
        def have(self, node):
            for bi in node.iter_buildinfos():
                if type(bi) in (BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled):
                    return True
                pass
            return False
        pass

    pass
