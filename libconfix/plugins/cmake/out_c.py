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

from buildinfo import BuildInfo_IncludePath_External_CMake
from buildinfo import BuildInfo_LibraryPath_External_CMake
from buildinfo import BuildInfo_Library_External_CMake
from buildinfo import BuildInfo_CommandlineMacros_CMake
from buildinfo import BuildInfo_CFLAGS_CMake
from buildinfo import BuildInfo_CXXFLAGS_CMake

from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.compiled import CompiledCBuilder
from libconfix.plugins.c.linked import LinkedBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeLocal
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils import const

import itertools

class COutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(HeaderOutputBuilder())
        dirbuilder.add_builder(CompiledOutputBuilder())
        dirbuilder.add_builder(LinkedOutputBuilder())
        pass
    pass

class HeaderOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(HeaderOutputBuilder, self).output()

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        # headers that have to be locally installed.
        # [('file', [rel-path])]
        local_install_info = []

        # headers that have to be publicly installed.
        # [('file', [rel-path])]
        public_install_info = []

        for header in self.parentbuilder().iter_builders():
            if not isinstance(header, HeaderBuilder):
                continue

            if header.public():
                public_install_info.append((header.file().name(), header.visibility()))
                pass

            package_visibility_action = header.package_visibility_action()
            assert package_visibility_action[0] in \
                   (HeaderBuilder.LOCALVISIBILITY_INSTALL, HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
            if package_visibility_action[0] == HeaderBuilder.LOCALVISIBILITY_INSTALL:
                local_install_info.append((header.file().name(), package_visibility_action[1]))
            elif package_visibility_action[0] is HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE:
                pass
            else:
                assert False, package_visibility_action[0]
                pass
            pass

        # publicly install headers
        for (file, installdir) in public_install_info:
            cmake_output_builder.local_cmakelists().add_install__files(files=[file], destination='/'.join(['include']+installdir))
            pass
        
        # locally install headers if necessary.
        if len(local_install_info):
            slashed_relpath = '/'.join(self.parentbuilder().directory().relpath(self.package().rootbuilder().directory()))
            dotted_relpath = '.'.join(self.parentbuilder().directory().relpath(self.package().rootbuilder().directory()))

            # ADD_CUSTOM_COMMAND() to link the headers to
            # confix-include and create a stamp file.
            if True:
                commands = []

                # create stamp directory.
                commands.append('${CMAKE_COMMAND} -E make_directory ${PROJECT_BINARY_DIR}/'+const.STAMP_DIR)
                # create install directories.
                for dir in sorted(set(('/'.join(visible_dir) for (file, visible_dir) in local_install_info))):
                    commands.append('${CMAKE_COMMAND} -E make_directory ${PROJECT_BINARY_DIR}/confix-include/'+dir)
                    pass
                # create symlinks for headers.
                for (file, visible_dir) in local_install_info:
                    commands.append('${CMAKE_COMMAND} -E create_symlink '
                                    '${PROJECT_SOURCE_DIR}/'+slashed_relpath+'/'+file+' '
                                    '${PROJECT_BINARY_DIR}/confix-include/'+'/'.join(visible_dir)+'/'+file)
                    pass
                # touch stamp file
                commands.append('${CMAKE_COMMAND} -E touch ${PROJECT_BINARY_DIR}/'+const.STAMP_DIR+'/local-header-install.'+dotted_relpath)
                
                cmake_output_builder.local_cmakelists().add_custom_command__output(
                    outputs=['${PROJECT_BINARY_DIR}/confix-stamps/local-header-install.'+dotted_relpath],
                    commands=commands,
                    depends=[file for (file, visible_dir) in local_install_info],
                    working_directory=None)
                pass

            # ADD_CUSTOM_TARGET(...ALL...) to hook local header
            # install to the toplevel directory build order.
            cmake_output_builder.local_cmakelists().add_custom_target(
                name='confix-local-install.'+dotted_relpath,
                all=True,
                depends=['${PROJECT_BINARY_DIR}/confix-stamps/local-header-install.'+dotted_relpath])
            pass
        pass
    pass

class CompiledOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def relate(self, node, digraph, topolist):
        super(CompiledOutputBuilder, self).relate(node, digraph, topolist)

        # reset all we gathered during the last round.
        self.__have_external_incpath = set()
        self.__external_incpath = []
        self.__external_cmdlinemacros = {}
        self.__external_cflags = []
        self.__external_cxxflags = []

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_IncludePath_External_CMake):
                    incpath = bi.incpath()
                    key = '.'.join(incpath)
                    if not key in self.__have_external_incpath:
                        self.__external_incpath.insert(0, incpath)
                        self.__have_external_incpath.add(key)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CommandlineMacros_CMake):
                    for (k, v) in bi.macros().iteritems():
                        existing_value = self.__external_cmdlinemacros.get(k)
                        if existing_value is not None and existing_value != v:
                            raise Error(os.sep.join(self.file().relpath())+': '
                                        'conflicting values for macro "'+key+'": '
                                        '"'+existing_value+'"/"'+value+'"')
                        self.__external_cmdlinemacros[k] = v
                        pass
                    continue
                if isinstance(bi, BuildInfo_CFLAGS_CMake):
                    self.__external_cflags.extend(bi.cflags())
                    continue
                if isinstance(bi, BuildInfo_CXXFLAGS_CMake):
                    self.__external_cxxflags.extend(bi.cxxflags())
                    continue
                pass
            pass

        pass

    def output(self):
        super(CompiledOutputBuilder, self).output()

        have_compiled = False

        native_local_include_dirs = []
        native_local_include_dirs_set = set()
        using_locally_installed_headers = False
        using_public_native_installed_headers = False

        for compiled_builder in self.parentbuilder().iter_builders():
            if not isinstance(compiled_builder, CompiledCBuilder):
                continue
            have_compiled = True
            for include_directory in compiled_builder.native_local_include_dirs():
                slashed_incdir = '/'.join(include_directory)
                if slashed_incdir in native_local_include_dirs_set:
                    continue
                native_local_include_dirs.append(slashed_incdir)
                native_local_include_dirs_set.add(slashed_incdir)
                pass
            if compiled_builder.have_locally_installed_includes():
                using_locally_installed_headers = True
                pass
            if compiled_builder.using_native_installed():
                using_public_native_installed_headers = True
                pass
            pass

        if not have_compiled:
            return

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        # if we have locally installed headers, add the
        # 'confix-include' directory to the include path.
        if using_locally_installed_headers:
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${PROJECT_BINARY_DIR}/'+const.LOCAL_INCLUDE_DIR)
            pass

        # in addition to the source directory, add the associated
        # build directory in case it contains generated headers
        # (automake has this built-in as it uses VPATH, and we don't
        # want to break with it).
        for dir in native_local_include_dirs:
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${'+self.package().name()+'_BINARY_DIR}/'+dir)
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${'+self.package().name()+'_SOURCE_DIR}/'+dir)
            pass

        # use our good old prefix/include if need be.
        if using_public_native_installed_headers:
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${CMAKE_INSTALL_PREFIX}/include')
            pass

        # include paths contributed by external library definitions.
        for p in self.__external_incpath:
            for item in p:
                cmake_output_builder.local_cmakelists().add_include_directory(item)
                pass
            pass

        # commandline macros floating in by external library
        # definitions.
        for macro, value in self.__external_cmdlinemacros.iteritems():
            if value is None:
                definition = '-D%s' % macro
            else:
                definition = '-D%s=%s' % (macro, value)
                pass
            cmake_output_builder.local_cmakelists().add_definitions([definition])
            pass

        # cflags and cxxflags, likewise
        cmake_output_builder.local_cmakelists().add_definitions(self.__external_cflags)
        cmake_output_builder.local_cmakelists().add_definitions(self.__external_cxxflags)
        pass
    pass

class LinkedOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    
    def relate(self, node, digraph, topolist):
        Builder.relate(self, node, digraph, topolist)

        self.__have_external_libpath = set()
        self.__external_libpath = []

        self.__have_external_libraries = set()
        self.__external_libraries = []

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_LibraryPath_External_CMake):
                    for p in reversed(bi.libpath()):
                        if p in self.__have_external_libpath:
                            continue
                        self.__have_external_libpath.add(p)
                        self.__external_libpath.insert(0, p)
                        pass
                    continue
                if isinstance(bi, BuildInfo_Library_External_CMake):
                    for l in reversed(bi.libs()):
                        if l in self.__have_external_libraries:
                            continue
                        self.__have_external_libraries.add(l)
                        self.__external_libraries.insert(0, l)
                        pass
                    continue
                pass
            pass

        pass

    def output(self):
        super(LinkedOutputBuilder, self).output()
        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        for linked in self.parentbuilder().iter_builders():
            if not isinstance(linked, LinkedBuilder):
                continue

            # add the linked entity.
            if True:
                if isinstance(linked, ExecutableBuilder):
                    target_name = linked.exename()
                    cmake_output_builder.local_cmakelists().add_executable(
                        target_name,
                        [member.file().name() for member in linked.members()])
                    if linked.what() == ExecutableBuilder.BIN:
                        cmake_output_builder.local_cmakelists().add_install__targets(
                            targets=[target_name],
                            destination='bin')
                        pass
                    pass
                elif isinstance(linked, LibraryBuilder):
                    target_name = linked.basename()
                    cmake_output_builder.local_cmakelists().add_library(
                        target_name,
                        [member.file().name() for member in linked.members()])
                    cmake_output_builder.local_cmakelists().add_install__targets(
                        targets=[target_name],
                        destination='lib')
                    pass
                else:
                    assert False, 'unknown LinkedBuilder type: '+str(linked)
                    pass
                pass

            # add libraries and linker paths if any.
            if True:
                native_local_libraries = []
                native_installed_libraries = []

                for bi in linked.topo_libraries():
                    if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                        native_local_libraries.append(bi.basename())
                        continue
                    if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                        native_installed_libraries.append(bi.basename())
                        continue
                    assert 0, 'missed some relevant build info type'
                    pass

                # if there are libraries that have been installed
                # natively using confix, then their path is added
                # first.
                if len(native_installed_libraries):
                    cmake_output_builder.local_cmakelists().add_link_directories(
                        ['${CMAKE_INSTALL_PREFIX}/lib'])
                    pass

                # next come the paths pointing to external libraries.
                if len(self.__external_libpath):
                    cmake_output_builder.local_cmakelists().add_link_directories(
                        self.__external_libpath)
                    pass

                link_libraries = []
                have = set()
                for lib in itertools.chain(native_local_libraries,
                                           native_installed_libraries,
                                           self.__external_libraries):
                    if lib in have:
                        continue
                    have.add(lib)
                    link_libraries.append(lib)
                    pass

                if len(link_libraries):
                    cmake_output_builder.local_cmakelists().target_link_libraries(
                        target_name, link_libraries)
                    pass
                pass
            pass

        pass
    pass

