#!/usr/bin/env python

# bounty.py
# COMP3411 - Assignment 3
# Chris Phibbs and Callum Howard 2015

import math
import socket
from socket import error as SocketError

class GameState(object):
    'GameState class stores state of Bounty game'
    PORT = 31415
    BUFFER_SIZE = 62  #TODO review this
    BOARD_DIM = 80
    BOARD_SIZE = BOARD_DIM * BOARD_DIM
    VIEW_DIM = 5
    VIEW_SIZE = VIEW_DIM * VIEW_DIM

    FEATURES = {
        '^':    'player',
        'd':    'dynamite',
        'T':    'tree',
        'B':    'boat',
        '~':    'water',
        '*':    'wall',
        'a':    'axe',
        'g':    'gold',
        ' ':    'land'
    }

    MOVES = {
        'forward':  'f',
        'left':     'l',
        'right':    'r',
        'chop':     'c',
        'blast':    'b'
    }

    CARDINAL = {
        'north':    0,
        'east':     1,
        'south':    2,
        'west':     3
    }

    DIRECTIONS = {
        'left':     3,  # same as -1 but works with mod
        'right':    1
    }


    # Constructor method for GameState class
    def __init__(self):
        self.board = Board()
        self.current_view = []

        # Establishes TCPIP connection on localhost at specified port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('localhost', GameState.PORT)
        self.sock.connect(address)


    ### getters
    def getTurn(self):
        return self.turnNum

    ### setters
    def _nextTurn(self):
        self.turnNum += 1

    # updates the internal representation of the board with the agent's current view
    def _storeView(self, agent_location):
        # rotate current view to universal orientation
        rotatedView = self._orientate(self.current_view)
        assert(len(rotatedView == GameState.VIEW_SIZE))

        # use agent location to determin which rows and columns of the board to update
        offset = math.floor(GameState.VIEW_SIZE / 2)
        # set board cursor to top left of the view
        row = agent_location[0] - offset
        col = agent_location[1] - offset



#        for i in range(GameState.VIEW_SIZE):
#            assert( len(rotatedView[i]) == GameState.VIEW_SIZE )  #TODO make sure this is ensured by sendMove()
#            self.state.board[i][self.location - offset : self.location + offset] = rotatedView[i]


    ### other methods
    def printBoard(self):
        self.board.printBoard()

    def sendMove(self, move):
        # Keeps receiving messages from server until connection reset
        # i.e. until game ends and server stops connection
        try:
            self.sock.sendall(move)
            self.current_view = self.sock.recv(GameState.BUFFER_SIZE)
            # update internal representation of the board
            self._storeView()
            self._nextTurn()
        except SocketError:
            self.sock.close()
            print 'Connection closed: Game Over'
            #TODO add in Game Lost or Game Won message if needed for Agent file


class Board(object):
    'Board class for internal representation of game board'

    def __init__(self):
        # board is a list of lists
        self.board = []
        # make internal board twice as big to guarantee enough space
        side_length = 2 * GameState.BOARD_SIZE
        for i in range(0, side_length):
            rows = []
            for j in range(0, side_length):
                rows.append(u'\u2588')  # block character
            self.board.append(rows)

    # location is a tuple of form (x, y)
    # returns coordinate above
    def getUp(location):
        return (location[0], location[1] - 1)


    # returns coordinate to right
    def getRight(location):
        return (location[0] + 1, location[1])


    # returns coordinate below
    def getDown(location):
        return (location[0], location[1] + 1)


    # returns coordinate to left
    def getLeft(location):
        return (location[0] - 1, location[1])


    # returns a list of tuples containing coordinates
    def shortestPath(self, (x1, y1), (x2, y2)):
        return


    def printBoard(self):
        for i in self.board:
            print ''.join(i)



