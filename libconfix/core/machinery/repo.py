# Copyright (C) 2009-2010 Joerg Faschingbauer

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

from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper_pickle
from libconfix.core.utils import debug
from libconfix.core.utils import const

import itertools
import pickle
import os
import re
import types

# use this like debug.trace([marshalling.REPOVERSION_TRACENAME], 'Upgrading class XXX from version 3 to version 100')
REPOVERSION_TRACENAME = 'repoversion'

class Marshallable(object):

    """ Provides support for versioned marshalling and unmarshalling
    of objects. Its functionality is a bit intrusive in that it
    requires every class that want to take part in this game to derive
    from it.

    The functionality is based on `pickle`'s __setstate__ and
    __getstate__ which is provided by `Marshallable`. Derived classes
    must implement two methods, `get_marshalling_data` and
    `set_marshalling_data`, to be able to operate meaningfully."""

    GENERATING_CLASS = 'generating_class'
    VERSIONS = 'versions'
    ATTRIBUTES = 'attributes'

    def get_marshalling_data(self):

        """ Return marshalling data for my attributes.

        To be implemented by derived classes.
        
        The returned marshalling data is a dictionary object that
        contains relatively anonymous data which represents the object
        to be marshalled. The dictionary is composed by derived
        classes and must look as follows:

        ::
        
           {
              'generating_class': <class object of generating object>,
              'versions': <versions of contributions>,
              'attributes': <dictionary with direct attributes key/value pairs>,
           }

        Called indirectly by `__getstate__`.
   
        """

        assert 0, 'abstract'
        pass

    def set_marshalling_data(self, data):

        """ (To be documented) """

        assert 0, 'abstract'
        pass
    
    def __getstate__(self):
        md = self.get_marshalling_data()

        # see if marshalling data are ok.

        assert Marshallable.GENERATING_CLASS in md
        assert Marshallable.VERSIONS in md
        assert Marshallable.ATTRIBUTES in md

        # see if marshalling data have been generated by the concrete
        # class of the object. this can happen if there is some new
        # class derived from an already-marshalled class, and the
        # implementor forgot to overload get_marshalling_data().

        # delete the member since it is only to catch errors during
        # the marshalling phase, and thus need not be marshalled.

        assert md[Marshallable.GENERATING_CLASS] is self.__class__, \
               'Generating class: '+str(md[Marshallable.GENERATING_CLASS])+\
               ', self\'s class: '+str(self.__class__)+\
               ' (maybe the latter forgot to overload get_marshalling_data()?)'
        del md[Marshallable.GENERATING_CLASS]

        return md

    def __setstate__(self, data):
        return self.set_marshalling_data(data)

    pass

class Unmarshallable(Marshallable):
    def get_marshalling_data(self):
        assert 0, self.__class__.__name__+' is not meant to be marshalled'
    def set_marshalling_data(self, data):
        assert 0, self.__class__.__name__+' is not meant to be marshalled'

class MarshalledVersionTooHighError(Error):
    def __init__(self, klass, marshalled_version, highest_version):
        Error.__init__('Unmarshalling error in '+klass.__name__+': '
                       'persistent version (%d) higher than highest version (%d)' \
                       % (marshalled_version, highest_version))
        pass

class MarshalledVersionUnknownError(Error):
    def __init__(self, klass, marshalled_version, current_version):
        Error.__init__('Unmarshalling error in '+klass.__name__+': '
                       'persistent version (%d) unknown; highest version (%d)' \
                       % (marshalled_version, current_version))
        pass
    pass

def update_marshalling_data(marshalling_data,
                            generating_class,
                            attributes,
                            version):
    # don't let attribute conflicts get through
    lhs_attr_keys = set(marshalling_data[Marshallable.ATTRIBUTES].keys())
    rhs_attr_keys = set(attributes.keys())
    assert len(lhs_attr_keys & rhs_attr_keys) == 0

    # same for version conflicts
    lhs_version_keys = set(marshalling_data[Marshallable.VERSIONS].keys())
    rhs_version_keys = set(version.keys())
    assert len(lhs_version_keys & rhs_version_keys) == 0

    marshalling_data[Marshallable.GENERATING_CLASS] = generating_class
    marshalling_data[Marshallable.ATTRIBUTES].update(attributes)
    marshalling_data[Marshallable.VERSIONS].update(version)

    return marshalling_data

