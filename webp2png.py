from subprocess import Popen
from glob import glob
from sys import argv
from os import remove

def main():
    for entry in argv[1:]:
        for fname in glob(entry):
            p = Popen(["magick.exe", fname, "-quality", "100", fname.replace(".webp", ".png")])
            p.communicate()
            remove(fname)

try:
    main()
except KeyboardInterrupt:
    pass