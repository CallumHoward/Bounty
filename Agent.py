#!/usr/bin/python

import bounty
import sys

def main():
    #TODO support same args as agent.java, but fall back on defaults
    agent = bounty.Agent()
    agent.state.printBoard()

    while agent.state.getTurn() <= GameState.MAX_MOVES:
        agent.makeBestMove()

# call main function only if not imported as a module
if __name__ == '__main__':
    main()
