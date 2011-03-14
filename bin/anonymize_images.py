#!/usr/bin/env python

import os
import sys
import logging
import glob
import hashlib
import shutil


log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)



target = sys.argv[1]
out_dir = sys.argv[2]

log.debug("anonymizing files in %s. writing to %s" % (target, out_dir))


for infile in glob.glob( os.path.join(target, '*') ):
    outdir = os.path.dirname(infile)
    (root, ext) = os.path.splitext(os.path.basename(infile))
    newfile = os.path.join(outdir,
                           "%s%s" % (hashlib.md5(root).hexdigest(), ext))
                           
    log.debug("renaming %s to %s" % (infile, newfile))
    shutil.move(infile, newfile)
