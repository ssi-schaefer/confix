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

from repo import Unmarshallable
from require import Require
from provide import Provide

from libconfix.core.utils.error import Error

class DependencySet(Unmarshallable):
    def __init__(self):
        # objects of type string_klass. sorted into a dictionary
        # {type -> {obj.string() -> obj}}
        self.__per_class_index = {}
        pass

    def __len__(self): return self.size()
    def size(self):
        n = 0
        for k, v in self.__per_class_index.iteritems():
            n += len(v)
            pass
        return n

    def has(self, obj):
        klass_dict = self.__per_class_index.get(obj.__class__)
        if klass_dict is None:
            return False
        existing_obj = klass_dict.get(obj.string())
        if existing_obj is None:
            return False
        if obj is existing_obj:
            return True
        return existing_obj.is_equal(obj)

    def add(self, obj):
        unique_id = obj.string()
        klass_dict = self.__per_class_index.setdefault(obj.__class__, {})
        existing_obj = klass_dict.get(unique_id)
        if existing_obj:
            if obj is not existing_obj:
                existing_obj.update(obj)
                pass
            pass
        else:
            klass_dict[unique_id] = obj
            pass
        pass

    def merge(self, other):
        for obj in other:
            self.add(obj)
            pass
        pass

    def __iter__(self): return self.__iter_values()        
    def __iter_values(self):
        for klass, klass_dict in self.__per_class_index.iteritems():
            for v in klass_dict.itervalues():
                yield v
                pass
            pass
        pass

    def is_equal(self, other):
        if self.size() != other.size():
            return False
        for obj in self.__iter_values():
            if not other.has(obj):
                return False
            pass
        return True

    pass

class DependencyInformation(Unmarshallable):

    def __init__(self):

        self.__requires = DependencySet()
        self.__provides = DependencySet()

        # a set of provide objects that can be resolved internal to a
        # module. rationale: local C and h source files include local
        # header files like #include "file.h". the source file
        # scanning stuff can not know that this is not a real require
        # object because it does not know that file.h is present
        # locally, and produces a require object for each local
        # include. these molest the dependency graph calculation a
        # lot, so we have to weed them out. we do this by maintaining
        # this set of "internal" provide objects, which are basically
        # our local header files. (BuildableHeader is responsible for
        # filling it.)

        self.__internal_provides = DependencySet()
        pass

    def size(self):
        return self.__requires.size() + \
               self.__provides.size() + \
               self.__internal_provides.size()

    def requires(self): return self.__requires
    def provides(self): return self.__provides
    def internal_provides(self): return self.__internal_provides

    def add_require(self, r): self.__requires.add(r)
    def add_provide(self, p): self.__provides.add(p)
    def add_internal_provide(self, p): self.__internal_provides.add(p)

    def add_requires(self, rs):
        for r in rs:
            self.__requires.add(r)
            pass
        pass
    def add_provides(self, provides):
        for p in provides:
            self.__provides.add(p)
            pass
        pass
    def add_internal_provides(self, provides):
        for p in provides:
            self.__internal_provides.add(p)
            pass
        pass
    def add(self, other):
        assert isinstance(other, self.__class__), str(other.__class__)
        self.__requires.merge(other.__requires)
        self.__provides.merge(other.__provides)
        self.__internal_provides.merge(other.__internal_provides)
        return self

    def is_equal(self, other):
        return self.__provides.is_equal(other.__provides) and \
               self.__internal_provides.is_equal(other.__internal_provides) and \
               self.__requires.is_equal(other.__requires)
    pass

class ProvideMap(Unmarshallable):

    def __init__(self):
        # dictionary: require-type -> ProvideMap.Index_Provide
        self.__string_indexes = {}
        pass

    def find_match(self, require):
        ret_nodes = []
        index = self.__string_indexes.get(require.__class__)
        if index:
            ret_nodes.extend(index.find_match(require))
            pass
        return ret_nodes
        
    def add(self, provide, node):
        for require_type in provide.can_match_classes():
            index = self.__string_indexes.get(require_type)
            if not index:
                index = ProvideMap.Index_Provide()
                self.__string_indexes[require_type] = index
                pass
            index.add(provide, node)
            pass
        pass

    class Index_Provide(Unmarshallable):

        def __init__(self):
            # map string -> Node
            self.__exact = {}
    
            # list of tuples (glob-provide, node)
            self.__glob = []

            # negative lookup cache. we remember the strings of the
            # require objects that we haven't been able to resolve.
            self.__negative_lookups = set()

            pass
    
        def n_exact(self): return len(self.__exact)
        def n_glob(self): return len(self.__glob)
    
        def find_match(self, require):
    
            """
            Try to match the given require object against what I have.
    
            @return: A Node object if one is found, else None
            """
            ret_nodes = []
            key = require.string()
            if key not in self.__negative_lookups:
                node = self.__exact.get(key)
                if node:
                    ret_nodes.append(node)
                    pass
                for p, n in self.__glob:
                    if p.resolve(require):
                        ret_nodes.append(n)
                        pass
                    pass
                if len(ret_nodes) == 0:
                    self.__negative_lookups.add(key)
                    pass
                pass
            return ret_nodes
    
        def add(self, provide, node):
            if provide.match() == Provide.EXACT_MATCH:
                existing_node = self.__exact.get(provide.string())
                if existing_node:
                    raise Error('Conflict: '+str(provide)+' of node '+str(node)+' already provided by node '+str(existing_node))
                self.__exact[provide.string()] = node
            elif provide.match() == Provide.GLOB_MATCH:
                self.__glob.append((provide, node))
                pass
            pass
        pass

    pass
