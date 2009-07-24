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

from external_library import \
     BuildInfo_IncludePath_External_AM, \
     BuildInfo_CFLAGS_AM, \
     BuildInfo_CXXFLAGS_AM, \
     BuildInfo_CommandlineMacros_AM, \
     BuildInfo_Library_External_AM
from libconfix.plugins.automake.configure_ac import Configure_ac
from libconfix.plugins.automake import readonly_prefixes
from libconfix.plugins.automake import helper
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.compiled import CompiledCBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.cxx import CXXBuilder
from libconfix.plugins.c.lex import LexBuilder
from libconfix.plugins.c.yacc import YaccBuilder
from libconfix.plugins.c.linked import LinkedBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils import const
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

import sys
import os

class COutputSetup(Setup):
    def __init__(self, use_libtool):
        Setup.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def setup(self, dirbuilder):
        dirbuilder.add_builder(HeaderOutputBuilder())
        dirbuilder.add_builder(CompiledOutputBuilder())
        dirbuilder.add_builder(COutputBuilder())
        dirbuilder.add_builder(CXXOutputBuilder())
        dirbuilder.add_builder(LexOutputBuilder())
        dirbuilder.add_builder(YaccOutputBuilder())
        dirbuilder.add_builder(LibraryOutputBuilder(use_libtool=self.__use_libtool))
        dirbuilder.add_builder(ExecutableOutputBuilder(use_libtool=self.__use_libtool))
        pass
    pass

class HeaderOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        super(HeaderOutputBuilder, self).output()
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, HeaderBuilder):
                continue

            public_visibility = b.public_visibility()
            local_visibility = b.local_visibility()

            automake_output_builder.file_installer().add_public_header(filename=b.file().name(), dir=public_visibility)

            assert local_visibility[0] in (HeaderBuilder.LOCAL_INSTALL, HeaderBuilder.DIRECT_INCLUDE)
            if local_visibility[0] == HeaderBuilder.LOCAL_INSTALL:
                automake_output_builder.file_installer().add_private_header(
                    filename=b.file().name(),
                    dir=local_visibility[1])
                pass
            pass
        pass
    pass

class CompiledOutputBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)

        self.__external_cflags = []
        self.__external_cmdlinemacros = {}

        # include path for external modules. this is a list of lists,
        # of the form

        # [['-I/dir1'],
        #  ['-I/this/dir/include', '-I/that/dir/include']]

        # each list has been distributed to us by one module, and we
        # must not change the order inside the individual lists - they
        # may be significant, and the distributing modules surely
        # don't expect us to mess with the order.

        # the complete list is accompanied with a set which serves us
        # to sort out duplicates from the beginning.
        
        self.__have_external_incpath = set()
        self.__external_incpath = []
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def relate(self, node, digraph, topolist):
        super(CompiledOutputBuilder, self).relate(node, digraph, topolist)

        # reset all we gathered during the last round.
        self.__have_external_incpath = set()
        self.__external_incpath = []
        self.__external_cflags = []
        self.__external_cmdlinemacros = {}

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_IncludePath_External_AM):
                    incpath = bi.incpath()
                    key = '.'.join(incpath)
                    if not key in self.__have_external_incpath:
                        self.__external_incpath.insert(0, incpath)
                        self.__have_external_incpath.add(key)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CFLAGS_AM):
                    self.__external_cflags.extend(bi.cflags())
                    continue
                if isinstance(bi, BuildInfo_CommandlineMacros_AM):
                    for (k, v) in bi.macros().iteritems():
                        existing_value = self.__external_cmdlinemacros.get(k)
                        if existing_value is not None and existing_value != v:
                            raise Error(os.sep.join(self.file().relpath())+': '
                                        'conflicting values for macro "'+key+'": '
                                        '"'+existing_value+'"/"'+value+'"')
                        self.__external_cmdlinemacros[k] = v
                        pass
                    continue
                pass
            pass
        pass

    def output(self):
        super(CompiledOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, CompiledCBuilder):
                continue

            # first, do the core confix things. then, add the
            # automake/external include paths, macros, and whatnot.

            for name, value in b.cmdlinemacros().iteritems():
                automake_output_builder.makefile_am().add_cmdlinemacro(name, value)
                pass
            for f in b.cflags():
                automake_output_builder.makefile_am().add_am_cflags(f)
                pass
    
            # native includes of the same package come first
            for d in b.native_local_include_dirs():
                automake_output_builder.makefile_am().add_includepath('-I'+'/'.join(['$(top_srcdir)']+d))
                pass
            # if files have been locally installed, we have to add
            # $(top_builddir)/confix_include to the include path.
            if b.have_locally_installed_includes():
                automake_output_builder.makefile_am().add_includepath('-I'+'/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR]))
                pass
            # native includes of other packages (i.e., native
            # installed includes) come next.
            if b.using_native_installed():
                automake_output_builder.makefile_am().add_includepath('-I$(includedir)')
                automake_output_builder.makefile_am().add_includepath('$('+readonly_prefixes.incpath_var+')')
                pass

            for name, value in self.__external_cmdlinemacros.iteritems():
                automake_output_builder.makefile_am().add_cmdlinemacro(name, value)
                pass
            for f in self.__external_cflags:
                automake_output_builder.makefile_am().add_am_cflags(f)
                pass
            for p in self.__external_incpath:
                for item in p:
                    automake_output_builder.makefile_am().add_includepath(item)
                    pass
                pass
            pass
        pass
    pass

class COutputBuilder(CompiledOutputBuilder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(COutputBuilder, self).output()
        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, CBuilder):
                continue
            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CC']),
                order=Configure_ac.PROGRAMS)
            pass
        pass
    pass

