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

from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core.digraph import algorithm
from libconfix.core.machinery import readonly_prefixes
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.utils.paragraph import Paragraph, OrderedParagraphSet

from buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled, \
     BuildInfo_CLibrary_External

import sys

class LinkedBuilder(Builder):
    def __init__(self, use_libtool):
        Builder.__init__(self)

        self.__init_buildinfo()
        self.__members = set()
        self.__use_libtool = use_libtool
        pass

    def members(self):
        return self.__members

    def add_member(self, b):
        assert isinstance(b, FileBuilder)
        self.__members.add(b)
        pass

    def remove_member(self, b):
        self.__members.remove(b)
        pass

    def use_libtool(self):
        return self.__use_libtool

    def am_compound_name(self):

        """ To be implemented by derived classes like
        ExecutableBuilder, LibraryBuilder, and possibly other linked
        entities that participate in writing Makefile.am."""
        assert 0
        pass
    
    def buildinfo_direct_dependent_native_libs(self):
        return self.__buildinfo_direct_dependent_native_libs
    def buildinfo_topo_dependent_native_libs(self):
        return self.__buildinfo_topo_dependent_native_libs
    def external_libpath(self):
        return self.__external_libpath
    def external_libraries(self):
        return self.__external_libraries

    def relate(self, node, digraph, topolist):
        Builder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()

        # of the native (confix-built) libraries we remember both the
        # next successors that have a library (for libtool, which does
        # topological sorting by itself) and the toposorted list (if
        # we do not use libtool).

        # we do not know if an external library was built with
        # libtool, so we have to pass the full topolist in either
        # case.

        nodes_with_library = algorithm.nearest_property(digraph=digraph, entrypoint=node, property=HaveLibraryProperty())
        for n in nodes_with_library:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.__buildinfo_direct_dependent_native_libs.append(bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_direct_dependent_native_libs.append(bi)
                    continue
                pass
            pass
        
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.__buildinfo_topo_dependent_native_libs.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_topo_dependent_native_libs.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_External):
                    key = '.'.join(bi.libpath())
                    if not key in self.__have_external_libpath:
                        self.__have_external_libpath.add(key)
                        self.__external_libpath.insert(0, bi.libpath())
                        pass
                    self.__external_libraries.insert(0, bi.libs())
                    continue
                pass
            pass
        pass

    def output(self):
        Builder.output(self)
        if self.__use_libtool:
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_LIBTOOL_DLOPEN',
                                     'AC_LIBTOOL_WIN32_DLL',
                                     'AC_PROG_LIBTOOL']),
                order=Configure_ac.PROGRAMS)
            pass
        pass

    def get_linkline(self):
        """
        This method is used by derived classes (shared library and
        executable builder being the most prominent), in order to get
        the necessary libraries onto their linker command line.

        Returns a list of strings, like ['-L/blah -L/bloh/blah
        -lonelibrary -lanotherone']
        """
        native_paths = []
        native_libraries = []
        external_linkline = []
        using_installed_library = False

        if self.__do_deep_linking():
            native_libs_to_use = self.__buildinfo_topo_dependent_native_libs
        else:
            native_libs_to_use = self.__buildinfo_direct_dependent_native_libs
            pass

        for bi in native_libs_to_use:
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                native_paths.append('-L'+'/'.join(['$(top_builddir)']+bi.dir()))
                native_libraries.append('-l'+bi.name())
                continue
            if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                using_installed_library = True
                native_libraries.append('-l'+bi.name())
                continue
            assert 0
            pass

        if using_installed_library:
            native_paths.append('-L$(libdir)')
            native_paths.append('$('+readonly_prefixes.libpath_var+')')
            pass

        # in either case (libtool or not), we have to link all
        # external libraries. we cannot decide whether they are built
        # with libtool or not, so we cannot rely on libtool making our
        # toposort. (note both are lists of lists...)
        for elem in self.__external_libpath + self.__external_libraries:
            external_linkline.extend(elem)
            pass
            
        return native_paths + native_libraries + external_linkline
    
    def __init_buildinfo(self):
        self.__buildinfo_direct_dependent_native_libs = []
        self.__buildinfo_topo_dependent_native_libs = []
        self.__external_libpath = []
        self.__have_external_libpath = set()
        self.__external_libraries = []
        pass

    def __do_deep_linking(self):
        """
        Returns a boolean value indicating if deep linking is desired
        or not. 'Deep linking' means that the whole dependency graph
        is reflected on the command line, in a topologically sorted
        way. As opposed to flat linking (or how one calls it), where
        only the direct dependent libraries are mentioned.
        """
        if self.__use_libtool:
            if not sys.platform.startswith('interix'):
                # when linking anything with libtool, we don't need to
                # specify the whole topologically sorted list of
                # dependencies - libtool does that by itself (*). We
                # only specify the direct dependencies.

                # (*) It is still unclear to me what the Libtool
                # policy is. I suspect it relies on the fact that the
                # native linker permits unresolved references (GNU ld
                # is happy with them, at the very least).
                return False
            else:
                # on Interix, Parity
                # (http://sourceforge.net/projects/parity) does things
                # in a way that the Windows native linker is
                # invoked. That guy likes things rather explicit, and
                # is very particular about unresolved references:
                return True
            pass
        else:
            # not using libtool; doing a dumb static link.
            return True
        pass

    pass

class HaveLibraryProperty:
    def have(self, node):
        for bi in node.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal) or \
               isinstance(bi, BuildInfo_CLibrary_NativeInstalled) or \
               isinstance(bi, BuildInfo_CLibrary_External):
                return True
            pass
        return False
    pass
