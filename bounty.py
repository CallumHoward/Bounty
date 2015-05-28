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
    MAX_MOVES = 10000
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
        ' ':    'land',
        '.':    'edge'
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
        self.current_view = self.sock.recv(GameState.VIEW_SIZE)

        print 'VIEW_SIZE = {}'.format(GameState.VIEW_SIZE)
        print 'current_view:'
        print '|',
        print self.current_view,
        print '|'
        print

        self._storeView(self.board.START_LOCATION, Agent.INIT_ROTATION)


    ### getters
    def getTurn(self):
        return self.turn_num

    ### setters
    def _nextTurn(self):
        if self.turn_num <= GameState.MAX_MOVES:
            self.turn_num += 1
        else:
            print 'Max number of turns reached'
            #TODO handle exiting of game

    def _orientate(self, rotation):
        rotated_view = self.current_view
        for num in range(rotation):
            # rotate view clockwise
            rotated_view = zip(*rotated_view[::-1])

        return rotated_view


    # updates the internal representation of the board with the agent's current view
    def _storeView(self, agent_location, agent_rotation):
        # rotate current view to universal orientation
        rotated_view = self._orientate(agent_rotation)

        print 'length of current_view'
        print len(self.current_view)

        print 'length of rotated_view'
        print len(rotated_view)

        assert(len(rotated_view) == GameState.VIEW_SIZE)  #TODO remove before submitting

        # use agent location to determin which rows and columns of the board to update
        offset = math.floor(GameState.VIEW_DIM / 2)  # floor because of zero indexing
        # set board cursor to top left of the view
        row_start = agent_location[0] - offset
        row_end = row_start + GameState.VIEW_DIM
        col_start = agent_location[1] - offset
        col_end = col_start + GameState.VIEW_DIM

        # store current view into board row by row
        for row in range(row_start, row_end):
            self.state.board[row][col_start:col_end] = rotated_view[row * GameState.VIEW_DIM]


    ### other methods
    def printBoard(self):
        self.board.printBoard()

    def sendMove(self, move, agent_location, agent_rotation):
        # Keeps receiving messages from server until connection reset
        # i.e. until game ends and server stops connection
        try:
            self.sock.sendall(move)
            self.current_view = self.sock.recv(GameState.VIEW_SIZE)
            # update internal representation of the board
            self._storeView(agent_location, agent_rotation)
            self._nextTurn()
            self.board.printBoard()
        except SocketError:
            self.sock.close()
            print 'Connection closed: Game Over'
            #TODO add in Game Lost or Game Won message if needed for Agent file


class Board(object):
    'Board class for internal representation of game board'

    START_LOCATION = (GameState.BOARD_DIM, GameState.BOARD_DIM)

    def __init__(self):
        # board is a list of lists
        self.board = []
        # make internal board twice as big to guarantee enough space
        side_length = 2 * GameState.BOARD_DIM
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

    INIT_ROTATION = 0

    def __init__(self):
        self.state = GameState()
        self.location = self.state.board.START_LOCATION  # start in the middle of the allocated 2D list
        self.origin = self.location
        self.rotation = Agent.INIT_ROTATION  # {0, 1, 2, 3}
        self.turn_num = 0
        self.is_in_boat = False
        self.num_dynamite = 0
        self.has_axe = False
        self.has_gold = False

    ### getters
    def isInBoat(self):
        return self.isInBoat

    def getNumDynamite(self):
        return self.num_dynamite

    def getHasAxe(self):
        return self.has_axe

    def getHasGold(self):
        return self.has_gold

    ### setters
    # Pass in True or False to set the value of isInBoat
    def setInBoat(self, value):
        self.is_in_boat = value

    def setHasAxe(self):
        self.has_axe = True

    def setHasGold(self):
        self.has_gold = True

    def gainDynamite(self):
        self.num_dynamite += 1

    def expendDynamite(self):
        self.num_dynamite -= 1


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
        return (self._getFacing() == GameState.FEATURES['edge'])

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

    def canRemoveTree(self):
        # note: a tree can be chopped from inside boat - tested
        if self.isFacingTree() and self.getHasAxe():
            return True

    def canRemoveWall(self):
        # note: a wall can be blasted from inside boat - tested
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
            self.state.sendMove(GameState.MOVES['forward'], self.location, self.rotation)

    def removeTree(self):
        if self.canRemoveTree():
            self.state.sendMove(GameState.MOVES['chop'], self.location, self.rotation)

    def removeWall(self):
        if self.canRemoveWall():
            self.state.sendMove(GameState.MOVES['blast'], self.location, self.rotation)

    def turnLeft(self):
        self.state.sendMove(GameState.MOVES['left'], self.location, self.rotation)
        self.rotation += GameState.DIRECTIONS['left']

    def turnRight(self):
        self.state.sendMove(GameState.MOVES['right'], self.location, self.rotation)
        self.rotation += GameState.DIRECTIONS['right']

    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.board.getLocation()


    ### other methods
    def makeBestMove(self):
        if self.canMoveForward():
            best_move = GameState.MOVES['forward']

        return best_move


def main():
    #TODO support same args as agent.java
    agent = Agent()
    agent.state.printBoard()

    while agent.state.getTurn() <= GameState.MAX_MOVES:
        agent.makeBestMove()


# call main function only if not imported as a module
if __name__ == '__main__':
   main()
