import socket
import sys
import select

s = socket.socket()
if len(sys.argv) != 2:
    print "Print in the following order : script, port number"
    exit()


s.connect(('127.0.0.1', int(sys.argv[1])))
inputlist = [s, sys.stdin]
outputlist = []
errorlist = []

while True:
    readable, writable, exceptional = select.select(inputlist, outputlist, errorlist)
    for inp in readable:
        if inp == s:
            msg = inp.recv(1024)
            if msg == "----":
                break
            print msg
        else:
            msg = inp.readline()
            s.send(msg)
            sys.stdout.flush()

s.close()
sys.exit()
    
