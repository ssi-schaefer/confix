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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.plainfile.builder import PlainFileBuilder
from libconfix.core.machinery.builder import Builder

class AutomakePlainfileOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def output(self):
        super(AutomakePlainfileOutputBuilder, self).output()

        output_builder = None
        
        for b in self.parentbuilder().iter_builders():
            if isinstance(b, PlainFileBuilder):

                if output_builder is None:
                    output_builder = find_automake_output_builder(self.parentbuilder())
                    assert output_builder is not None
                    pass

                if b.datadir() is not None:
                    output_builder.file_installer().add_datafile(
                        filename=b.file().name(),
                        dir=b.datadir())
                elif b.prefixdir() is not None:
                    output_builder.file_installer().add_prefixfile(
                        filename=b.file().name(),
                        dir=b.prefixdir())
                else:
                    assert 0
                    pass

                pass
            pass
        pass

    pass
