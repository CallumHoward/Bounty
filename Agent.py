#!/usr/bin/python

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
    elif agent.canMoveForward() and random.randint(-1,4):
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
            agent.chopTree()

    dumbBot(agent)

def exploreBot(agent):
    # bfs to nearest unexplored location
    destination = agent.state.board.getNearestUnexplored()
    path = agent.state.board.getShortestPath(agent.location, destination, agent.getHasAxe(), agent.getNumDynamite())
    agent.followPath(path)


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
