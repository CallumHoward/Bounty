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
# the agent is in a boat. All constants are also stored in this class, as well as a dictionary of
# strings representing elements of the board and different player moves to improve code readability.
# e.g. FEATURES['water'] will print the character for water, and so forth. Socket code is also stored
# in this class, as the current board state is based off the information given by the server.

# Agent Class:
# ------------
# This class aggregates the GameState class and then makes movement decisions based on the
# current game state before sending its move choice to the server. Uses breadth-first search to
# explore the map and get as much information as possible. If it finds the location of the gold
# it devises the shortest path to the gold. Once the agent obtains the gold, it uses a shortest-path
# algorithm to get back to its starting location.
#
# If the agent fails to find a path to the gold or does not know the location of the gold, it finds the
# location of the axe. It then finds the shortest path to the axe, picks it up, then calculates all the
# shortest paths to every known tree and cuts them down. It then explores any unexplored areas if they are
# unobstructed. If a path to the gold still can't be found, it will revert to the "dumbBot" strategy where
# it randomly wanders the map while blowing up random walls when possible. The behavioural methods
# representing these strategies are stored in Agent.py, while all gamestate methods are stored in
# bounty.py.
#
# Our agent also stores a log of all its behaviours in a file called agent.log
#
####



import bounty
import sys
#import time
import random

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
        makeBestMove(agent)
        #userControl()


def makeBestMove(agent):
    smartBot(agent)
    #print 'FACING: |' + agent.state.board.getLocation(agent._getFacing()) + '|', '\t', agent._getFacing()
    #time.sleep(0.05) #TODO remove before submitting
    #print '..'
    #raw_input()


def dumbBot(agent):
    if agent.canRemoveTree():
        agent.removeTree()
    elif agent.canRemoveWall() and not random.randint(-1, 20):
        agent.agentLog('BLASTING WALL')
        raw_input()
        agent.removeWall()
    elif agent.canMoveForward() and random.randint(-1,3):
        agent.moveForward()
    else:
        a = random.randint(-1,1)
        if a == 1:
            agent.turnLeft()
        else:
            agent.turnRight()


def smartBot(agent):
    if agent.getHasGold():
        agent.agentLog('GOT GOLD')
        # follow shortest path back to starting point
        path = agent.state.board.getShortestPath(agent.location, agent.origin, agent.getHasAxe(), agent.getNumDynamite())
        agent.followPath(path)

    # if the location of gold is known
    if agent.state.getGoldLocation():
        agent.agentLog('FOUND GOLD')
        # if path to the location can be found, follow path
        destination = agent.state.getGoldLocation()
        path = agent.state.board.getShortestPath(agent.location, destination, agent.getHasAxe(), agent.getNumDynamite())
        agent.followPath(path)

    # if the location of axe is known
    if agent.state.getAxeLocation():
        agent.agentLog('FOUND AXE')
#        raw_input()
        # if path to the location can be found, follow path
        destination = agent.state.getAxeLocation()
        path = agent.state.board.getShortestPath(agent.location, destination, agent.getHasAxe(), agent.getNumDynamite())
        agent.followPath(path)

    # collect any dynamite that can be seen
    if agent.state.getDynamiteLocations():
        agent.agentLog('COLLECTING EVERY DYNAMITE IN SIGHT')
        for dynamite in agent.state.getDynamiteLocations():
#            raw_input()
            # if path to the location can be found, follow path
            path = agent.state.board.getShortestPath(agent.location, dynamite, agent.getHasAxe(), agent.getNumDynamite())
            agent.followPath(path)

    # chop down all the trees
    if agent.getHasAxe() and agent.state.getTreeLocations():
        agent.agentLog('CHOPPING EVERY TREE IN SIGHT')
        for tree in agent.state.getTreeLocations():
#            raw_input()
            # if path to the location can be found, follow path
            path = agent.state.board.getShortestPath(agent.location, tree, agent.getHasAxe(), agent.getNumDynamite())
            agent.agentLog(path)
            agent.followPath(path)
            agent.removeTree()

    #exploreBot(agent)
    dumbBot(agent)


def exploreBot(agent):
    # bfs to nearest unexplored location
    destination = agent.state.board.getNearestUnexplored()
    if destination:
        agent.agentLog('EXPLORING')
        path = agent.state.board.getShortestPath(agent.location, destination, agent.getHasAxe(), agent.getNumDynamite())
        agent.followPath(path)
    else:
        dumbBot(agent)


def userControl(agent):
    print 'FACING: |' + agent.state.board.getLocation(agent._getFacing()) + '|', '\t', agent._getFacing()
    print 'Move: ',
    input = raw_input()

    if input == 'f' and agent.canMoveForward():
        agent.moveForward()
    elif input == 'l':
        agent.turnLeft()
    elif input == 'r':
        agent.turnRight()
    elif input == 's':  #DEBUG
        destination = agent.state.board.getUp(agent.location)
        destination = agent.state.board.getUp(destination)
        destination = agent.state.board.getLeft(destination)
        agent.state.board.getShortestPath(agent.location, destination, agent.getHasAxe(), agent.getNumDynamite())
    elif input == 'b':
        agent.removeWall()
    elif input == 'c':
        agent.removeTree()
    elif input == 'g':
        agent.moveLeft()
    elif input == 'y':
        agent.moveUp()
    elif input == 'h':
        agent.moveDown()
    elif input == 'j':
        agent.moveRight()
    else:
        print 'can\'t move!'
        exit()

# call main function only if not imported as a module
if __name__ == '__main__':
    main()
