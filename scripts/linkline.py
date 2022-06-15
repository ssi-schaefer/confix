#!/usr/bin/env python

import sys
import os

from libconfix.repo import ModuleRepository
from libconfix.require_h import Require_CInclude
from libconfix.depgraph import DependencyGraph
from libconfix.content_c import ModuleContent_C_NativeInstalled
from libconfix.debug import die

prefix = sys.argv[1]
incfile = sys.argv[2]

repo = ModuleRepository(os.path.join(prefix, 'repo'))

require = Require_CInclude(incfile, 'commandline')
depgraph = DependencyGraph(repo.modules())

resolving_module = None

for n in depgraph.nodes():
    if n.resolves_require(require):
        if resolving_module is not None:
            die("include file '"+incfile+"' is resolved "
                "by at least 2 modules, "+'.'.join(resolving_module.name())+" "
                "and "+'.'.join(n.module().name()))
        else:
            resolving_module = n.module()

if resolving_module is None:
    die("include file '"+incfile+"' is not resolved by any module")

topo_nodes = depgraph.toposort(resolving_module)
topo_nodes.reverse()

linkline = ''

for n in topo_nodes:
    for c in n.module().contents():
        if isinstance(c, ModuleContent_C_NativeInstalled):
            for l in c.libbases():
                linkline += ' -l' + l

if len(linkline) != 0:
    linkline = '-L'+os.path.join(prefix, 'lib') + linkline

print(linkline)
