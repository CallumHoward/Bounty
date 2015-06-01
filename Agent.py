#!/usr/bin/python

import bounty
import sys
#import time

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-p":
        print "Usage: Agent -p <portnumber>"
        return

    portno = int(sys.argv[2])

    if (portno < 1025 or portno > 65535):
        print "Usage: Agent -p <portnumber>"
        return

    agent = bounty.Agent()
    agent.state.printBoard()

    while agent.state.getTurn() <= bounty.GameState.MAX_MOVES:
        agent.makeBestMove()
        #agent.userControl()

# call main function only if not imported as a module
if __name__ == '__main__':
    main()
