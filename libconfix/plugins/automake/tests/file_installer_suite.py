# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from libconfix.plugins.automake.file_installer import FileInstaller
from libconfix.plugins.automake.makefile_am import Makefile_am
from libconfix.core.utils.error import Error 

import unittest

class FileInstallerTest(unittest.TestCase):

    def test__makefile_am_output_correctness(self):
        file_installer = FileInstaller()

        # public headers
        # --------------

        # public_header_global*.h are installed into $(includedir)
        file_installer.add_public_header(filename='public_header_global_1.h', dir=[])
        file_installer.add_public_header(filename='public_header_global_2.h', dir=[])

        # public_header_x_y.h i installed into $(includedir)/x/y.
        file_installer.add_public_header(filename='public_header_x_y.h', dir=['x', 'y'])

        # public_header_duplicate.h is installed into two distinct
        # directories, one of which is $(includedir)/x/y.
        file_installer.add_public_header(filename='public_header_duplicate.h', dir=[])
        file_installer.add_public_header(filename='public_header_duplicate.h', dir=['x','y'])

        # private headers
        # ---------------
        file_installer.add_private_header(filename='a.h', dir=[])
        file_installer.add_private_header(filename='a.h', dir=['x','y'])
        file_installer.add_private_header(filename='b.h', dir=['x','y'])

        # data files
        # ----------
        file_installer.add_datafile(filename='d', dir=[])
        file_installer.add_datafile(filename='d', dir=['d','D'])
        file_installer.add_datafile(filename='D', dir=['d','D'])

        # prefix files
        # ------------
        file_installer.add_prefixfile(filename='p', dir=[])
        file_installer.add_prefixfile(filename='p', dir=['p','P'])
        file_installer.add_prefixfile(filename='P', dir=['p','P'])

        # tunnel files
        # ------------
        file_installer.add_tunnelfile(filename='t', dir=[])
        file_installer.add_tunnelfile(filename='t', dir=['t','T'])
        file_installer.add_tunnelfile(filename='T', dir=['t','T'])
        
        # the test section
        # ================

        makefile_am = Makefile_am()
        file_installer.output(makefile_am)

        # public headers
        # --------------

        # global directory ($(includedir)) (note that the symbolic
        # name of $(includedir) is hardwired to '').
        dirdefinition_global = makefile_am.install_directories().get('')
        self.failIf(dirdefinition_global is None)
        global_headers = dirdefinition_global.files('HEADERS')
        self.failIf(global_headers is None)

        self.failUnless('public_header_global_1.h' in global_headers)
        self.failUnless('public_header_global_2.h' in global_headers)
        self.failUnless('public_header_duplicate.h' in global_headers)

        # $(includedir)/x/y. its symbolic name is computed by
        # FileInstaller as publicheader_xy.
        
        dirdefinition_x_y = makefile_am.install_directories().get('publicheader_xy')
        self.failIf(dirdefinition_x_y is None)
        x_y_headers = dirdefinition_x_y.files('HEADERS')
        self.failIf(x_y_headers is None)

        self.failUnless('public_header_x_y.h' in x_y_headers)
        self.failUnless('public_header_duplicate.h' in x_y_headers)

        # TODO: rest of the installed types: private headers, data,
        # prefix, tunnel. currently, we only insert them to have the
        # code paths covered. we don't test for correct output.

        pass
    pass

    def test__interface_ok(self):
        file_installer = FileInstaller()

        file_installer.add_public_header(filename='a.h', dir=[])
        file_installer.add_public_header(filename='b.h', dir=[])
        self.failUnless(file_installer.is_public_header_in_dir(filename='a.h', dir=[]))
        self.failUnless(file_installer.is_public_header_in_dir(filename='b.h', dir=[]))

        file_installer.add_public_header(filename='c.h', dir=['x', 'y'])
        file_installer.add_public_header(filename='d.h', dir=['x', 'y'])
        self.failUnless(file_installer.is_public_header_in_dir(filename='c.h', dir=['x', 'y']))
        self.failUnless(file_installer.is_public_header_in_dir(filename='d.h', dir=['x', 'y']))

        file_installer.add_private_header(filename='e.h', dir=[])
        file_installer.add_private_header(filename='f.h', dir=[])
        self.failUnless(file_installer.is_private_header_in_dir(filename='e.h', dir=[]))
        self.failUnless(file_installer.is_private_header_in_dir(filename='f.h', dir=[]))

        file_installer.add_private_header(filename='g.h', dir=['x', 'y'])
        file_installer.add_private_header(filename='h.h', dir=['x', 'y'])
        self.failUnless(file_installer.is_private_header_in_dir(filename='g.h', dir=['x', 'y']))
        self.failUnless(file_installer.is_private_header_in_dir(filename='h.h', dir=['x', 'y']))

        # TODO: rest of the installed types: data, prefix, tunnel
        
        pass

    def test__interface_error(self):
        file_installer = FileInstaller()
        file_installer.add_public_header(filename='a.h', dir=[])
        try:
            file_installer.add_public_header(filename='a.h', dir=[])
            self.fail()
        except Error:
            pass
        except:
            self.fail()
            pass
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(FileInstallerTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

