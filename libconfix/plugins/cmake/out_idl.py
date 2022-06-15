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

from .out_cmake import find_cmake_output_builder

from libconfix.plugins.idl.builder import IDLBuilder

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder

class IDLOutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(IDLOutputBuilder())
        pass
    pass

class IDLOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def output(self):
        super(IDLOutputBuilder, self).output()

        output_builder = None
        
        for idl in self.parentbuilder().iter_builders():
            if type(idl) is not IDLBuilder:
                continue

            if output_builder is None:
                output_builder = find_cmake_output_builder(self.parentbuilder())
                assert output_builder is not None
                pass

            # public install
            output_builder.local_cmakelists().add_install__files(
                files=[idl.file().name()],
                destination='/'.join(['include']+idl.install_path()))

            # local install
            if True:
                destdir = '/'.join(['${PROJECT_BINARY_DIR}', 'confix-include']+idl.install_path())
                destfile = destdir+'/'+idl.file().name()
                destfile_all_target = '.'.join(['confix-local-install']+idl.install_path()+[idl.file().name()])
                sourcefile = '${CMAKE_CURRENT_SOURCE_DIR}/'+idl.file().name()

                # create rule for the IDL local install
                output_builder.local_cmakelists().add_custom_command__output(
                    outputs=[destfile],
                    commands=[
                        ('${CMAKE_COMMAND} -E make_directory '+destdir, []),
                        ('${CMAKE_COMMAND} -E copy '+sourcefile+' '+destfile, []),
                        ],
                    depends=[sourcefile],
                    )

                # hook IDL local install to the 'all' target.
                output_builder.local_cmakelists().add_custom_target(
                    name=destfile_all_target,
                    all=True,
                    depends=[destfile])
                pass
            pass
        pass

    pass

