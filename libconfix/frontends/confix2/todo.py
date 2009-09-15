# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.plugins.automake import bootstrap, configure, make
from libconfix.plugins.automake.kde_hack import KDEHackSetup
from libconfix.plugins.automake.repo_automake import AutomakePackageRepository
from libconfix.core.digraph.cycle import CycleError
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.filesys.overlay_filesys import OverlayFileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.repo import CompositePackageRepository
from libconfix.core.utils import debug
from libconfix.core.utils import helper
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

from libconfix.plugins.c.setups.default_setup import DefaultCSetup

from confix_setup import ConfixSetup
from debug import DebugSetup

import os
import sys
import time
import profile

TODO = []
CONFIG = None

repository = None
filesystem = None
package = None

def todo():
    global TODO
    for a in TODO:
        err = a()
        if err: return err
        pass
    pass

DONE_PACKAGE = 0
def PACKAGE():
    global DONE_PACKAGE
    global package
    global filesystem

    if DONE_PACKAGE: return 0

    SETTINGS()

    debug.message("scanning package in %s ..." % CONFIG.packageroot())
    before = time.time()

    if CONFIG.setups() is None:
        debug.warn('No setup given; using automatic recognition. '
                   'To avoid this warning, use SETUPS() in your '+const.CONFIX2_PKG+' file.')
        setups = [ConfixSetup(use_libtool=CONFIG.use_libtool(),
                              short_libnames=CONFIG.short_libnames())]
    else:
        setups = CONFIG.setups()[:]
        pass

    if CONFIG.debug() is not None:
        setups.append(DebugSetup(CONFIG.debug()))
        pass

    if CONFIG.use_kde_hack():
        setups.append(KDEHackSetup())
        pass

    filesystem = scan_filesystem(path=CONFIG.packageroot().split(os.sep))

    if CONFIG.overlayroot() is not None:
        overlayed_filesystem = scan_filesystem(path=CONFIG.overlayroot().split(os.sep))
        filesystem = OverlayFileSystem(original=filesystem, overlay=overlayed_filesystem)
        pass

    package = LocalPackage(rootdirectory=filesystem.rootdirectory(),
                           setups=setups)
    DONE_PACKAGE = 1

    debug.message('done scanning ('+str(time.time()-before)+' seconds)')
    
    return 0

DONE_READREPO = 0
def READ_REPO():
    global DONE_READREPO
    global repository
    global ARGS

    if DONE_READREPO: return 0

    SETTINGS()

    # collect list of repositories to use

    prefixes = []

    if CONFIG.prefix() is not None:
        prefixes.append(CONFIG.prefix())
        pass

    # make sure we don't read the same repo twice
    have = {}
    unique_prefixes = []
    for prefix in prefixes:
        dir = os.path.expanduser(os.path.expandvars(prefix))
        if not have.has_key(dir):
            have[dir] = 1
            unique_prefixes.append(dir)
            pass
        pass
    prefixes = unique_prefixes

    # finally, do our job
    repository = CompositePackageRepository()
    num_repos = len(prefixes) + len(CONFIG.readonly_prefixes())

    debug.message('reading '+str(num_repos)+' repositories...')
    before = time.time()

    for prefix in prefixes + CONFIG.readonly_prefixes():
        debug.message('reading repository '+prefix+' ...')
        repository.add_repo(AutomakePackageRepository(prefix=prefix.split(os.sep)))
        pass

    debug.message('done reading respositories ('+str(time.time()-before)+' seconds)')
    
    DONE_READREPO = 1
    return 0

DONE_BOIL = 0
def BOIL():
    global DONE_BOIL
    global repository
    global package

    if DONE_BOIL: return 0

    if PACKAGE(): return -1
    if READ_REPO(): return -1
    SETTINGS()

    # as input for the dependency graph calculation, extract all nodes
    # from our package repository.
    external_nodes = []
    for p in repository.packages():
        if p.name() != package.name():
            external_nodes.extend(p.nodes())
            pass
        pass

    debug.message('boiling package ...')
    before = time.time()
    try:
        #profile.runctx('package.boil(external_nodes=external_nodes)', {'package':package, 'external_nodes':external_nodes} ,{})
        package.boil(external_nodes=external_nodes)
    except CycleError, e:
        for l in helper.format_cycle_error(e):
            sys.stderr.write(l+'\n')
            pass
        return 1

    debug.message('done boiling ('+str(time.time()-before)+' seconds)')

    DONE_RESOLVE = 1
    return 0

