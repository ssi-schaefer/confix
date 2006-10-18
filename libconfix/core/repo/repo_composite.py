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

from repo import PackageRepository

class CompositePackageRepository(PackageRepository):
    def __init__(self):
        PackageRepository.__init__(self)
        self.repositories_ = []
        pass

    def add_repo(self, repo):
        self.repositories_.append(repo)
        pass

    def packages(self):
        ret_packages = []
        have_packages = set()

        for r in self.repositories_:
            for p in r.packages():
                if p.name() in have_packages:
                    continue
                have_packages.add(p.name())
                ret_packages.append(p)
                pass
            pass

        return ret_packages

    def nodes(self):
        ret_nodes = []
        for p in self.packages():
            ret_nodes.extend(p.nodes())
            pass
        return ret_nodes

    pass
