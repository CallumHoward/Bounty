#!/usr/bin/python

# Documentation for COMP3411
# Chris Phibbs (z3460482) and Callum Howard (z3419451)

# We decided to use Python for this assignment due to our familiarity
# with the language and due to its easy readability and power

# The main design
# idea from the start was to have our agent create inside of itself its
# own representation of the board displaying all the areas it had seen, so
# that it could make an informed decision based off this information and then
# create paths to wherever it needed to go.

# To achieve this, we split the program into 3 classes: GameState, Agent and Board.

# Board Class:
# ------------
# The board class stores the internal representation of the board that our agent
# would keep track of as he explores the board itself. To represent this we used
# a two-dimensional list, which allowed us to use a coordinate system to keep
# track of objects on the map easily. This was much better than our earlier ideas of
# a string, 1-dimensional list and a hash, as each of these options in our opinion
# made it harder to keep track of positions/objects on the map. This allowed us to
# keep track of board positions with tuples.
#
# Storing the board this way made it easy to find adjacent objects to particular
# board coordinates and such, as well as pathfinding. We therefore included all methods
# related to object finding and path finding in this class.
#
# We initialise the board to be 160x160 squares. By starting our mapping in the middle of this
# 160x160 board, we ensure that regardless of our orientation/starting position on the real map,
# we will be able to accurately represent it in our own agent's version - since the real board
# can be no bigger than 80x80 squares.

# GameState Class:
# ----------------
# This class stores all information on the current game state. It aggregates the board
# class to keep track of the game board, as well as storing boolean variables denoting
# whether objects such as the axe, dynamite, gold etc. had been picked up, as well as whether
# the agent is in a boat. Constants are stored in their respective classes, and are used to improve code readability.
# e.g. FEATURES['water'] will print the character for water, and so forth. Socket code is also stored
# in this class, as the current board state is based off the information given by the server.

# Agent Class:
# ------------
# This class aggregates the GameState class and then makes movement decisions based on the
# current game state before sending its move choice to the server. Uses breadth-first search to
# explore the map and get as much information as possible, before devising a path to the gold. Once
# the agent obtains the gold, it uses Breadth First Search algorithm to get back to its starting location.
#
# If the agent fails to find a path to the gold, it will randomly wander the map while chopping
# trees at random until it can make a more informed decision.

####

import bounty
import sys

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
