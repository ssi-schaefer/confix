# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

import os, shutil, unittest

class PersistentTestCase(unittest.TestCase):

    sequential_number = 0
    
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        pass

    def rootpath(self):
        return self.__my_rootpath

    def setUp(self):
        self.__my_rootpath = ['', 'tmp',
                              'confix.'+str(os.getpid())+'.'+ \
                              str(PersistentTestCase.sequential_number)+'.'+ \
                              self.__class__.__name__]
        PersistentTestCase.sequential_number += 1
        pass
    
    def tearDown(self):
        dir = os.sep.join(self.__my_rootpath)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            pass
        pass

    pass
