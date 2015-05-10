#!/usr/bin/env python

# bounty.py
# COMP3411 - Assignment 3
# Chris Phibbs and Callum Howard 2015

class GameState:
    # Constructor method for GameState class
    def __init__(self):
        self.turnNum = 0
        self.isInBoat = False
        self.numDynamite = 0
        self.hasAxe = False
        self.hasGold = False
        self.board = Board()

    ### getters
    def getTurn(self):
        return self.turnNum

    def getIsInBoat(self):
        return self.isInBoat

    def getNumDynamite(self):
        return self.numDynamite

    def getHasAxe(self):
        return self.hasAxe

    def getHasGold(self):
        return self.hasGold

    ### setters
    def nextTurn(self):
        self.turnNum += 1

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

