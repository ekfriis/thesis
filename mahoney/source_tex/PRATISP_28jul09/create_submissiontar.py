#!/usr/bin/env python

import os
import shutil
import tarfile
import subprocess

src = 'pratisp'
dest = 'PRATISP'

try:
    shutil.rmtree(dest)
except OSError:
    pass
shutil.copytree(src, dest)

extensions = ['aux','bib','blg','dvi','end','log','out','ps','tex~']

# remove garbage
for ext in extensions:
    name = 'pratisp.'+ext
    try:
        fn = os.path.join(dest, name)
        os.remove(fn)
    except OSError:
        pass

for name in ['cmechabbrev.tex~', 'IDiagramEM.eps', 'IDiagramEM.pdf']:
    try:
        fn = os.path.join(dest, name)
        os.remove(fn)
    except OSError:
        pass

# tar it up
tar = tarfile.open(dest+'.tar', 'w')
tar.add(dest)
tar.close()
subprocess.call(['gzip', '-f', dest+'.tar'])

shutil.rmtree(dest)

print "Done."
