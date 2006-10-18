# $Id: todo.py,v 1.43 2006/07/18 10:43:16 jfasch Exp $

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
import sys
import pickle

from repo_composite import CompositePackageRepository
from repo_automake import AutomakePackageRepository
from repo_local import LocalPackageRepository
from digraph.digraph import DirectedGraph
from core.edgefinder import EdgeFinder
import repo_automake
from repo import PackageRepository
from digraph.cycle import CycleError
from pkg_buildable import BuildablePackage
from core.error import Error
import core.helper
import configure
import make
import core.debug
import const
import kde_hack

from buildable_mgr import BuildableManager

TODO = []
ARGS = {}

repository = None
package = None

def todo():
    global TODO
    for a in TODO:
        err = a()
        if err: return err

DONE_CHROOT = 0
def CHROOT():
    global DONE_CHROOT
    global ARGS

    if DONE_CHROOT: return 0

    assert ARGS.has_key(const.ARG_PACKAGEROOT)
    os.chdir(ARGS[const.ARG_PACKAGEROOT])

    DONE_CHROOT = 1
    return 0

DONE_BUILDABLEMGR = 0
def BUILDABLEMGR():
    
    global DONE_BUILDABLEMGR

    if DONE_BUILDABLEMGR: return 0
    DONE_BUILDABLEMGR = 1

    if ARGS.has_key(const.ARG_CONFIXPARAMS):
        for (regex, creator) in ARGS[const.ARG_CONFIXPARAMS].buildablecreators():
            BuildableManager.instance.register_creator(regex, creator)

        for clusterer in ARGS[const.ARG_CONFIXPARAMS].buildableclusterers():
            BuildableManager.instance.register_clusterer(clusterer)

DONE_PACKAGE = 0
def PACKAGE():
    global DONE_PACKAGE
    global package
    global ARGS

    if DONE_PACKAGE: return 0

    # ATTENTION: CHDIR TO THE PACKAGE ROOT IS REQUIRED FOR CONFIX TO
    # WORK !!!

    if CHROOT(): return -1

    core.debug.message("scanning package in %s ..." % ARGS[const.ARG_PACKAGEROOT],
                  ARGS[const.ARG_VERBOSITY])

    BUILDABLEMGR()

    # python is neat. build a dictionary containing arguments for the
    # Package class constructor, depending on whether they were
    # specified on the command line. then invoke Package() with the
    # argument dictionary.

    package_args = { 'dir' : os.getcwd(),
                     'use_libtool' : ARGS[const.ARG_USELIBTOOL],
                     'use_bulk_install' : ARGS[const.ARG_USE_BULK_INSTALL],
                     'use_kde_hack' : ARGS[const.ARG_USE_KDE_HACK],
                     'print_timings': ARGS[const.ARG_PRINT_TIMINGS]}
    if ARGS.has_key(const.ARG_PACKAGENAME):
        package_args['name'] = ARGS[const.ARG_PACKAGENAME]
        pass
    if ARGS.has_key(const.ARG_PACKAGEVERSION):
        package_args['version'] = ARGS[const.ARG_PACKAGEVERSION]
        pass
    if ARGS.has_key(const.ARG_CONFIXPARAMS):
        package_args['global_requires'] = ARGS[const.ARG_CONFIXPARAMS].global_requires()
        pass
    package_args['confix_scriptdir'] = os.path.dirname(sys.argv[0])

    package = apply(BuildablePackage, (), package_args)

    DONE_PACKAGE = 1
    return 0

DONE_SCAN = 0
def SCAN():
    global DONE_SCAN
    global package
    if DONE_SCAN: return 0
    PACKAGE()
    debug.message("scanning package in %s ..." % ARGS[const.ARG_PACKAGEROOT],
                  ARGS[const.ARG_VERBOSITY])
    package.scan()
    core.debug.message("done scanning.", ARGS[const.ARG_VERBOSITY])
    DONE_SCAN = 1
    return 0

