#!/usr/bin/env python3
# On *nix: could just use tor-resolve w/ -v piped into greps instead to get to largely the same outcome
from sys import argv, exit
from random import shuffle, choice
from threading import Thread
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM, inet_ntoa
from struct import pack, calcsize, unpack
from enum import Enum

class ResolveResponse(Enum):
    OK = 0
    FAIL = 1
    EXCEPTION = 2

proxies = []

for port in range(9051, 9070 + 1):
    proxies.append(("127.0.0.1", port))

def write(output, x):
    with open(output, "a+") as f:
        f.write(x + "\n")

def recv_bin(s, fmt):
    return unpack(fmt, s.recv(calcsize(fmt)))

def resolve(domain):
    global proxies

    try:
        host, port = choice(proxies)

        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))

        s.send(pack("=BBB", 0x05, 1, 0x00))
        recv_bin(s, "=BB")

        pkt = b""
        pkt += pack("=B", 5)                 # version
        pkt += pack("=B", 0xF0)              # command: tor extension: resolve (domain name) command
        pkt += pack("=B", 0x00)              # reserved
        pkt += pack("=B", 0x03)              # atype: SOCKS5_ATYPE_HOSTNAME
        pkt += pack("=B", len(domain))       # domain length
        pkt += domain.encode("u8", "ignore") # domain
        pkt += pack("=H", 0x0)               # port

        s.send(pkt)
        _, rep, _, _ = recv_bin(s, "=BBBB")

        if rep == 4:
            s.close()
            return ResolveResponse.FAIL, "0x%02x" % rep
        else:
            ip, port = recv_bin(s, "=IB")
            ip = inet_ntoa(ip.to_bytes(4, "little"))
            s.close()
            return ResolveResponse.OK, ip
    except Exception as err:
        return ResolveResponse.EXCEPTION, err

def thread_main(output, host_base, queue):
    while len(queue) > 0:
        i = len(queue) - 1
        subdomain = queue.pop()
        final_host = "%s.%s" % (subdomain, host_base)
        result, message = resolve(final_host)

        if result == ResolveResponse.OK:
            print("[%d] %s exists: %s" % (i, final_host, message))
            write(output, "%s exists: %s" % (final_host, message))
        elif result == ResolveResponse.FAIL:
            write(output, "%s does not exist: %s" % (final_host, message))
        elif result == ResolveResponse.EXCEPTION:
            print("[%d] %s exception: %s" % (i, final_host, message))
            write(output, "%s exception: %s" % (final_host, message))
            queue.append(subdomain)

def main():
    if len(argv) < 4:
        exit("Usage: %s <host> <wordlist> <output>" % argv[0])

    host_base = argv[1]
    wordlist = argv[2]
    output = argv[3]
    queue = []

    with open(wordlist, "r") as f:
        queue = [x for x in f.read().split("\n") if len(x) > 0]

    shuffle(queue)

    for _ in range(0, 32):
        thread = Thread(target = thread_main, args = (output, host_base, queue))
        thread.daemon = True
        thread.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass

main()