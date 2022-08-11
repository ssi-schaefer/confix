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

import types
import hashlib
import os
from chardet import detect

from libconfix.core.digraph.cycle import CycleError

from .error import Error
from . import external_cmd

def find_confix_root(argv0):
    dir = os.path.dirname(argv0)
    
    # accommodate for relative paths.
    if not os.path.isabs(dir):
        dir = os.path.normpath(os.path.join(os.getcwd(), dir))
        pass

    # first the uninstalled case. (we know programs to be either in
    # the tests subdirectory or in the scripts subdirectory.)
    idx = dir.find(os.path.join('confix', 'tests'))
    if idx == -1:
        idx = dir.find(os.path.join('confix', 'scripts'))
        pass

    if idx >= 0:
        confixroot = os.path.join(dir[0:idx], 'confix')
        installfile = os.path.join(confixroot, 'INSTALL')
        if not os.path.isfile(installfile):
            raise Error('Cannot find (uninstalled) Confix root: file '+installfile+' missing')
        return confixroot

    # ... and then the installed case. this is a pretty big hack, but
    # it ought to work as long as people don't go around messing with
    # the relative locations of installation dirs.
    if dir.endswith('bin'):
        return os.path.dirname(dir)
    
    # we seem to be running completely outside confix's world.
    confix2_py = external_cmd.search_program(program='confix2.py', path=None)
    if confix2_py is None:
        raise Error('Cannot find Confix root: cannot find confix2.py in $PATH at all')

    return find_confix_root(confix2_py)

def format_cycle_error(error):

    assert error.edgelist() is not None

    lines = []
    lines.append('ERROR: cycle detected')
    lines.append(' '*2+'->'.join([n.short_description() for n in error.nodelist()]))
    lines.append('Details follow:')

    for edge in error.edgelist():
        lines.append(' '*2+edge.tail().short_description()+'->'+edge.head().short_description())
        for require in edge.annotations():
            lines.append(' '*4+str(require))
            pass
        pass
    return lines

    for i in range(len(path)-1):

        # from the successors of #i along the circle path, get the one
        # which is the next on the path. print the edge.

        successors = path[i].successors()

        cirlepathnode = None
        cirlepathreasons = []

        for (succnode, succreasons) in successors:
            if succnode is path[i+1]:
                cirlepathnode = succnode
                cirlepathreasons = succreasons
                break
        else:
            assert 0, \
                   'Successor ' + '.'.join(path[i+1].module().name()) + ' of ' + \
                   '.'.join(path[i].module().name()) + ' on circle path is not a successor in the dependency graph'
            pass

        lines.append('  '+'.'.join(path[i].module().name()) + ' depends on ' + '.'.join(path[i+1].module().name()) + ' because of')
        for r in succreasons:
            lines.append('    ' + str(r))
            pass
        pass

    return lines

def normalize_lines(lines):
    """
    When a line contains embedded newlines, it is split into several
    lines.
    """
    ret = None
    for i in range(len(lines)):
        if lines[i].find('\n') >= 0:
            if ret is None: ret = lines[:i]
            ret.extend(lines[i].split('\n'))
        else:
            if ret:
                ret.append(lines[i])
                pass
            pass
        pass
    if ret: return ret
    return lines

def md5_hexdigest_from_lines(lines):
    md5sum = hashlib.md5()
    for l in lines:
        md5sum.update(l.encode())
        pass
    return md5sum.hexdigest()

def write_lines_to_file(filename, lines):

    """ Write lines to filename, appending newlines to each.
        lines may also be bytes, so we have to encode everything
        that is not bytes and write the file as binary
        """

    print('writing '+filename+'...')
    file = open(filename, 'wb')
    for l in lines:
        if type(l) is str: l=l.encode()
        file.write(l+b'\n')
    file.close()

