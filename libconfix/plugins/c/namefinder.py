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

from libconfix.core.utils.error import Error

class NameFinder:
    def __init__(self):
        pass
    def find_exename(self, packagename, path, centername):
        assert 0, 'abstract'
        return 'some_string'
    def find_libname(self, packagename, path):
        assert 0, 'abstract'
        return 'some_string'
    pass

class LongNameFinder(NameFinder):
    def __init__(self):
        NameFinder.__init__(self)
        pass

    def find_exename(self, packagename, path, centername):
        return '_'.join([packagename] + path + [centername])
    def find_libname(self, packagename, path):
        return '_'.join([packagename] + path)
    pass

class ShortNameFinder(NameFinder):
    def __init__(self):
        NameFinder.__init__(self)
        self.assigned_libnames_ = set()
        pass

    def find_exename(self, packagename, path, centername):
        return '_'.join([packagename] + path + [centername])

    def find_libname(self, packagename, path):
        if len(path) == 0:
            if packagename in self.assigned_libnames_:
                raise Error('Name '+packagename+' has already been assigned')
            return packagename
        
        candidate = []
        iter = range(len(path))
        iter.reverse()
        
        for i in iter:
            candidate.insert(0, path[i])
            name = '_'.join([packagename]+candidate)
            if name not in self.assigned_libnames_:
                self.assigned_libnames_.add(name)
                return name
            pass

        raise Error('Could not find unique name for '+'.'.join([packagename]+path))
