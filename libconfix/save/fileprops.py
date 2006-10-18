# $Id: fileprops.py,v 1.5 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2003 Salomon Automation

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

import types
import fnmatch

import core.helper
from core.error import Error

class FileProperties:

    """ There is a L{sub-hierarchy<buildable_single.BuildableSingle>}
    in the hierarchy of L{buildables<buildable.Buildable>} which is
    responsible for building a single file. These single-file
    buildables can have certain properties. For example, a C or C++
    source file (usually having the extension .c or .cc) can contain
    the main() function. This property makes it the center of an
    executable (which is built by a L{composite
    buildable<buildable_composite.BuildableComposite>}, namely
    L{buildable_exe.BuildableExecutable} then.

    This class, FileProperties, is a small wrapper around a properties
    dictionary. It implements what is needed, and saves the user from
    inconvenient exceptions that he would have to deal with when we'd
    use a plain dictionary.

    To handle properties you should first see if the property is set
    at all. If it is not set, you reveive a None value from get() (and
    its relatives), then it is up to you how to handle that case. If
    it is set, you interpret the value as you like.

    Take as an example the MAIN property (see
    L{buildable_c_base.BuildableCBase}). If it is not set, the source
    file is scanned for the C{main()} function, and the property is
    set accordingly. If it is set, and if it is true, then the EXENAME
    property is set (if not already). If it is false, and the EXENAME
    is set, an error is flagged. And so on.

    """

    # IF YOU ADD A PROPERTY, BE SURE TO ADD A TEST FOR IT IN
    # tests/fileprops.py

    # C, C++: the source file contains the main() function, and is
    # therefore subject to build as an executable.

    MAIN = 'MAIN'

    # C, C++: the name of the executable that the file will result
    # in. only valid if the file has the MAIN property.

    EXENAME = 'EXENAME'

    # C/C++ header files: should the header be provided package-only,
    # public, or should we make wild guesses.

    PROVIDE_MODE = 'PROVIDE_MODE'

    INSTALL_PATH = 'INSTALL_PATH'

    def __init__(self, properties=None):

        if properties is None:
            self.props_ = {}
        else:
            assert type(properties) is types.DictionaryType
            self.props_ = properties

    def keys(self):
        return self.props_.keys()

    def set(self, name, value):

        assert type(name) is types.StringType

        if value is None:
            raise Error("Value of file property '"+name+"' cannot be None")
            
        self.props_[name] = value

    def get(self, name):

        assert type(name) is types.StringType
        try:
            return self.props_[name]
        except KeyError:
            return None

    def update(self, other):
        
        assert isinstance(other, FileProperties)
        self.props_.update(other.props_)

    def set_main(self, main=1):

        try:
            b = core.helper.read_boolean(main)
        except Error, e:
            raise Error("Cannot convert value of property 'main' "
                        "to a boolean value")

        self.set(FileProperties.MAIN, b)

    def get_main(self):

        return self.get(FileProperties.MAIN)

    def set_exename(self, exename):

        assert type(exename) is types.StringType
        assert len(exename) != 0

        self.set(FileProperties.EXENAME, exename)

    def get_exename(self):

        return self.get(FileProperties.EXENAME)

    def set_install_path(self, p):

        assert type(p) is types.StringType
        self.set(FileProperties.INSTALL_PATH, p)

    def get_install_path(self):

        return self.get(FileProperties.INSTALL_PATH)
            
    def get_provide_mode(self):

        return self.get(FileProperties.PROVIDE_MODE)
            

class FilePropertiesSet:

    def __init__(self):

        self.props_ = []

    def add(self, filename, buildable_type, properties):

        assert filename and len(filename) or buildable_type
        assert properties

        self.props_.append((filename, buildable_type, properties))

    def get_by_filename_or_type(self, filename, buildable_type):

        ret = FileProperties()
        for p in self.props_:

            if filename and p[0] and fnmatch.fnmatchcase(filename, p[0]) or \
                   buildable_type and p[1] and issubclass(buildable_type, p[1]):
                ret.update(p[2])

        return ret
