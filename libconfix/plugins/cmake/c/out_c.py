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

from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.compiled import CompiledCBuilder
from libconfix.plugins.c.linked import LinkedBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeLocal

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils import const

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

        # collect the headers that have to be locally installed.
        # [('file', [rel-path])]
        local_install_info = []
        
        for h in self.parentbuilder().iter_builders():
            if not isinstance(h, HeaderBuilder):
                continue

            local_visibility = h.local_visibility()

            assert local_visibility[0] in (HeaderBuilder.LOCAL_INSTALL, HeaderBuilder.DIRECT_INCLUDE)
            if local_visibility[0] == HeaderBuilder.LOCAL_INSTALL:
                local_install_info.append((h.file().name(), local_visibility[1]))
                pass
            pass

        if len(local_install_info):
            slashed_relpath = '/'.join(self.parentbuilder().directory().relpath(self.package().rootbuilder().directory()))
            dotted_relpath = '.'.join(self.parentbuilder().directory().relpath(self.package().rootbuilder().directory()))
            cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

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

    def output(self):
        super(CompiledOutputBuilder, self).output()

        native_local_include_dirs = []
        native_local_include_dirs_set = set()
        have_locally_installed_headers = False

        for compiled_builder in self.parentbuilder().iter_builders():
            if not isinstance(compiled_builder, CompiledCBuilder):
                continue
            for include_directory in compiled_builder.native_local_include_dirs():
                slashed_incdir = '/'.join(include_directory)
                if slashed_incdir in native_local_include_dirs_set:
                    continue
                native_local_include_dirs.append(slashed_incdir)
                native_local_include_dirs_set.add(slashed_incdir)
                pass
            if compiled_builder.have_locally_installed_includes():
                have_locally_installed_headers = True
                pass
            pass

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        # if we have locally installed headers, add the
        # 'confix-include' directory to the include path.
        if have_locally_installed_headers:
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${PROJECT_BINARY_DIR}/'+const.LOCAL_INCLUDE_DIR)
            pass

        for dir in native_local_include_dirs:
            # in addition to the source directory, add the associated
            # build directory in case it contains generated headers
            # (automake has this built-in as it uses VPATH, and we
            # don't want to break with it).
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${'+self.package().name()+'_BINARY_DIR}/'+dir)
            cmake_output_builder.local_cmakelists().add_include_directory(
                '${'+self.package().name()+'_SOURCE_DIR}/'+dir)
            pass
        pass
    pass

class LinkedOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    
    def output(self):
        super(LinkedOutputBuilder, self).output()
        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())
        for linked in self.parentbuilder().iter_builders():
            if not isinstance(linked, LinkedBuilder):
                continue

            # add the linked entity.
            if isinstance(linked, ExecutableBuilder):
                target_name = linked.exename()
                cmake_output_builder.local_cmakelists().add_executable(
                    target_name,
                    [member.file().name() for member in linked.members()])
            elif isinstance(linked, LibraryBuilder):
                target_name = linked.basename()
                cmake_output_builder.local_cmakelists().add_library(
                    target_name,
                    [member.file().name() for member in linked.members()])
            else:
                assert False, 'unknown LinkedBuilder type: '+str(linked)
                pass

            # add dependencies if any.
            native_local_libraries = []
            for bi in linked.topo_libraries():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    native_local_libraries.append(bi.name())
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    assert False, "implement me!"
                    continue
                assert 0, 'missed some relevant build info type'
                pass
            if len(native_local_libraries):
                cmake_output_builder.local_cmakelists().target_link_libraries(target_name, native_local_libraries)
                pass

            pass
        pass

    pass
