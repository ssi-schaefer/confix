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

from libconfix.plugins.c.compiled import CompiledCBuilder
from libconfix.plugins.c.linked import LinkedBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeLocal

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder

class COutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(CompiledOutputBuilder())
        dirbuilder.add_builder(LinkedOutputBuilder())
        pass
    pass

class CompiledOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def output(self):
        super(CompiledOutputBuilder, self).output()

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        for compiled_builder in self.parentbuilder().iter_builders():
            if not isinstance(compiled_builder, CompiledCBuilder):
                continue
            for include_directory in compiled_builder.native_local_include_dirs():
                # in addition to the source directory, add the
                # associated build directory in case it contains
                # generated headers (automake has this built-in, and
                # we don't want to break with it).
                directory_name = '/'.join(include_directory)
                cmake_output_builder.local_cmakelists().add_include_directory(
                    '${'+self.package().name()+'_BINARY_DIR}/'+directory_name)
                cmake_output_builder.local_cmakelists().add_include_directory(
                    '${'+self.package().name()+'_SOURCE_DIR}/'+directory_name)
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
