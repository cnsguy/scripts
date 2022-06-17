from subprocess import Popen
from sys import argv, exit
from os import makedirs

EXPRESSION_SPRITE_SIZE = 256

def main():
    if len(argv) < 4:
        exit("Usage: %s <image file> <start y> <num expressions> <output dir>" % argv[0])

    fname = argv[1]
    start_y = int(argv[2])
    num_expressions = int(argv[3])
    output_dir = ".".join(fname.split(".")[:-1])
    makedirs(output_dir, exist_ok = True)

    for i in range(0, num_expressions):
        x_offset = (i % 4) * EXPRESSION_SPRITE_SIZE
        y_offset = (i // 4) * EXPRESSION_SPRITE_SIZE + start_y
        out_file = "%s/%d.png" % (output_dir, i + 1)
        p = Popen(["magick.exe", fname, "-quality", "100", "-crop", "%dx%d+%d+%d" % (EXPRESSION_SPRITE_SIZE, EXPRESSION_SPRITE_SIZE, x_offset, y_offset), out_file])
        p.communicate()

try:
    main()
except KeyboardInterrupt:
    pass