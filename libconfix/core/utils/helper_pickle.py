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

from libconfix.core.utils.error import Error, NativeError

import sys

# pickle segfaults on interix. this should be fixed in python 2.5, but
# we leave it in for a while from now.
mypickle = None
if sys.platform.startswith('interix'):
    from libconfix.core.utils import debug
    debug.warn('using pickle instead of cPickle on interix')
    import pickle
    mypickle = pickle
else:
    import pickle
    mypickle = cPickle
    pass

def load_object_from_file(filename):
    try:
        file = open(filename, 'r')
    except IOError as e:
        raise Error('Cannot open file '+filename+' for reading', [e])

    try:
        object = mypickle.load(file)
    except Exception as e:
        raise Error('Cannot read Python object from file '+filename, [NativeError(e, sys.exc_info()[2])])

    return object

def dump_object_to_file(object, filename):
    try:
        file = open(filename, 'w')
    except IOError as e:
        raise Error('Cannot open file '+filename+' for writing', [e])
    try:
        mypickle.dump(object, file)
    except Exception as e:
        raise Error('Cannot dump Python object "'+str(object)+'" to file '+filename, [NativeError(e, sys.exc_info()[2])])
    pass

def load_object_from_string(string):
    try:
        object = mypickle.loads(string)
    except Exception as e:
        raise Error('Cannot read Python object from string', [NativeError(e, sys.exc_info()[2])])

    return object

def dump_object_to_string(object):
    try:
        return mypickle.dumps(object)
    except Exception as e:
        raise Error('Cannot dump Python object to string', [NativeError(e, sys.exc_info()[2])])
    pass

def load_object_from_lines(lines):
    """
    Load a pickled object from a list of lines (as returned by
    File.lines()).
    """
    return load_object_from_string('\n'.join(lines))
