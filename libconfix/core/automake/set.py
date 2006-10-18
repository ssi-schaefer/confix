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

from element import MakefileElement
import helper_automake
from backslash import BACKSLASH_MITIGATOR

class Set(MakefileElement):
    def __init__(self, name, values, mitigate):
        self.name_ = name
        self.values_ = set(values)
        self.mitigate_ = mitigate
        pass
    def __str__(self):
        return self.name_ + '=' + str(self.values_)
    def __iter__(self):
        return self.values_.__iter__()
    def __len__(self):
        return self.values_.__len__()
    def __contains__(self, value):
        return self.values_.__contains__(value)
    def name(self):
        return self.name_
    def values(self):
        return self.values_
    def add(self, value):
        self.values_.add(value)
        pass
    def lines(self):
        if len(self.values_) == 0:
            return []
        values = list(self.values_)
        values.sort()
        wordlist = [self.name_+' ='] + values
        if self.mitigate_:
            wordlist.append('$(CONFIX_BACKSLASH_MITIGATOR)')
            pass
        return helper_automake.format_word_list(wordlist)
    pass