DONE_READREPO = 0
def READ_REPO():
    global DONE_READREPO
    global repository
    global ARGS

    if DONE_READREPO: return 0

    # collect list of repositories to use

    repodirs = []
    if 1:
        if ARGS.has_key(const.ARG_PREFIX):
            repodirs.append(repo_automake.dir(ARGS[const.ARG_PREFIX]))

        if ARGS.has_key(const.ARG_REPOSITORY) and len(ARGS[const.ARG_REPOSITORY]):
            if ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
                core.debug.warn('both repositories and readonly-prefixes specified; '
                           'taking only repositories ('+','.join(ARGS[const.ARG_REPOSITORY])+')')
            repodirs.extend(ARGS[const.ARG_REPOSITORY][:])
        elif ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
            repodirs.extend([repo_automake.dir(prefix) for prefix in ARGS[const.ARG_READONLY_PREFIXES]])

    # make sure we don't read the same repo twice

    if 1:
        have = {}
        unique_repodirs = []
        for r in repodirs:
            dir = os.path.expanduser(os.path.expandvars(r))
            if not have.has_key(dir):
                have[dir] = 1
                unique_repodirs.append(dir)
        repodirs = unique_repodirs

    repository = CompositePackageRepository()
    for dir in repodirs:
        core.debug.message("reading repository "+dir+" ",
                      ARGS[const.ARG_VERBOSITY])
        repository.add_repo(AutomakePackageRepository(dir=dir))
        core.debug.message("done.", ARGS[const.ARG_VERBOSITY])

    DONE_READREPO = 1
    return 0

DONE_RESOLVE = 0
def RESOLVE():
    global DONE_RESOLVE
    global repository
    global package

    if DONE_RESOLVE: return 0

    if SCAN(): return -1
    if READ_REPO(): return -1

    package.set_repository(repository)

    core.debug.message("resolving dependencies ...", ARGS[const.ARG_VERBOSITY])

    try:
        package.resolve_dependencies()

    except CycleError, e:
        for l in core.helper.format_cycle_error(e):
            sys.stderr.write(l+'\n')
            pass
        return 1

    core.debug.message("done resolving", ARGS[const.ARG_VERBOSITY])

    DONE_RESOLVE = 1
    return 0

DONE_DUMPGRAPH = 0
def DUMPGRAPH():
    global package
    global repository
    if RESOLVE(): return -1
    if READ_REPO(): return -1

    repo = CompositePackageRepository()
    repo.add_repo(LocalPackageRepository(package.install()))
    repo.add_repo(repository)
    modules = []
    for p in repo.packages():
        modules.extend(p.modules())
        pass
    digraph = DirectedGraph(nodes=modules, edgefinder=EdgeFinder(nodes=modules))

    pickle.dump(DirectedGraph(nodes=digraph.nodes(), edges=digraph.edges()), sys.stdout)
    return 0

DONE_BOOTSTRAP = 0
def BOOTSTRAP():
    global DONE_BOOTSTRAP
    global ARGS

    if DONE_BOOTSTRAP: return 0

    if OUTPUT(): return -1

    verbosity = ARGS[const.ARG_VERBOSITY]

    debug.message('+ BOOTSTRAP')
    debug.message('+ Current working directory: '+os.getcwd())
    debug.message('')

    am_prefix = '' # '/usr/local/automake-1.5'
    ac_prefix = '' # '/usr/local/autoconf-2.52'
    lt_prefix = '' # '/usr/local/libtool-1.4.0'

    aclocal = 'aclocal'
    autoheader = 'autoheader'
    autoheader_args = ''
    automake = 'automake'
