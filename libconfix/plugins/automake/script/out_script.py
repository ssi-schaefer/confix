# Copyright (C) 2009-2010 Joerg Faschingbauer

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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.script.builder import ScriptBuilder
from libconfix.core.machinery.builder import Builder

class AutomakeScriptOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    
    def output(self):
        super(AutomakeScriptOutputBuilder, self).output()

        output_builder = None

        for script in self.parentbuilder().iter_builders():
            if isinstance(script, ScriptBuilder):
                if output_builder is None:
                    output_builder = find_automake_output_builder(self.parentbuilder())
                    assert output_builder is not None
                    pass

                if script.what() == ScriptBuilder.BIN:
                    output_builder.makefile_am().add_bin_script(scriptname=script.file().name())
                elif script.what() == ScriptBuilder.CHECK:
                    output_builder.makefile_am().add_check_script(scriptname=script.file().name())
                else:
                    assert False
                    pass
                pass
            pass
        pass

    pass