class PackageFile:

    """ A utility class that helps us storing a package into a file,
    and reading it back from it.

    :todo: the functions suffice; shouldn't force the user to create
    and destroy an object for that purpose.

    """
    VERSION = 1

    def __init__(self, file):
        self.__file = file
        pass

    def load(self):
        try:
            # fixme: File.lines() is currently the only method of
            # reading the content of a file. we read the lines, join
            # them together, and then unpickle the object from the
            # whole buffer. to make this more efficient, we'd need
            # something like File.content().
            obj = helper_pickle.load_object_from_lines(self.__file.lines())
            if obj['version'] != PackageFile.VERSION:
                raise Error('Version mismatch in repository file '+os.sep.join(self.__file.abspath())+''
                            ' (file: '+str(obj['version'])+','
                            ' current: '+str(PackageFile.VERSION)+')')
            return obj['package']
        except Error as e:
            raise Error('Could not read package file '+os.sep.join(self.__file.abspath()), [e])
        pass
    
    def dump(self, package):
        try:
            self.__file.truncate()
            self.__file.add_lines(
                [helper_pickle.dump_object_to_string({'version': PackageFile.VERSION,
                                                      'package': package})
                 ])
        except Error as e:
            raise Error('Could not write package file '+os.sep.join(self.__file.abspath()), [e])
        pass
    
    pass

class PackageRepository:
    
    def __init__(self): pass

    def iter_packages(self): assert 0 # abstract

    def iter_nodes(self): assert 0 # abstract

    pass

class CompositePackageRepository(PackageRepository):
    def __init__(self, repositories):
        PackageRepository.__init__(self)
        self.__repositories = repositories
        pass

    def add_repo(self, repo):
        self.__repositories.append(repo)
        pass

    def iter_packages(self):
        have_packages = set()

        for r in self.__repositories:
            for p in r.iter_packages():
                if p.name() in have_packages:
                    continue
                have_packages.add(p.name())
                yield p
                pass
            pass
        pass

    def iter_nodes(self):
        for p in self.iter_packages():
            for n in p.nodes():
                yield n
                pass
            pass
        pass
    
    pass

class PackageFileRepository(PackageRepository):
    def __init__(self, file):
        PackageRepository.__init__(self)
        self.__package = PackageFile(file).load()
        pass
    def iter_packages(self):
        yield self.__package
        pass
    def iter_nodes(self):
        return iter(self.__package.nodes())
    pass

_re_repo = re.compile('^.*\\.repo$')

class AutomakePackageRepository(CompositePackageRepository):
    """
    Composite for <prefix>/share/confix-<repo-version>/repo/*.repo style
    repo collection.
    """

    REPO_DATADIR_PATH = ['confix-%s' % const.REPO_VERSION, 'repo']
    REPO_FULL_PATH = ['share'] + REPO_DATADIR_PATH
    
    def __init__(self, prefix):
        assert type(prefix) in [list, tuple], prefix

        CompositePackageRepository.__init__(self, [])

        repodir = prefix+self.REPO_FULL_PATH
        if not os.path.isdir(os.sep.join(repodir)):
            debug.warn('No repository directory '+os.sep.join(repodir))
            return
        
        fs = scan_filesystem(path=repodir)

        errlist = []

        for name, entry in fs.rootdirectory().entries():
            if not isinstance(entry, VFSFile):
                continue
            if _re_repo.match(name):
                try:
                    self.add_repo(PackageFileRepository(file=entry))
                except Error as e:
                    errlist.append(Error('Error reading file "'+os.sep.join(entry.abspath()), [e]))
                except Exception as e:
                    errlist.append(Error('Error reading file "'+os.sep.join(entry.abspath()), [e]))
                    pass
                pass
            pass

        if len(errlist):
            raise Error('Error in repo directory "'+os.sep.join(fs.rootdirectory().abspath())+'"', errlist)

        pass

    pass

class AutomakeCascadedPackageRepository(CompositePackageRepository):
    """
    Composite for AutomakePackageRepository objects.
    """
    def __init__(self, prefix, readonly_prefixes):
        repos = []
        repos.append(AutomakePackageRepository(prefix=prefix))
        for d in readonly_prefixes:
            repos.append(AutomakePackageRepository(prefix=d))
            pass
        CompositePackageRepository.__init__(self, repos)
        pass
    pass

