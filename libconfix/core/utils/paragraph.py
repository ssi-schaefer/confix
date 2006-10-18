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

import md5

class Paragraph:

    """ A paragraph is a unit of lines of text, and has a unique
    fingerprint. """

    def __init__(self, lines):

        self.lines_ = lines

        md5sum = md5.new()
        for l in lines:
            md5sum.update(l)
            pass
        self.fingerprint_ = md5sum.hexdigest()
        pass

    def fingerprint(self): return self.fingerprint_
    def lines(self): return self.lines_

    pass

class ParagraphSet:

    """ Unordered set of paragraphs. """

    def __init__(self):
        self.dict_ = {}
        pass

    def add(self, paragraph):
        assert isinstance(paragraph, Paragraph)
        self.dict_.setdefault(paragraph.fingerprint(), paragraph)
        pass

    def update(self, other):
        self.dict_.update(other.dict_)
        pass
    
    def __add__(self, other):
        ret = ParagraphSet()
        ret.update(self)
        ret.update(other)
        return ret

    def lines_for_configure_ac(self):
        ret = []
        for p in self.dict_.values():
            ret.extend(['',
                        '# '+p.fingerprint()])
            ret.extend(p.lines())
            pass
        return ret

    def lines_for_acinclude_m4(self):
        return self.lines_for_configure_ac()

    pass

class OrderedParagraphSet:
    
    def __init__(self):
        self.sets_per_order_ = {}
        pass

    def add(self, paragraph, order):
        assert isinstance(paragraph, Paragraph)
        set = self.sets_per_order_.setdefault(order, ParagraphSet())
        set.add(paragraph)
        pass

    def update(self, other):
        assert isinstance(other, OrderedParagraphSet)
        for other_order, other_set in other.sets_per_order_.iteritems():
            my_set = self.sets_per_order_.get(other_order)
            if my_set:
                my_set.update(other_set)
            else:
                self.sets_per_order_[other_order] = other_set
                pass
            pass
        pass

    def __add__(self, other):

        ret = OrderedParagraphSet()
        ret.update(self)
        ret.update(other)
        return ret

    def lines_for_configure_ac(self):
        ret = []
        orders = self.sets_per_order_.keys()[:]
        orders.sort()
        for o in orders:
            ret.extend(['',
                        '# order: '+str(o)])
            ret.extend(self.sets_per_order_[o].lines_for_configure_ac())
            pass
        return ret

