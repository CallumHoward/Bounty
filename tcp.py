
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
a = True

while a:
    try:
        received_data = ""
        data_stream = ""
        while len(received_data) != 24:
            data_stream = sock.recv(4092)
            received_data += data_stream
        i = 0
        received_data = received_data[:12]+"^"+received_data[12:]
        agent_view = ""
        while (i < 25):
            if (i % 5 == 0 and i != 0):
                agent_view = agent_view+"\n"+received_data[i]
            else:
                #if i == 12:
                #    print "^",
                agent_view = agent_view+received_data[i]
            i += 1
        print agent_view
        sock.sendall(message)
        a = False
    except SocketError as e:
        sock.close()
        break
    # add in Game Lost or Game Won message if needed for Agent file

