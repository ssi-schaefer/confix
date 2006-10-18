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
from libconfix.core.utils import helper_pickle

import os

class PackageFile:

    """ A utility class that helps us storing a package into a file,
    and reading it back from it.

    :todo: to functions suffice; shouldn't force the user to create
    and destroy an object for that purpose.

    """
    VERSION = 1

    def __init__(self, file):
        self.file_ = file
        pass

    def load(self):
        try:
            # fixme: File.lines() is currently the only method of
            # reading the content of a file. we read the lines, join
            # them together, and then unpickle the object from the
            # whole buffer. to make this more efficient, we'd need
            # something like File.content().
            obj = helper_pickle.load_object_from_string('\n'.join(self.file_.lines()))
            if obj['version'] != PackageFile.VERSION:
                raise Error('Version mismatch in repository file '+os.sep.join(self.file_.abspath())+''
                            ' (file: '+str(obj['version'])+','
                            ' current: '+str(PackageFile.VERSION)+')')
            return obj['package']
        except Error, e:
            raise Error('Could not read package file '+os.sep.join(self.file_.abspath()), [e])
        pass
    
    def dump(self, package):
        try:
            self.file_.truncate()
            self.file_.add_line(helper_pickle.dump_object_to_string(
                {'version': PackageFile.VERSION,
                 'package': package}))
        except Error, e:
            raise Error('Could not write package file '+os.sep.join(self.file_.abspath()), [e])
        pass
    
    pass
