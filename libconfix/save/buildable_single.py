# $Id: buildable_single.py,v 1.28 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import types

import core.debug
import core.helper
from buildable import Buildable
from fileprops import FileProperties
from core.error import Error

class BuildableSingle(Buildable):

    """ Base class for every Buildable which is responsible for
    building a single file. In doing so, BuildableSingle is also
    responsible for knowing the file name of the source file, and
    knowing how to open and read it.

    """

    def __init__(self,
                 dir,
                 filename,
                 lines):

        Buildable.__init__(self,
                           name=os.path.join(dir, filename),
                           dir=dir)

        self.filename_ = filename
        self.fileproperties_ = FileProperties()

        # FIXME: from the fact that lines is not null we conclude that
        # we are handling a physical file. this conclusion can be
        # wrong.
        
        if len(lines):
            self.handled_file_ = filename
        else:
            self.handled_file_ = None

    def filename(self):
        return self.filename_

    def fullname(self):
        return os.path.join(self.dir(), self.filename())

    def fileproperties(self):
        return self.fileproperties_

    def gather_handled_files(self):

        ret = Buildable.gather_handled_files(self)[:]
        if self.handled_file_ is not None:
            ret.append(self.handled_file_)
        return ret

    def consume_fileproperties(self, f):

        """ Consuming file properties means calling derived classes to
        consume every member of it. Each then picks the properties it
        understands, and leaves the rest untaken. Derived classes that
        implement consume_fileproperty() should take care to pass that
        call on to their base class.

        Also, we remember all properties that come in for future
        reference. This way we are somewhat dynamic. """

        self.fileproperties_.update(f)

        errors = []

        for k in f.keys():
            if type(k) is not types.StringType:
                errors.append(Error('Object "'+self.name()+'" cannot consume '
                                    'file property: key must be a string'))
                continue
            try:
                self.consume_fileproperty(k, f.get(k))
            except Error, e:
                errors.append(Error('Object "'+self.name()+'" cannot consume '
                                    'file property "'+k+'"', [e]))

        if len(errors):
            raise Error('There were file property errors in object "'+self.name()+'"')

    def consume_fileproperty(self, name, value):

        pass
