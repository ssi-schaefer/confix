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
from libconfix.core.filesys.file import File

class PseudoHandWrittenFileManager(object):
    def __init__(self, directory):
        self.directory_ = directory
        # we remember registered files in a dictionary to maintain
        # uniqueness. NOTE that this object is subject to
        # pickling/unpickling, and that we still do not implement
        # versioning. so be careful about changes.
        self.registered_files_ = set()
        pass

    def create_file(self, filename):
        if filename in self.registered_files_:
            raise Error(self.directory_.relpath(self.directory_.filesystem().rootdirectory())+': '
                        'cannot add pseudo-handwritten file "'+filename+'" twice')
        self.registered_files_.add(filename)
        try:
            existing_file = self.directory_.get(filename)
            if existing_file is None:
                return self.directory_.add(name=filename, entry=File())
            else:
                existing_file.truncate()
                return existing_file
            pass
        except Error, e:
            raise Error('Cannot add pseudo-handwritten file "'+filename+'"')
        return ret

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

                debug.warn('Pseudo-handwritten file '+path+' has been '
                           'registered in '+
                           os.path.join(previous.dir(), previous.filename())+
                           ' , but does not exist (maybe due to a crash)')