##     automake_args = ' --foreign --add-missing --copy --verbose'
    automake_args = ' --foreign --add-missing --copy'
    autoconf = 'autoconf'
    autoconf_args = ''
    libtoolize = 'libtoolize'
    libtoolize_args = ' --force --copy'

    assert ARGS.has_key(const.ARG_M4INCDIR)

    aclocal_args = ''
    for d in ARGS[const.ARG_M4INCDIR]:
        aclocal_args = aclocal_args + ' -I ' + d

    if (ARGS[const.ARG_USELIBTOOL]):

        # see where libtool lives, in order to set aclocal's include
        # path to libtool's macros (roughly stolen from apr's
        # buildconf)

        if os.environ.has_key('PATH'): path = os.environ['PATH']
        else: path = ['/usr/bin']

        libtooldir = None

        for dir in path.split(os.pathsep):
            file = os.path.join(dir, libtoolize)
            if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.X_OK):
                libtooldir = dir
                break

        if libtooldir is None:
            raise Error('libtoolize not found along path')

        aclocal_args = aclocal_args + ' -I ' + libtooldir + '/../share/aclocal'

    if len(am_prefix): aclocal = os.path.join(am_prefix, 'bin', aclocal)

    aclocal = aclocal + aclocal_args # in confix2
    debug.message(aclocal + '...') # in confix2
    if os.system(aclocal): # in confix2
        return -1

    if ARGS[const.ARG_USELIBTOOL]:
        if len(lt_prefix):
            libtoolize = os.path.join(lt_prefix, 'bin', libtoolize)
        libtoolize = libtoolize + libtoolize_args
        debug.message(libtoolize + '...')
        if os.system(libtoolize):
            return -1

    if len(ac_prefix): autoheader = os.path.join(ac_prefix, 'bin', autoheader)
    autoheader = autoheader + autoheader_args # in confix2
    debug.message(autoheader + '...') # in confix2
    if os.system(autoheader): # in confix2
        return -1 # in confix2

    if len(am_prefix): automake = os.path.join(am_prefix, 'bin', automake)
    automake = automake + automake_args # in confix2
    debug.message(automake + '...') # in confix2
    if os.system(automake): # in confix2
        return -1 # in confix2

    if ARGS[const.ARG_USE_KDE_HACK]:
        # somehow autoconf will not create a new configure script when
        # it decides that this is not necessary (still don't know how
        # it would decide that). anyway, if it leaves the old script
        # around which we have already patched, then conf.change.pl
        # (the patch is about calling conf.change.pl) will complain
        # about something I don't quite understand. solution: remove
        # configure before re-creating it.
        if os.path.isfile('configure'):
            debug.message('KDE hack: removing existing configure script')
            os.remove('configure')
            pass
        pass

    if len(ac_prefix): autoconf = os.path.join(ac_prefix, 'bin', autoconf)
    autoconf = autoconf + autoconf_args # in confix2
    debug.message(autoconf + '...') # in confix2
    if os.system(autoconf): # in confix2
        return -1 # in confix2

    if ARGS[const.ARG_USE_KDE_HACK]:
        debug.message('KDE hack: patching configure script...')            
        kde_hack.patch_configure_script('configure')
        pass

    DONE_BOOTSTRAP = 1
    return 0

DONE_OUTPUT = 0
def OUTPUT():
    global DONE_OUTPUT
    global package

    if DONE_OUTPUT: return 0

    if RESOLVE(): return -1

    core.debug.message("generating output ...", ARGS[const.ARG_VERBOSITY])
    package.output()
    core.debug.message("done generating output", ARGS[const.ARG_VERBOSITY])

    DONE_OUTPUT = 1
    return 0

DONE_BUILDDIR = 0
def BUILDDIR():
    global DONE_BUILDDIR
    if DONE_BUILDDIR: return 0

    if ARGS.has_key(const.ARG_BUILDDIR): return 0

    if PACKAGE(): return -1

    if not ARGS.has_key(const.ARG_BUILDROOT):
        raise Error("Cannot determine build directory because root of "
                    "package compilation tree (aka BUILDROOT) "
                    "not specified")

    global package

    builddir = os.path.join(ARGS[const.ARG_BUILDROOT], package.name())
    ARGS[const.ARG_BUILDDIR] = builddir

    DONE_BUILDDIR = 1
    return 0

