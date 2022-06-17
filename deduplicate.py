from glob import glob
from os import walk, remove
from os.path import join as path_join
from sys import argv, exit, stdout
from hashlib import sha1
from webbrowser import open as webbrowser_open

CHUNK_SIZE = 65536

def hash_file(fname):
    hasher = sha1()

    with open(fname, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)

            if not data:
                break

            hasher.update(data)
    
    return hasher.hexdigest()

def main():
    if len(argv) < 2:
        exit("Usage: %s <directory glob expressions...>" % argv[0])

    hash_map = {}

    for expr in argv[1:]:
        for dir in glob(expr):
            for root, _, files in walk(dir):
                for fname in files:
                    full_path = path_join(root, fname)
                    stdout.write('"%s" = ' % full_path)
                    stdout.flush()
                    shahash = hash_file(full_path)
                    print(shahash)

                    if shahash in hash_map:
                        print('"%s" is a duplicate of "%s" (%s)' % (full_path, hash_map[shahash], shahash))

                        while True:
                            res = input("Delete it? (y/Y/n/o/h) ")

                            if res == "y":
                                remove(full_path)
                                break
                            if res == "Y":
                                remove(hash_map[shahash])
                                break
                            elif res == "n":
                                break
                            elif res == "o":
                                webbrowser_open(full_path)
                                continue
                            elif res == "h":
                                print("y - Delte left file")
                                print("Y - Delete right file")
                                print("n - Skip and continue")
                                print("o - Open in the default handler for the file type")
                                print("h - Show this help message")
                                continue
                            
                            print("Invalid option '%s'" % res)

                    hash_map[shahash] = full_path

try:
    main()
except KeyboardInterrupt:
    pass