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

class AutomakeScriptOutputBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__directory_output_builder = None
        pass
    
    def output(self):
        super(AutomakeScriptOutputBuilder, self).output()
        for b in self.parentbuilder().iter_builders():
            if isinstance(ScriptBuilder, b):
                if self.__directory_output_builder is None:
                    self.__directory_output_builder = find_directory_output_builder(self.parentbuilder())
                    assert self.__directory_output_builder is not None
                    pass

                self.__directory_output_builder.makefile_am().add_bin_script(scriptname=b.file().name())
                pass
            pass
        pass

    pass
