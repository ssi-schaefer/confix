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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

from libconfix.core.utils.error import Error
from libconfix.core.utils import helper_pickle
from libconfix.core.filesys.file import File

class PseudoHandWrittenFileSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_backend_builder(PseudoHandWrittenFileManager())
        pass
    pass

class PseudoHandWrittenFileManager(Builder):

    # name of the per-directory file which contains the list of
    # automatically generated sources (the pseudo hand-written
    # generated files)
    PSEUDO_HANDWRITTEN_LIST_FILENAME = '.confix-pseudo-handwritten'
    
    def __init__(self):
        Builder.__init__(self)
        
        # we remember registered files in a dictionary to maintain
        # uniqueness. NOTE that this object is subject to
        # pickling/unpickling, and that we still do not implement
        # versioning. so be careful about changes.
        self.__registered_files = set()

        # the set of files that have been registered in a previous
        # instance. None means that nothing has been registered.
        self.__previous_registered_files = None
        
        pass

    def create_file(self, filename):
        if filename in self.__registered_files:
            raise Error('/'.join(self.parentbuilder().directory().relpath(self.package().rootdirectory()))+': '
                        'cannot add pseudo-handwritten file "'+filename+'" twice')
        self.__registered_files.add(filename)
        try:
            existing_file = self.parentbuilder().directory().get(filename)
            if existing_file is None:
                return self.parentbuilder().directory().add(name=filename, entry=File())
            else:
                existing_file.truncate()
                return existing_file
            pass
        except Error as e:
            raise Error('Cannot add pseudo-handwritten file "'+filename+'"')
        pass

    def locally_unique_id(self):
        return self.__class__.__name__

    def initialize(self, package):
        super(PseudoHandWrittenFileManager, self).initialize(package)

        registry_file = self.parentbuilder().directory().get(self.PSEUDO_HANDWRITTEN_LIST_FILENAME)
        if registry_file is None:
            return
        try:
            self.__previous_registered_files = helper_pickle.load_object_from_lines(registry_file.lines())
        except Error as e:
            path = '/'.join(registry_file.relpath(package.rootdirectory()))
            raise Error('Cannot read pseudo-handwritten files '
                        'from file '+path+' though the file exists')
        pass

    def output(self):
        super(PseudoHandWrittenFileManager, self).output()

        if len(self.__registered_files) or self.__previous_registered_files:
            registry_file = self.parentbuilder().directory().get(self.PSEUDO_HANDWRITTEN_LIST_FILENAME)
            if registry_file is not None:
                registry_file.truncate()
            else:
                registry_file = self.parentbuilder().directory().add(
                    name=self.PSEUDO_HANDWRITTEN_LIST_FILENAME,
                    entry=File())
                pass
            registry_file.add_lines([helper_pickle.dump_object_to_string(self.__registered_files)])
            pass

        if self.__previous_registered_files is None:
            return

        # clean up previous. if we have files around that aren't
        # registered anymore in the current instance (but have been
        # registered in the previous instance), remove them.

        # But note: we haven't currently a way to actually remove
        # files (bloody filesys), so we can only truncate them.

        for filename in self.__previous_registered_files:
            if filename in self.__registered_files:
                continue
            file = self.parentbuilder().directory().get(filename)
            if file is None:
                continue
            file.truncate()
            pass
        pass

    pass

def find_pseudo_handwritten_builder(dirbuilder):
    for b in dirbuilder.iter_builders():
        if isinstance(b, PseudoHandWrittenFileManager):
            return b
        pass
    else:
        assert False
        pass
    pass
    
