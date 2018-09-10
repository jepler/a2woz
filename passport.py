#!/usr/bin/env python3

from passport import eddimage, wozimage, a2rimage
from passport import DefaultLogger, DebugLogger
from passport import Crack, Verify, EDDToWoz
from passport.strings import STRINGS
import os.path
import sys

def usage(error_code):
    exe = sys.argv[0]
    print(STRINGS["header"])
    print("""usage: {exe} crack image.woz
       {exe} verify image.woz
       {exe} convert image.edd""".format(**locals()))
    sys.exit(error_code)

args = len(sys.argv)

if args < 3:
    usage(0)

cmd, inputfile = sys.argv[1:3]
if cmd == "crack":
    processor = Crack
elif cmd == "verify":
    processor = Verify
elif cmd == "convert":
    processor = EDDToWoz
else:
    print("unrecognized command")
    usage(1)

base, ext = os.path.splitext(inputfile)
ext = ext.lower()
if ext == ".woz":
    reader = wozimage.WozReader
elif ext == ".edd":
    reader = eddimage.EDDReader
elif ext == ".a2r":
    reader = a2rimage.A2RImage
else:
   print("unrecognized file type")
   usage(1)

logger = DefaultLogger # TODO add flag to change this

processor(reader(inputfile), logger)
