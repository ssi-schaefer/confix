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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.provide_symbol import Provide_Symbol
from libconfix.core.machinery.require_symbol import Require_Symbol
from libconfix.core.machinery.require import Require
from libconfix.core.machinery.builder import Builder
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.utils import const

import unittest

class UrgencyErrorSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(UrgencyErrorTest('test'))
        pass
    pass

class DeferredProvider(Builder):
    def __init__(self, provide):
        Builder.__init__(self)
        self.__provide = provide
        self.__num_rounds = 0
        pass
    def locally_unique_id(self):
        return self.__class__.__name__+':'+str(self.__provide)
    def enlarge(self):
        self.__num_rounds += 1
        if self.__num_rounds < 5:
            self.force_enlarge()
            pass
        pass
    def relate(self, node, digraph, topolist):
        super(DeferredProvider, self).relate(node, digraph, topolist)
        pass
    def dependency_info(self):
        ret = super(DeferredProvider, self).dependency_info()
        if self.__num_rounds == 5:
            ret.add_provide(self.__provide)
            pass
        return ret
    pass

class UrgencyErrorTest(unittest.TestCase):
    """ Require object with URGENCY_ERROR needs not be resolved immediately.

    Rather, it is sufficient if it has ben resolved at the end of the
    boil cycle."""
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())

        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])

        lodir_builder = DirectoryBuilder(directory=lo)
        lodir_builder.add_builder(DeferredProvider(provide=Provide_Symbol(symbol='the_deferred_provided_symbol')))
        package.rootbuilder().add_builder(lodir_builder)

        hidir_builder = DirectoryBuilder(directory=hi)
        hidir_builder.add_require(Require_Symbol(symbol='the_deferred_provided_symbol',
                                                 found_in=[],
                                                 urgency=Require.URGENCY_ERROR))
        package.rootbuilder().add_builder(hidir_builder)

        package.boil(external_nodes=[])

        self.failUnless(lodir_builder in package.digraph().successors(hidir_builder))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(UrgencyErrorSuite())
    pass

