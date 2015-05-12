#!/usr/bin/env python

# bounty.py
# COMP3411 - Assignment 3
# Chris Phibbs and Callum Howard 2015

import math

class GameState:
    'GameState class stores state of Bounty game'

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

    #! should constants go here?
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
        self.location = (GameState.BOARD_SIZE, GameState.BOARD_SIZE)
        self.board = Board()

    ### getters
    def getTurn(self):
        return self.turnNum

    ### setters
    def nextTurn(self):
        self.turnNum += 1

    def storeView(self):
        offset = math.floor(GameState.VIEW_SIZE)
        for i in range(GameState.VIEW_SIZE):
            assert( len(self.currentView[i]) == GameState.VIEW_SIZE )
            self.board.board[i][self.location - offset : self.location + offset] = self.currentView[i]

    ### other methods
    def printBoard(self):
        self.board.printBoard()


class Board:
    def __init__(self):
        # board is a list of lists
        self.board = []
        for i in range(0, 160):
            rows = []
            for j in range(0, 160):
                rows.append(u"\u2588")
            self.board.append(rows)

    def interpretString(self):
        return

    # returns a list of tuples containing coordinates
    def shortestPath(self, (x1, y1), (x2, y2)):
        return

    def printBoard(self):
        for i in self.board:
            print "".join(i)



class Agent:
    'Agent class for agent of Bounty Game'

    def __init__(self):
        self.rotation = 0  # {0, 1, 2, 3}
        self.turnNum = 0
        self.isInBoat = False
        self.numDynamite = 0
        self.hasAxe = False
        self.hasGold = False
        self.offMap = False

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
            target = getUp(self.location)
            facing = self.getBoardLocation(target)
        elif (self.rotation == GameState.CARDINAL['east']):
            target = getRight(self.location)
            facing = self.getBoardLocation(target)
        elif (self.rotation == GameState.CARDINAL['south']):
            target = getDown(self.location)
            facing = self.getBoardLocation(target)
        else: #(self.rotation == GameState.CARDINAL['west'])
            target = getLeft(self.location)
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

    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.board.getLocation()