class Agent(object):
    'Agent class for agent of Bounty Game'

    def __init__(self):
        self.location = (GameState.BOARD_SIZE, GameState.BOARD_SIZE)  # start in the middle of the allocated 2D list
        self.origin = self.location
        self.rotation = 0  # {0, 1, 2, 3}
        self.turnNum = 0
        self.isInBoat = False
        self.numDynamite = 0
        self.hasAxe = False
        self.hasGold = False
        self.offMap = False
        self.state = GameState()

    ### getters
    def isInBoat(self):
        return self.isInBoat

    def getNumDynamite(self):
        return self.numDynamite

    def getHasAxe(self):
        return self.hasAxe

    def getHasGold(self):
        return self.hasGold

    ### setters
    # Pass in True or False to set the value of isInBoat
    #TODO should it be seperated into two functions?
    def setInBoat(self, change):
        self.isInBoat = change

    def setHasAxe(self):
        self.hasAxe = True

    def setHasGold(self):
        self.hasgold = true

    def gainDynamite(self):
        self.numDynamite += 1

    def expendDynamite(self):
        self.numDynamite -= 1


    # returns space in front of player
    def _getFacing(self):
        if (self.rotation == GameState.CARDINAL['north']):
            target = self.state.board.getUp(self.location)
            facing = self.getBoardLocation(target)
        elif (self.rotation == GameState.CARDINAL['east']):
            target = self.state.board.getRight(self.location)
            facing = self.getBoardLocation(target)
        elif (self.rotation == GameState.CARDINAL['south']):
            target = self.state.board.getDown(self.location)
            facing = self.getBoardLocation(target)
        else: #(self.rotation == GameState.CARDINAL['west'])
            target = self.state.board.getLeft(self.location)
            facing = self.getBoardLocation(target)
        return facing

    def isFacingLand(self):
        return (self._getFacing() == GameState.FEATURES['land'])

    def isFacingTree(self):
        return (self._getFacing() == GameState.FEATURES['tree'])

    def isFacingWall(self):
        return (self._getFacing() == GameState.FEATURES['wall'])

    def isFacingBoat(self):
        return (self._getFacing() == GameState.FEATURES['boat'])

    def isFacingSea(self):
        return (self._getFacing() == GameState.FEATURES['sea'])

    def isFacingEdge(self):
        return #TODO

    def canMoveForward(self):
        if self.isFacingLand():
            return True
        if self.isFacingAxe():
            return True
        if self.isFacingDynamite():
            return True
        if self.isFacingGold():
            return True
        if self.isFacingBoat():
            return True
        if self.isInBoat() and (self.isFacingSea() or self.isFacingLand() or self.isFacingAxe() or self.isFacingGold()):
            return True
            #TODO consider cases when at sea, must record if isInBoat correctly
            #If moving back on land, must reset isInBoat somewhere --Done in moveForward

    def canRemoveTree(self):
        # note: a tree can be chopped from inside boat - tested
        if self.isFacingTree() and self.getHasAxe():
            return True

    def canRemoveWall(self):
        #TODO test if a wall can be blasted from inside boat
        if self.isFacingWall() and self.getNumDynamite():
            return True

    ### setters
    def moveForward(self):
        if self.canMoveForward():
            # update inventory if necessary, if we are facing and have moved forward, then we obtain
            if self.isFacingAxe():
                self.setHaxAxe()
            elif self.isFacingDynamite():
                self.gainDynamite()
            elif self.isFacingGold():
                self.setHasGold()
            elif self.isFacingBoat():
                self.setInBoat(True)
            elif self.isInBoat() and self.isFacingLand():
                self.setInBoat(False)
            #TODO more cases needed here?

            # note: GameState.sendMove() will update internal representation of the board
            # update agent location
            self.location = self.state.board.getUp(self.location)
            self.state.sendMove(GameState.MOVES['forward'])

    def removeTree(self):
        if self.canRemoveTree():
            self.state.sendMove(GameState.MOVES['chop'])

    def removeWall(self):
        if self.canRemoveWall():
            self.state.sendMove(GameState.MOVES['blast'])


    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.board.getLocation()


    ### other methods

