#!/usr/bin/env python

# bounty.py
# COMP3411 - Assignment 3
# Chris Phibbs and Callum Howard 2015

turnNum = 0
isInBoat = False
numDynamite = 0
hasAxe = False
hasGold = False

class GameState:

    # Constructor method for GameState class
    def __init__(self):
        self.turnNum = 0
        self.isInBoat = False
        self.numDynamite = 0
        self.hasAxe = False
        self.hasGold = False
        self.board = [][]

        for i in range(0, 160):
            for j in range(0, 160):
                self.board.append(-1)