class CXXOutputBuilder(CompiledOutputBuilder):
    def __init__(self):
        CompiledOutputBuilder.__init__(self)
        self.__external_cxxflags = []
        pass
    
    def locally_unique_id(self):
        return str(self.__class__)
    
    def relate(self, node, digraph, topolist):
        super(CXXOutputBuilder, self).relate(node, digraph, topolist)
        self.__external_cxxflags = []
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CXXFLAGS_AM):
                    self.__external_cxxflags.extend(bi.cxxflags())
                    continue
                pass
            pass
        pass

    def output(self):
        super(CXXOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, CXXBuilder):
                continue

            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CXX']),
                order=Configure_ac.PROGRAMS)
            for f in b.cxxflags() + self.__external_cxxflags:
                automake_output_builder.makefile_am().add_am_cxxflags(f)
                pass
            pass
        pass
    pass

class LexOutputBuilder(CompiledOutputBuilder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LexOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, LexBuilder):
                continue

            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_LEX']),
                order=Configure_ac.PROGRAMS)
            root, ext = os.path.splitext(b.file().name())
            if ext == '.l':
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CC']),
                    order=Configure_ac.PROGRAMS)
                automake_output_builder.makefile_am().add_built_sources(root + '.c')
            elif ext == '.ll':
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CXX']),
                    order=Configure_ac.PROGRAMS)
                automake_output_builder.makefile_am().add_built_sources(root + '.cc')
                # argh: when using "%option c++" in the lex source
                # file, flex generates lex.yy.cc, which automake
                # doesn't seem to be aware of. force it to generate
                # the file automake is aware of. this is not supposed
                # to work with other lexers however. but, as the
                # documentation states, it is better to not use the
                # C++ feature of lex since it is inherently
                # non-portable anyway.
                automake_output_builder.makefile_am().add_am_lflags('-olex.yy.c')
            else:
                assert 0
                pass
            pass
        pass
    pass

class YaccOutputBuilder(CompiledOutputBuilder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(YaccOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, YaccBuilder):
                continue

            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_YACC']),
                order=Configure_ac.PROGRAMS)
            root, ext = os.path.splitext(b.file().name())
            if ext == '.y':
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CC']),
                    order=Configure_ac.PROGRAMS)
                automake_output_builder.makefile_am().add_built_sources(root + '.c')
            elif ext == '.yy':
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CXX']),
                    order=Configure_ac.PROGRAMS)
                automake_output_builder.makefile_am().add_built_sources(root + '.cc')
                # force Yacc to output files named y.tab.h
                automake_output_builder.makefile_am().add_am_yflags('-d');
            else:
                assert 0
                pass
            pass
        pass
    pass

