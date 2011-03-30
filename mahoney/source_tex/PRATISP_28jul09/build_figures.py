#!/usr/bin/env python

"""
    Creates $\epsilon$-machine diagrams and the 
            $\epsilon$-machine information diagram.

    For example, creates Even.pdf from _Even.tex.
"""

import os
import subprocess
import glob
import shutil

os.chdir('image_src')
pratisp_dir = 'pratisp'

sources = glob.glob("_*.tex")
extensions = ['aux','bbl','blg','dvi','log','ps','pdf','tex~']

for source in sources:
    # Create the PDF
    subprocess.call(['latex', source])
    subprocess.call(['dvips', source[:-3]+'dvi'])
    subprocess.call(['ps2pdf', source[:-3]+'ps'])
    subprocess.call(['pdftops', source[:-3]+'pdf'])
    subprocess.call(['ps2eps', '-f', source[:-3]+'ps'])
    subprocess.call(['epstopdf', source[:-3]+'eps'])
    # Copy EPS/PDF over
    ext = 'eps'
    newfn = os.path.join('..', pratisp_dir, source[1:-3]+ext)
    shutil.move(source[:-3]+ext, newfn)
    ext = 'pdf'
    newfn = newfn[:-3] + ext
    shutil.move(source[:-3]+ext, newfn)

    # Cleanup
    for extension in extensions:
        try:
            os.remove("%s%s" % (source[:-3], extension))
        except OSError:
            pass

# Now create the information processing diagrams.
for base in ['even', 'gmp', 'rip']:
    subprocess.call(['python', base+'.py'])
    for ext in ['eps','pdf']:
        fn = base+'ip.'+ext
        target = os.path.join('..', pratisp_dir, fn)
        try:
            os.remove(target)
        except OSError:
            pass
        shutil.move(fn, target)

os.chdir('..')

