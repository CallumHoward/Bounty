
### TCP Code for Bounty.py

import socket
import sys
from socket import error as SocketError
import errno

# Dunno if this is good enough for handling required arguments
try:
    port = int(sys.argv[2])
    port += 1
except:
    print >> sys.stderr, "Usage: Bounty.py -p portnumber"
    sys.exit(1)

if (len(sys.argv) != 3 or sys.argv[1] != "-p"):
    print >> sys.stderr, "Usage: Bounty.py -p portnumber"
    sys.exit(1)

# Assigns the port number to the port specified in the command line arguments
port = int(sys.argv[2])

# Establishes TCPIP connection on localhost at specified port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', port)
sock.connect(address)

# Remove this line later, but this is the message sent to the server
message = "F"

# Keeps receiving messages from server until connection reset
# i.e. until game ends and server stops connection
while True:
    try:
        data = sock.recv(62)
        sock.sendall(message)
    # have message = method call to get whatever move we want to send
    except SocketError as e:
        sock.close()
        break
    # add in Game Lost or Game Won message if needed for Agent file