DONE_DUMPGRAPH = 0
def DUMPGRAPH():
    global package
    global repository
    if BOIL(): return -1
    if READ_REPO(): return -1
    SETTINGS()

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

    SETTINGS()
    if OUTPUT(): return -1

    bootstrap.bootstrap(packageroot=CONFIG.packageroot().split(os.sep),
                        use_kde_hack=CONFIG.use_kde_hack(),
                        path=None,
                        argv0=sys.argv[0])

    DONE_BOOTSTRAP = 1
    return 0

DONE_OUTPUT = 0
def OUTPUT():
    global DONE_OUTPUT
    global package
    global filesystem

    if DONE_OUTPUT: return 0

    if BOIL(): return -1
    SETTINGS()

    debug.message('generating ...')
    before = time.time()
    package.output()
    filesystem.sync()
    debug.message('done generating ('+str(time.time()-before)+' seconds)')

    DONE_OUTPUT = 1
    return 0

DONE_BUILDDIR = 0
def BUILDDIR():
    global DONE_BUILDDIR
    if DONE_BUILDDIR: return 0

    if ARGS.has_key(const.ARG_BUILDDIR): return 0

    if PACKAGE(): return -1
    SETTINGS()

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

    SETTINGS()

    configure_env = {}
    configure_env.update(os.environ)
    if CONFIG.configure_env() is not None:
        configure_env.update(CONFIG.configure_env())
        pass

    try:
        builddir = deduce_builddir()
    except Error, e:
        raise Error('Cannot call configure: build directory unknown', [e])
    
    if CONFIG.advanced() and not os.path.exists(builddir):
        os.makedirs(builddir)
        pass

    debug.message('configure ...')
    before = time.time()
    
    try:
        ro_pfxs = []
        for p in CONFIG.readonly_prefixes():
            ro_pfxs.append(p.split(os.sep))
            pass
        prefix = None
        if CONFIG.prefix() is not None:
            prefix = CONFIG.prefix().split(os.sep)
            pass
        configure.configure(packageroot=CONFIG.packageroot().split(os.sep),
                            builddir=builddir.split(os.sep),
                            prefix=prefix,
                            readonly_prefixes=ro_pfxs,
                            args=CONFIG.configure_args(),
                            env=configure_env)
        pass
    except Error, e:
        raise Error("Error calling configure:", [e])

    debug.message('done configure ('+str(time.time()-before)+' seconds)')

    DONE_CONFIGURE = 1
    return 0

DONE_MAKE = 0
def MAKE():
    global DONE_MAKE
    if DONE_MAKE: return 0

    SETTINGS()

    make_env = {}
    make_env.update(os.environ)
    if CONFIG.make_env() is not None:
        make_env.update(CONFIG.make_env())
        pass

    try:
        builddir = deduce_builddir()
    except Error, e:
        raise Error('Cannot call make: build directory unknown', [e])

    debug.message('make ...')
    before = time.time()
    
    try:
        make.make(builddir=builddir.split(os.sep),
                  args=CONFIG.make_args(),
                  env=make_env)
    except Error, e:
        raise Error("Error calling make:", [e])

    debug.message('done make ('+str(time.time()-before)+' seconds)')

    DONE_MAKE = 1
    return 0

DONE_SETTINGS = 0
def SETTINGS():
    global DONE_SETTINGS
    if DONE_SETTINGS: return 0

    trace = CONFIG.trace()
    if trace is not None:
        debug.set_trace(trace)
        pass

    message_prefix = CONFIG.message_prefix()
    if message_prefix is not None:
        debug.set_message_prefix(message_prefix)
        pass

    pass

def deduce_builddir():
    builddir = CONFIG.builddir()
    if builddir is not None:
        return builddir
    buildroot = CONFIG.buildroot()
    if buildroot is None:
        raise Error('Cannot determine build directory: neither builddir nor buildroot are set')
    packageroot = CONFIG.packageroot()
    if packageroot is None:
        raise Error('Cannot determine build directory: need packageroot')

    PACKAGE()

    return os.path.join(buildroot, package.name()+'-'+package.version())
