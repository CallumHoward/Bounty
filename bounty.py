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
    BUFFER_SIZE = 62
    BOARD_SIZE = 80
    VIEW_SIZE = 5

    FEATURES = {
        '^':    'player',
        'd':    'dynamite',
        'T':    'tree',
        'B':    'boat',
        '~':    'water',
        '*':    'wall',
        'a':    'axe',
        'g':    'gold',
        ' ':    'blank'
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
        self.currentView = []

        # Establishes TCPIP connection on localhost at specified port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('localhost', GameState.PORT)
        self.sock.connect(address)


    ### getters
    def getTurn(self):
        return self.turnNum

    ### setters
    def nextTurn(self):
        self.turnNum += 1

    def storeView(self):
        offset = math.floor(GameState.VIEW_SIZE)  #TODO should this be divided by 2? I can't remember
        for i in range(GameState.VIEW_SIZE):
            assert( len(self.currentView[i]) == GameState.VIEW_SIZE )
            self.state.board[i][self.location - offset : self.location + offset] = self.currentView[i]

    ### other methods
    def printBoard(self):
        self.board.printBoard()

    def sendMove(self, move):
        # Keeps receiving messages from server until connection reset
        # i.e. until game ends and server stops connection
        while True:
            try:
                self.sock.sendall(move)
                self.currentView = self.sock.recv(GameState.BUFFER_SIZE)
            except SocketError:
                self.sock.close()
                print "Connection closed: Game Over"
                break
        #TODO add in Game Lost or Game Won message if needed for Agent file
        return move

class Board(object):
    def __init__(self):
        # board is a list of lists
        self.board = []
        for i in range(0, 160):
            rows = []
            for j in range(0, 160):
                rows.append(u"\u2588")
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
            print "".join(i)



class Agent(object):
    'Agent class for agent of Bounty Game'

    def __init__(self):
        self.location = (GameState.BOARD_SIZE, GameState.BOARD_SIZE)  # start in the middle of the allocated 2D list
        self.rotation = 0  # {0, 1, 2, 3}
        self.turnNum = 0
        self.isInBoat = False
        self.numDynamite = 0
        self.hasAxe = False
        self.hasGold = False
        self.offMap = False
        self.state = GameState()

    ### getters

    def getIsInBoat(self):
        return self.isInBoat

    def getNumDynamite(self):
        return self.numDynamite

    def getHasAxe(self):
        return self.hasAxe

    def getHasGold(self):
        return self.hasGold

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

    def isFacingBlank(self):
        return (self._getFacing() == GameState.FEATURES['blank'])

    def isFacingTree(self):
        return (self._getFacing() == GameState.FEATURES['tree'])

    def isFacingWall(self):
        return (self._getFacing() == GameState.FEATURES['wall'])

    def isFacingSea(self):
        return (self._getFacing() == GameState.FEATURES['sea'])

    def isFacingEdge(self):
        return #TODO


    ### setters
    def moveForward(self):
        # update internal representation of the board
        if self.isFacingBlank() or self.isFacingAxe() or self.isFacingDynamite() or self.isFacingGold():
            self.location = self.state.board.getUp(self.location)
            self.state.sendMove(GameState.MOVES['forward'])


    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.board.getLocation()


    ### other methods

