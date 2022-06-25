import os.path
import os
import sys
import subprocess
import threading
import io
import shutil
import pathlib

def die(reason):
    sys.stderr.write(reason + "\n")
    sys.exit(1)

def format_config(port, data_dir):
    return "\n".join([
        "SOCKSPort %d" % port,
        "DataDirectory %s" % data_dir
    ])

def forward(dest, source):
    for line in io.TextIOWrapper(source, "u8", "ignore"):
        line = line.strip()
        dest.write(line + "\n")
        dest.flush()

def launch_tor(binary, config):
    proc = subprocess.Popen([binary, "-f", "-"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    with proc:
        assert proc.stdin is not None and proc.stdout is not None and proc.stderr is not None

        proc.stdin.write(config.encode("u8", "ignore"))
        proc.stdin.flush()
        proc.stdin.close()

        t1 = threading.Thread(target = forward, args = (sys.stdout, proc.stdout), daemon = True)
        t1.start()

        t2 = threading.Thread(target = forward, args = (sys.stderr, proc.stderr), daemon = True)
        t2.start()
        t1.join()
        t2.join()

def main():
    if len(sys.argv) < 2:
        die("Usage: %s <number of instances>" % sys.argv[0])

    binary = shutil.which("tor")

    if binary is None:
        die("Please move the tor binary to your PATH")

    num_launch = int(sys.argv[1])
    threads = []

    for i in range(0, num_launch):
        port = 9050 + i
        ddir = os.path.abspath(os.path.join("tor-dirs", "data-%d" % i))

        if not os.path.exists(ddir):
            pathlib.Path(ddir).mkdir(parents = True, exist_ok = True)
        elif not os.path.isdir(ddir):
            die("Path %s already exists and is not a directory" % dir)

        config = format_config(port, ddir)
        t = threading.Thread(target = launch_tor, args = (binary, config), daemon = True)
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        return

main()