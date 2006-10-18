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

import types

from element import MakefileElement
import helper_automake

class Rule(MakefileElement):
    def __init__(self, targets, prerequisites=[], commands=[]):
        assert type(targets) is types.ListType
        assert len(targets)
        self.targets_ = targets[:]
        self.prerequisites_ = prerequisites[:]
        self.commands_ = commands[:]
        pass

    def targets(self):
        return self.targets_

    def prerequisites(self):
        return self.prerequisites_
    def add_prerequisite(self, p):
        self.prerequisites_.append(p)
        pass

    def commands(self):
        return self.commands_
    def add_command(self, c):
        self.commands_.append(c)
        pass
        
    def lines(self):
        targ_prereqlist = self.targets_[:]
        targ_prereqlist[-1] = targ_prereqlist[-1] + ':'
        targ_prereqlist.extend(self.prerequisites_)

        commandlist = []
        if self.commands_ is not None:
            for c in self.commands_:
                if type(c) is types.StringType:
                    commandlist.append('\t'+c)
                elif (type(c) is types.ListType) or (type(c) is types.TupleType):
                    commandlist.extend(['\t'+l for l in helper_automake.format_word_list(c)])
                else: assert 0
                pass
            pass
        
        return helper_automake.format_word_list(targ_prereqlist) + commandlist
    pass
