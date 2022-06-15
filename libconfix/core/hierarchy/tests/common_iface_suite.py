# Copyright (C) 2008-2012 Joerg Faschingbauer

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
from libconfix.core.machinery.buildinfo import BuildInformation
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase
from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.c import C

import unittest

class CURRENT_BUILDER_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "if '"+str(fs.rootdirectory())+"' == str(CURRENT_BUILDER().directory()):",
                              "  CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        pass
    pass
        
class CWD_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['subdir'])",
                              "from libconfix.core.filesys.file import File",
                              "if CWD() == '':",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())"]))
        subdir = fs.rootdirectory().add(
            name='subdir',
            entry=Directory())
        subdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['subdir'])",
                              "from libconfix.core.filesys.file import File",
                              "if CWD() == 'subdir':",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        subsubdir = subdir.add(
            name='subdir',
            entry=Directory())
        subsubdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "if CWD() == 'subdir/subdir':",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        self.assertTrue(package.rootdirectory().find(['subdir']).get('ok'))
        self.assertTrue(package.rootdirectory().find(['subdir', 'subdir']).get('ok'))
        pass
    pass
        
class CURRENT_DIRECTORY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "if '"+str(fs.rootdirectory())+"' == str(CURRENT_DIRECTORY()):",
                              "  CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        pass
    pass
        
class ADD_DIRECTORY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["ADD_DIRECTORY('dir')"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertFalse(package.rootdirectory().get('dir') is None)
        self.assertTrue(type(package.rootdirectory().get('dir')) is Directory)
        pass
    pass
        
class FIND_ENTRY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "entry = FIND_ENTRY('file')",
                              "if entry is not None and type(entry) is File:",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())",
                              ]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        pass
    pass
        
class GET_ENTRIES_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "for e in GET_ENTRIES():",
                              "    if e[0] == 'file' and type(e[1]) is File:",
                              "        CURRENT_DIRECTORY().add(name='ok', entry=File())",
                              "        break",
                              ]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        pass
    pass

class RESCAN_CURRENT_DIRECTORY_Test(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "file('file', 'w')",
                              "RESCAN_CURRENT_DIRECTORY()",
                              "if FIND_ENTRY('file') is not None:",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        fs.sync()

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.assertTrue(package.rootdirectory().get('ok'))
        pass
    pass
        
class ADD_BUILDER_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.machinery.builder import Builder",
                              "class MyBuilder(Builder):",
                              "    def locally_unique_id(self): return 'my_builder_id'",
                              "ADD_BUILDER(builder=MyBuilder())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        for b in package.rootbuilder().iter_builders():
            if b.locally_unique_id() == 'my_builder_id':
                break
            pass
        else:
            self.fail()
            pass
        pass
    pass
        
class SET_FILE_PROPERTIES_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_FILE_PROPERTIES(filename='file', properties={'a': 1, 'b': 2})"]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        f = fs.rootdirectory().get('file')
        self.assertFalse(f is None)
        self.assertTrue(f.get_property('a') == 1)
        self.assertTrue(f.get_property('b') == 2)
        pass
    pass
        
class SET_FILE_PROPERTY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_FILE_PROPERTY(filename='file', name='a', value=1)"]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        f = fs.rootdirectory().get('file')
        self.assertFalse(f is None)
        self.assertTrue(f.get_property('a') == 1)
        pass
    pass

# once I was hunting a bug ...
class BUILDINFORMATION_propagates_Test(PersistentTestCase):
    class TestBuildInformation(BuildInformation):
        def __init__(self):
            BuildInformation.__init__(self)
            self.hello = 1
            pass
        def unique_key(self): return str(self.__class__)
        pass

    class TestBuildInformationReceiver(Builder):
        def __init__(self):
            Builder.__init__(self)
            self.seen_buildinfo = False
            pass
        def locally_unique_id(self): return self.__class__.__name__
        def relate(self, node, digraph, topolist):
            super(BUILDINFORMATION_propagates_Test.TestBuildInformationReceiver, self).relate(node, digraph, topolist)
            for n in topolist:
                for bi in n.iter_buildinfos():
                    try:
                        getattr(bi, 'hello')
                        self.seen_buildinfo = True
                    except: pass
                    pass
                pass
            pass
    
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['lo'])",
                              "DIRECTORY(['hi'])",
                              ]))

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.hierarchy.tests.common_iface_suite import BUILDINFORMATION_propagates_Test",
                              "BUILDINFORMATION(BUILDINFORMATION_propagates_Test.TestBuildInformation())",
                              "PROVIDE_SYMBOL('test')"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.hierarchy.tests.common_iface_suite import BUILDINFORMATION_propagates_Test",
                              "REQUIRE_SYMBOL('test', URGENCY_ERROR)",
                              "ADD_BUILDER(BUILDINFORMATION_propagates_Test.TestBuildInformationReceiver())"
                              ]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(), C()])
        package.boil(external_nodes=[])

        for receiver in package.rootbuilder().find_entry_builder(['hi']).iter_builders():
            try:
                getattr(receiver, 'seen_buildinfo')
                break
            except: pass
            pass
        else:
            self.fail()
            pass

        self.assertTrue(receiver.seen_buildinfo)
        pass
    pass
        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CURRENT_BUILDER_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CWD_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CURRENT_DIRECTORY_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ADD_DIRECTORY_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FIND_ENTRY_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GET_ENTRIES_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(RESCAN_CURRENT_DIRECTORY_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ADD_BUILDER_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SET_FILE_PROPERTIES_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SET_FILE_PROPERTY_Test))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BUILDINFORMATION_propagates_Test))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
