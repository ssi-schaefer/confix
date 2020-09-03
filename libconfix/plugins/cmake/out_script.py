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

from out_cmake import find_cmake_output_builder

from libconfix.plugins.script.builder import ScriptBuilder

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder

class ScriptOutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(ScriptOutputBuilder())
        pass
    pass

class ScriptOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def output(self):
        super(ScriptOutputBuilder, self).output()

        output_builder = None
        
        for script in self.parentbuilder().iter_builders():
            if type(script) is not ScriptBuilder:
                continue

            if output_builder is None:
                output_builder = find_cmake_output_builder(self.parentbuilder())
                assert output_builder is not None
                pass

            output_builder.local_cmakelists().add_install__programs(
                programs=[script.file().name()],
                destination='bin')
            pass
        pass

    pass

