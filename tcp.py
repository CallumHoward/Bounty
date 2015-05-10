
### TCP Code for Bounty.py

import socket
import sys

try:
    port = int(sys.argv[2])
    port += 1
except:
    print >> sys.stderr, "Usage: Bounty.py -p portnumber"
    sys.exit(1)

if (len(sys.argv) != 3 or sys.argv[1] != "-p"):
    print >> sys.stderr, "Usage: Bounty.py -p portnumber"
    sys.exit(1)
else:
    print "good"

port = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', port)
