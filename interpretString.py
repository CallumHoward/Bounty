#!/usr/bin/env python

# interpretString.py
# converts string to board as stored in board method
# Callum Howard 2015

#from bounty.py import GameState
import re


sampleString = """
+-----+
|     |
|     |
|  ^ d|
|     |
|     |
+-----+
Enter Action(s):
"""

# boardString is what will be recieved over the tcp connection
# according to the spec, the '^' indicator is undefined and must be inferred by the agent
boardString = re.findall('\|(.{5})\|', sampleString)


#TODO move to OO respecting places
location = (81, 81)

rotation = 0;  # {0, 1, 2, 3}

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

### possibly should go in new class that gets inherited

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




def moveForward(self):
    if self.isFacingBlank():
        self.location = getUp(self.location)
    # send move
    sendMove(MOVES['forward'])
    return


def turnLeft(self):
    self.rotation += DIRECTIONS['left']
    self.rotation %= len(CARDINAL)

    # send move
    sendMove(MOVES['left'])


def turnRight(self):
    self.rotation += DIRECTIONS['right']
    self.rotation %= len(CARDINAL)

    # send move
    sendMove(MOVES['right'])


def chopTree(self):
    # send move
    sendMove(MOVES['chop'])
    return


def blastWall(self):
    # send move
    sendMove(MOVES['blast'])
    return


def sendMove(move):
    return


# location is a tuple of form (x, y)
def getBoardLocation(self, location):
    return self.board.getLocation()


# returns space in front of player
def getFacing(self):
    # switch case
    if (rotation == CARDINAL['north']):
        target = getUp(self.location)
        facing = self.getBoardLocation(target)

    elif (rotation == CARDINAL['east']):
        target = getRight(self.location)
        facing = self.getBoardLocation(target)

    elif (rotation == CARDINAL['south']):
        target = getDown(self.location)
        facing = self.getBoardLocation(target)

    else: #(rotation == CARDINAL['west'])
        target = getLeft(self.location)
        facing = self.getBoardLocation(target)

    return facing


def isFacingBlank(self):
    return (self.getFacing() == FEATURES['blank'])


def isFacingTree(self):
    return (self.getFacing() == FEATURES['tree'])


def isFacingWall(self):
    return (self.getFacing() == FEATURES['wall'])


def isFacingSea(self):
    return (self.getFacing() == FEATURES['sea'])


def isFacingEdge(self):
    return #TODO

