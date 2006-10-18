# $Id: pseudo_registry.py,v 1.3 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2004 Salomon Automation

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

import os

import core.debug
import helper_pickle
from core.error import Error

class PseudoHandWrittenFileRegistry:

    def __init__(self, dir, filename):

        self.dir_ = dir
        self.filename_ = filename

        # we remember registered files in a dictionary to maintain
        # uniqueness. NOTE that this object is subject to
        # pickling/unpickling, and that we still do not implement
        # versioning. so be careful about changes.
        
        self.registered_files_ = {}

    def dir(self): return self.dir_

    def filename(self): return self.filename_

    def get_registered_files(self): return self.registered_files_.keys()

    def register_file(self, filename):

        if self.registered_files_.has_key(filename):
            raise Error(os.path.join(self.dir_, self.filename_)+
                        'Cannot register pseudo-handwritten file '+filename+' twice')

        self.registered_files_[filename] = 1

    def load(self):

        path = os.path.join(self.dir_, self.filename_)
        if os.path.exists(path):
            try:
                self.registered_files_ = helper_pickle.load_object_from_file(path)
            except Error, e:
                raise Error('Cannot read pseudo-handwritten files '
                            'from file '+path+' though the file exists')

    def dump(self):

        path = os.path.join(self.dir_, self.filename_)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError, e:
                raise Error('Could not remove file '+path, [e])

        if len(self.registered_files_):
            helper_pickle.dump_object_to_file(self.registered_files_, path)
        
    def synchronize_dir_content(self, previous):

        assert self.dir() == previous.dir(), \
               'Cannot synchronize two different directories ('+self.dir()+', '+previous.dir()+')'

        for fn in previous.get_registered_files():

            path = os.path.join(self.dir_, fn)

            if os.path.exists(path):

                # remove any files that won't be written anymore by
                # the current run.

                if not fn in self.get_registered_files():
                    os.remove(path)

            else:

                # the previous run may have registered the files
                # before actually creating them (which is wise anyway
                # because they won't get lost this way). we must not
                # treat the absence of a registered file as an error
                # because the program may have crashed. print out a
                # warning instead.

                core.debug.warn('Pseudo-handwritten file '+path+' has been '
                           'registered in '+
                           os.path.join(previous.dir(), previous.filename())+
                           ' , but does not exist (maybe due to a crash)')
