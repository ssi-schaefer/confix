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
from require import Require_String
from provide import Provide
from provide import Provide_String

from ..utils.error import Error

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

class DependencyInformation(Unmarshallable):

    def __init__(self):

        self.requires_ = DependencySet(klass=Require, string_klass=Require_String)
        self.provides_ = DependencySet(klass=Provide, string_klass=Provide_String)

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

        self.internal_provides_ = DependencySet(klass=Provide, string_klass=Provide_String)
        pass

    def size(self):
        return self.requires_.size() + \
               self.provides_.size() + \
               self.internal_provides_.size()

    def requires(self): return self.requires_
    def provides(self): return self.provides_
    def internal_provides(self): return self.internal_provides_

    def add_require(self, r): self.requires_.add(r)
    def add_provide(self, p): self.provides_.add(p)
    def add_internal_provide(self, p): self.internal_provides_.add(p)

    def add_requires(self, rs):
        for r in rs:
            self.requires_.add(r)
            pass
        pass
    def add_provides(self, provides):
        for p in provides:
            self.provides_.add(p)
            pass
        pass
    def add_internal_provides(self, provides):
        for p in provides:
            self.internal_provides_.add(p)
            pass
        pass
    def add(self, other):
        assert isinstance(other, self.__class__), str(other.__class__)
        self.requires_.merge(other.requires_)
        self.provides_.merge(other.provides_)
        self.internal_provides_.merge(other.internal_provides_)
        return self

    def is_equal(self, other):
        return self.provides_.is_equal(other.provides_) and \
               self.internal_provides_.is_equal(other.internal_provides_) and \
               self.requires_.is_equal(other.requires_)
    pass

class ProvideMap(Unmarshallable):

    def __init__(self, permissive):

        # permissive means to return as soon as we have at least one
        # match (to return as soon as possible, so to say), and to not
        # continue to search for more.

        self.__permissive = permissive

        # dictionary: require-type -> ProvideMap.Index_Provide_String

        self.__string_indexes = {}

        # list of tuples (provide-object, Node) (use is deprecated)
        
        self.__rest = []

        pass

    def find_match(self, require):

        # see if a string index claims to know how to match the
        # require

        ret_nodes = []

        index = self.__string_indexes.get(require.__class__)
        if index:
            ret_nodes.extend(index.find_match(require))
            if self.__permissive and len(ret_nodes) > 0:
                return ret_nodes
            pass

        # ask the anti-performant section for a match.

        for p, n in self.__rest:
            if p.resolve(require):
                ret_nodes.append(n)
                if self.__permissive and len(ret_nodes) > 0:
                    return ret_nodes
                pass
            pass

        return ret_nodes
        
    def add(self, provide, node):

        # if the provide object is not one which we can index
        # (Provide_String is the only indexable so far), then add it
        # to the anti-performant section.

        if not isinstance(provide, Provide_String):
            raise Error('Indexing of provide objects that are not derived '
                        'from Provide_String is not supported anymore')

        # else, create an index for its type (if not yet available),
        # and add it there.

        for require_type in provide.can_match_classes():
            index = self.__string_indexes.get(require_type)
            if not index:
                index = ProvideMap.Index_Provide_String(type=require_type,
                                                        permissive=self.__permissive)
                self.__string_indexes[require_type] = index
                pass
            index.add(provide, node)
            pass
        pass

    class Index_Provide_String(Unmarshallable):
    
        def __init__(self,
                     type,
                     permissive):
    
            # same meaning as with our checf, the ProvideMap
            self.__permissive = permissive
    
            # map string -> Node
            self.__exact = {}
    
            # list of tuples (prefix-provide, node) 
            self.__prefix = []
    
            # list of tuples (prefix-provide, node)
            self.__glob = []
    
            pass
    
        def n_exact(self): return len(self.__exact)
        def n_prefix(self): return len(self.__prefix)
        def n_glob(self): return len(self.__glob)
    
        def find_match(self, require):
    
            """ Try to match the given require object against what I have.
    
            @return: A Node object if one is found, else None """
    
            ret_nodes = []
    
            node = self.__exact.get(require.string())
            if node:
                ret_nodes.append(node)
                pass
    
            if self.__permissive and len(ret_nodes) > 0:
                return ret_nodes
    
            for p, n in self.__glob:
                if p.resolve(require):
                    ret_nodes.append(n)
                    if self.__permissive:
                        return ret_nodes
                    pass
                pass
    
            for p, n in self.__prefix:
                if p.resolve(require):
                    ret_nodes.append(n)
                    if self.__permissive:
                        return ret_nodes
                    pass
                pass
    
            return ret_nodes
    
        def add(self, provide, node):
            if provide.match() == Provide_String.EXACT_MATCH:
                existing_node = self.__exact.get(provide.string())
                if existing_node:
                    raise Error('Conflict: '+str(provide)+' of node '+str(node)+' already provided by node '+str(existing_node))
                self.__exact[provide.string()] = node
            elif provide.match() == Provide_String.PREFIX_MATCH:
                self.__prefix.append((provide, node))
            elif provide.match() == Provide_String.GLOB_MATCH:
                self.__glob.append((provide, node))
                pass
            pass
    
        pass

    pass
