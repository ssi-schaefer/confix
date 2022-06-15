#!/usr/bin/env python

import os, sys, types
from stat import *
import re
from optparse import OptionParser

VERBOSE = False

def main():
    parser = OptionParser()
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      default='False',
                      action='store_true',
                      metavar='VERBOSE',
                      help='talk loudly about what\'s being done')

    opts, args = parser.parse_args()

    VERBOSE = opts.verbose

    variables = []
    re_var = re.compile(r'^\s*(\w+)\s*=\s*(\S+)\s*$')

    for nv in args:
        match = re_var.search(nv)
        if not match:
            fatal(nv+" doesn't look like a variable definition")
            pass
        variables.append(Variable(name=match.group(1), value=match.group(2)))
        pass

    re_ignore = re.compile(r'^(\s*#.*|\s*)$')

    directories = set()
    install_instructions = []
    lineno = 0
    for line in sys.stdin:
        lineno += 1
        line = line.rstrip('\n')
        if re_ignore.search(line):
            continue
        for v in variables:
            line = v.subst(line)
            pass

        filenames_str, mode, dir = line.split(':')
        filenames = filenames_str.split(',')
        mode = eval(mode) # interpret octal string, f.e. 0755
        assert type(mode) is int

        directories.add(dir)
        install_instructions.append(InstallationInstruction(
            sourcefiles=filenames, mode=mode, destdir=dir))
        pass

    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)
            pass
        pass

    for i in install_instructions:
        i.execute()
        pass

    pass

def fatal(msg):
    sys.stderr.write(msg+'\n')
    sys.exit(1)
    pass

def verbose(msg):
    if VERBOSE:
        sys.stderr.write(msg+'\n')
        pass
    pass

class Variable:
    def __init__(self, name, value):
        self.name_ = name
        self.value_ = value
        self.rex_ = re.compile(r'\$\('+name+'\)')
        pass
    def subst(self, str):
        return self.rex_.sub(self.value_, str)
    pass

class InstallationInstruction:

    """ From a list of sourcefiles, install the first one that is
    found to destdir, applying mode. """
    
    def __init__(self, sourcefiles, mode, destdir):
        self.sourcefiles_ = sourcefiles
        self.mode_ = mode
        self.destdir_ = destdir
        pass
    def execute(self):
        found_source = False
        for sourcefilename in self.sourcefiles_:
            destfilename = os.path.join(self.destdir_, os.path.basename(sourcefilename))
            deststat = None
            sourcestat = None

            try:
                deststat = os.stat(destfilename)
            except OSError:
                # destination file does not exist
                pass
            try:
                sourcestat = os.stat(sourcefilename)
            except OSError:
                # search for next source file
                continue

            # install only if the destination file does not exist, or
            # if the destination file is older than the source file.
            
            if deststat is None or deststat.st_mtime < sourcestat.st_mtime:
                verbose('copying '+sourcefilename+' to '+destfilename)
                sourcefile = file(sourcefilename, 'r')
                destfile = file(destfilename, 'w')
                for line in sourcefile:
                    destfile.write(line)
                    pass
                sourcefile.close()
                destfile.close()
                os.chmod(destfilename, self.mode_)
                pass

            # in any case, 

            found_source = True
            break
        
        if not found_source:
            fatal('Did not find any of '+str(self.sourcefiles_))
            pass
        pass
    pass

if __name__ == '__main__':
    main()