class LinkedOutputBuilder(Builder):
    """
    In addition to what LibraryBuilder objects provide, gather
    information that is automake specific, and which is then used by
    derived classes like LibraryOutputBuilder and
    ExecutableOutputBuilder.
    """    
    def __init__(self, use_libtool):
        Builder.__init__(self)
        self.__use_libtool = use_libtool
        pass

    def relate(self, node, digraph, topolist):
        """
        Builder method. Gather the automake specific build
        information, such as BuildInfo_CLibrary_External.
        """
        Builder.relate(self, node, digraph, topolist)

        self.__external_libpath = []
        self.__have_external_libpath = set()
        self.__external_libraries = []

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_Library_External_AM):
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
        super(LinkedOutputBuilder, self).output()
        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, LinkedBuilder):
                continue
            
            if self.__use_libtool:
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_LIBTOOL_DLOPEN',
                                         'AC_LIBTOOL_WIN32_DLL',
                                         'AC_PROG_LIBTOOL']),
                    order=Configure_ac.PROGRAMS)
                pass
            pass
        pass

    def use_libtool(self):
        """
        For derived classes.
        """
        return self.__use_libtool

    def get_linkline(self, linked_builder):
        """
        For derived classes. Returns the link line for linked_builder,
        as a list of strings, like ['-L/blah -L/bloh/blah -lonelibrary
        -lanotherone']
        """
        assert isinstance(linked_builder, LinkedBuilder)
        
        native_paths = []
        native_libraries = []
        external_linkline = []
        using_installed_library = False

        if _linked_do_deep_linking(use_libtool=self.__use_libtool):
            native_libs_to_use = linked_builder.topo_libraries()
        else:
            native_libs_to_use = linked_builder.direct_libraries()
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
            assert 0, 'missed some relevant build info type'
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

    def external_libpath(self):
        """ For unit tests only. """
        return self.__external_libpath
    def external_libraries(self):
        """ For unit tests only. """
        return self.__external_libraries

    pass

class LibraryOutputBuilder(LinkedOutputBuilder):
    def __init__(self, use_libtool):
        LinkedOutputBuilder.__init__(self, use_libtool=use_libtool)
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LibraryOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, LibraryBuilder):
                continue

            if self.use_libtool():
                filelibname = 'lib'+b.basename()+'.la'
            else:
                filelibname = 'lib'+b.basename()+'.a'
                pass
            automakelibname = helper.automake_name(filelibname)

            if self.use_libtool():
                automake_output_builder.makefile_am().add_ltlibrary(filelibname)
                if b.version() is not None:
                    automake_output_builder.makefile_am().add_compound_ldflags(automakelibname, '-version-info %d:%d:%d' % b.version())
                elif b.default_version() is not None:
                    automake_output_builder.makefile_am().add_compound_ldflags(automakelibname, '-release '+b.default_version())
                    pass
                pass
            else:
                automake_output_builder.configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_RANLIB']),
                    order=Configure_ac.PROGRAMS)
                automake_output_builder.makefile_am().add_library(filelibname)
                pass

            for m in b.members():
                automake_output_builder.makefile_am().add_compound_sources(automakelibname, m.file().name())
                pass

            if self.use_libtool():
                for fragment in self.get_linkline(linked_builder=b):
                    automake_output_builder.makefile_am().add_compound_libadd(
                        compound_name=automakelibname,
                        lib=fragment)
                    pass
                pass
            pass
        pass
    pass

class ExecutableOutputBuilder(LinkedOutputBuilder):
    def __init__(self, use_libtool):
        LinkedOutputBuilder.__init__(self, use_libtool=use_libtool)
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(ExecutableOutputBuilder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, ExecutableBuilder):
                continue

            if b.what() == ExecutableBuilder.BIN:
                automake_output_builder.makefile_am().add_bin_program(b.exename())
            elif b.what() == ExecutableBuilder.CHECK:
                automake_output_builder.makefile_am().add_check_program(b.exename())
            elif b.what() == ExecutableBuilder.NOINST:
                automake_output_builder.makefile_am().add_noinst_program(b.exename())
            else: assert 0

            automakeexename = helper.automake_name(b.exename())

            for m in b.members():
                automake_output_builder.makefile_am().add_compound_sources(automakeexename, m.file().name())
                pass
            
            for fragment in self.get_linkline(linked_builder=b):
                automake_output_builder.makefile_am().add_compound_ldadd(
                    compound_name=automakeexename,
                    lib=fragment)
                pass
            pass
        pass
    pass

def _linked_do_deep_linking(use_libtool):
    """
    Returns a boolean value indicating if deep linking is desired or
    not. 'Deep linking' means that the whole dependency graph is
    reflected on the command line, in a topologically sorted way. As
    opposed to flat linking (or how one calls it), where only the
    direct dependent libraries are mentioned.
    """
    if use_libtool:
        if not sys.platform.startswith('interix'):
            # when linking anything with libtool, we don't need to
            # specify the whole topologically sorted list of
            # dependencies - libtool does that by itself (*). We only
            # specify the direct dependencies.

            # (*) It is still unclear to me what the Libtool policy
            # is. I suspect it relies on the fact that the native
            # linker permits unresolved references (GNU ld is happy
            # with them, at the very least).
            return False
        else:
            # on Interix, Parity
            # (http://sourceforge.net/projects/parity) does things in
            # a way that the Windows native linker is invoked. That
            # guy likes things rather explicit, and is very particular
            # about unresolved references:
            return True
        pass
    else:
        # not using libtool; doing a dumb static link.
        return True
    pass

