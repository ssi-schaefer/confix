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

from libconfix.core.repo.marshalling import Unmarshallable

from provide_string import Provide_String

class DependencySet(Unmarshallable):
    def __init__(self, klass, string_klass):
        self.klass_ = klass
        self.string_klass_ = string_klass

        # objects of type string_klass. sorted into a dictionary
        # {type -> {obj.string() -> obj}}
        self.string_ = {}
        pass

    def __len__(self): return self.size()
    def size(self):
        n = 0
        for k, v in self.string_.iteritems():
            n += len(v)
            pass
        return n

    def has(self, obj):
        assert isinstance(obj, self.klass_), obj
        if isinstance(obj, self.string_klass_):
            klass_dict = self.string_.get(obj.__class__)
            if klass_dict is None:
                return False
            existing_obj = klass_dict.get(obj.string())
            if existing_obj is None:
                return False
            if obj is existing_obj:
                return True
            return existing_obj.is_equal(obj)
        else:
            assert 0, 'not supported anymore (should be refactored)'
            pass
        pass

    def add(self, obj):
        assert isinstance(obj, self.klass_), obj
        if isinstance(obj, self.string_klass_):
            klass_dict = self.string_.setdefault(obj.__class__, {})
            existing_obj = klass_dict.get(obj.string())
            if existing_obj:
                if obj is not existing_obj:
                    existing_obj.update(obj)
                    pass
                pass
            else:
                klass_dict[obj.string()] = obj
                pass
            pass
        else:
            assert 0, 'not supported anymore (should be refactored)'
            pass
        pass

    def merge(self, other):
        for obj in other.values():
            self.add(obj)
            pass
        pass

    def __iter__(self): return self.values().__iter__()
    def values(self):
        for klass, klass_dict in self.string_.iteritems():
            for v in klass_dict.itervalues():
                yield v
                pass
            pass
        pass

    def is_equal(self, other):
        if self.size() != other.size():
            return False
        for obj in self.values():
            if not other.has(obj):
                return False
            pass
        return True

    pass