def lines_of_file(filename):

    """ Return a list containing the lines of a file, with newlines
    stripped. """

    with open(filename, 'rb') as file:
        c=file.read()

    enc=detect(c)['encoding']
    if type(enc) is not str:
        enc="ascii"
        print('WARNING: reading '+filename+'[fallback to ' + enc + '] ...')
    else:
        print('reading '+filename+'[' + enc + '] ...')

    file = open(filename, 'r', encoding=enc)

    lines = [l.rstrip() for l in file]

    file.close()
    return lines

def write_lines_to_file_if_changed(filename, lines):

    """ Write lines to filename if the lines are not what the file
    has, or if the file does not exist. (It's not that writing the
    file should be considered expensive; rather, writing the file
    unnecessarily can be expensive if the file is a dependency of
    another file in the build process.) """

    m_file = hashlib.md5()
    m_lines = hashlib.md5()

    if os.path.exists(filename):
        try:
            file = open(filename, 'r')
        except IOError as e:
            raise Error('Could not open file \'' + filename + '\' for reading', [e])
        for l in file:
            m_file.update(l)
            pass
        for l in lines:
            m_lines.update(l+'\n')
            pass

        if m_file.digest() != m_lines.digest():
            write_lines_to_file(filename, lines)
            pass
        pass

    else:
        write_lines_to_file(filename, lines)
        pass
    pass

def copy_file_if_changed(sourcename, targetname, mode):
    sourcedigest = md5_of_file(sourcename)
    if os.path.exists(targetname):
        targetdigest = md5_of_file(targetname)
    else:
        targetdigest = None
        pass
    if targetdigest is None or sourcedigest != targetdigest:
        copy_file(sourcename, targetname, mode)
        pass
    pass

def copy_file(sourcename, targetname, mode):
    try:
        sourcefile = open(sourcename, 'r')
    except IOError as e:
        raise Error('Could not open file \'' + sourcename + '\' for reading', [e])
    try:
        targetfile = open(targetname, 'w')
    except IOError as e:
        raise Error('Could not open file \'' + targetname + '\' for writing', [e])
    for l in sourcefile:
        targetfile.write(l)
        pass
    targetfile.close()
    os.chmod(targetname, mode)
    pass

def md5_of_file(filename):
    finger = hashlib.md5()
    try:
        file = open(filename, 'r')
    except IOError as e:
        raise Error('Could not open file \'' + filename + '\' for reading', [e])
    for l in file:
        finger.update(l)
        pass
    return finger.digest()

def read_boolean(b):

    """ Read a boolean from whatever we offer as boolean value, and
    return real boolean values 0 and 1, or raise an exception. """

    if b is None: return False
    if type(b) in [int, bool]:
        return b
    if type(b) is str:
        b = b.lower()
        if b == 'yes' or b == 'y' or b == 'true' or b == 't' or b == '1':
            return True
        if b == 'no' or b == 'n' or b == 'false' or b == 'f' or b == '0':
            return False
        raise Error("Boolean value must be "
                    "'yes', 'no', 'y', 'n', 'true', 'false', "
                    "'t', 'f', '1', '0', 1, 0")
    raise Error("Bad boolean type")

def intersect_lists(l1, l2):

    dict = {}
    for el in l1:
        dict[el] = 1
    ret = []
    for el in l2:
        if el in dict: ret.append(el)

    return ret

def normalize_filename(fn):
    return fn.replace('\\', '/')

def clone_value(v):

    if type(v) is list or type(v) is tuple:
        ret = []
        for e in v:
            ret.append(clone_value(e))
        return ret

    if type(v) is dict:
        ret = {}
        for k in v.keys():
            ret[k] = clone_value(v[k])
        return ret

    return v

def make_path(str_or_list):
    if isinstance(str_or_list, str):
        if len(str_or_list) == 0:
            return []
        else:
            return str_or_list.split(os.sep)
        pass
    if isinstance(str_or_list, (list, tuple)):
        return str_or_list
    raise Error('Cannot make a path (list of strings) out of a '+str(str_or_list.__class__))