DONE_CONFIGURE = 0
def CONFIGURE():
    global DONE_CONFIGURE
    if DONE_CONFIGURE: return 0

    if CHROOT(): return -1
    if BUILDDIR(): return -1

    # we determine const.ARG_PACKAGEROOT automatically if not specified, so
    # paranoia is right.

    assert ARGS.has_key(const.ARG_PACKAGEROOT)

    cmdline = []
    env = {}
    if ARGS.has_key(const.ARG_CONFIGUREPARAMS):
        cmdline.extend(ARGS[const.ARG_CONFIGUREPARAMS].args())
        env.update(ARGS[const.ARG_CONFIGUREPARAMS].env())

    if ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
        cmdline.append('--with-readonly-prefixes='+','.join(ARGS[const.ARG_READONLY_PREFIXES]))

    try:
        configure.configure(cmdline=cmdline,
                            environment=env,
                            srcdir=os.getcwd(),
                            destdir=ARGS[const.ARG_BUILDDIR],
                            create_dirs = ARGS[const.ARG_ADVANCED],
                            verbosity = ARGS[const.ARG_VERBOSITY])
    except Error, e:
        raise Error("Error calling configure:", [e])

    DONE_CONFIGURE = 1
    return 0

DONE_MAKE = 0
def MAKE():
    global DONE_MAKE
    if DONE_MAKE: return 0

    if BUILDDIR(): return -1

    params = None
    if ARGS.has_key(const.ARG_MAKEPARAMS):
        params = ARGS[const.ARG_MAKEPARAMS]

    targets = []
    if ARGS.has_key(const.ARG_TARGETS):
        targets = ARGS[const.ARG_TARGETS].split()

    try:
        make.make(params, targets, ARGS[const.ARG_BUILDDIR],
                  verbosity = ARGS[const.ARG_VERBOSITY])
    except Error, e:
        raise Error("Error calling make:", [e])

    DONE_MAKE = 1
    return 0

DONE_VERSION = 0
def VERSION():
    global DONE_VERSION
    if DONE_VERSION: return 0

    str = """%s version %s
Confix is Free Software, as defined by the GNU Lesser General Public License
(LGPL). As such Confix comes with ABSOLUTELY NO WARRANTY, and you are free to
modify and redistribute Confix under certain conditions. See the LGPL for more
details about copying conditions and other information.
""" % (os.path.basename(sys.argv[0]), const.CONFIX_VERSION)

    sys.stderr.write(str)

    DONE_VERSION = 1
    return 0

DONE_HELP = 0
def HELP():
    global DONE_HELP
    if DONE_HELP: return 0

    dirname = os.getcwd()

    str = """Usage: %s [SETTING]... [ACTION]...

Settings:

--advanced                    Enable advanced features (see manual).
--builddir=DIR                Set the package build directory to DIR.
                              [default is BUILDROOT/PACKAGENAME]
--buildroot=DIR               Set the package build root to DIR.
--configfile=file1,file2,...  Paths to extra configuration files.
--packagename=NAME            Set the name of the package.
--packageroot=DIR             Top level directory of the package to be scanned.
                              [default is current directory]
--packageversion=VERSION      Set the version of the package. [default is 0.0.0]
--prefix=DIR                  Use DIR for the installation prefix.
--profile=profilename         Name of the configuration profile to be used.
                              [default is 'default']
--quiet                       Print out less Confix information.
--trace=level1,level2,...     Turn on debugging messages. Available levels:
                              provide, require, resolve, check.
--verbose                     Print out more Confix information.

Actions:

--help                        Print this message and quit.
--version                     Print Confix version information and quit.
--resolve                     Scan files for dependencies, and resolve them. Do
                              not output anything.
--output, --bootstrap         Generate the toplevel configure.in and all needed
                              Makefile.am files. Automatically runs --resolve.
--configure                   Call 'configure' in the package's build directory.
--make                        Call 'make' in the package's build directory.
--targets="check clean ..."   Specify one or more make targets

Special dirty performance hacks:

--use-bulk-install            Do not install files one-by-one. Rather,
                              use a dedicated high-preformance
                              install program.
--use-kde-hack                Apply KDE's perl hack which replaces sed
                              in creating configuration files.

""" % sys.argv[0]

    sys.stderr.write(str)

    DONE_HELP = 1
    return 0
