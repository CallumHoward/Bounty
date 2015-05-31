#!/usr/bin/env python

# bounty.py
# COMP3411 - Assignment 3
# Chris Phibbs and Callum Howard 2015

import math
import socket
import sys
from socket import error as SocketError
from Queue import Queue
import time
import random

class GameState(object):
    'GameState class stores state of Bounty game'

    PORT = 31415
    MAX_MOVES = 10000
    BOARD_DIM = 10#80
    BOARD_SIZE = BOARD_DIM * BOARD_DIM
    VIEW_DIM = 5
    VIEW_SIZE = VIEW_DIM * VIEW_DIM
    FOG_CHAR = '+'#u'\u2588'

    FEATURES = {
        'player':   '^',
        'dynamite': 'd',
        'tree':     'T',
        'boat':     'B',
        'water':    '~',
        'wall':     '*',
        'axe':      'a',
        'gold':     'g',
        'land':     ' ',
        'edge':     '.',
        'fog':      FOG_CHAR
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
        self.turn_num = 0
        self.board = Board()
        self.current_view = []  #TODO make sure string is converted to list of lists for rotation
        # Establishes TCPIP connection on localhost at specified port
        portNumber = int(sys.argv[2])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('localhost', portNumber)
        self.sock.connect(address)

        try:
            received_data = ""
            data_stream = ""
            while len(received_data) != 24:
                data_stream = self.sock.recv(4092)
                if len(data_stream) == 0:
                   # receiving = False
                    break
                received_data += data_stream
              #  print "len of received is ", len(received_data)
            i = 0
            received_data = received_data[:12]+"^"+received_data[12:]
            agent_view = ""
            while (i < 25):
             #   print "for i=", i, " object is |", received_data[i], "|"
             #   if (i % 5 == 0 and i != 0):
            #        print "executed mod condition"
                agent_view = agent_view+received_data[i]
                #else:
                #    agent_view = agent_view+received_data[i]
                i += 1
                #print "stuck in i loop"
        except SocketError:
            self.sock.close()
            #break
            #print "stuck in outer loop"
        #print agent_view
        #print "size of thing is", len(agent_view)
        self._convertString2List(agent_view)

        #print 'VIEW_SIZE = {}'.format(GameState.VIEW_SIZE)
        #print 'current_view:'
        #print '|',
        #print self.current_view,
        #print '|'
        #print

        self._storeView(self.board.START_LOCATION, Agent.INIT_ROTATION)


    ### getters
    def getTurn(self):
        return self.turn_num


    ### setters
    def _nextTurn(self):
        if self.turn_num <= GameState.MAX_MOVES:
            self.turn_num += 1
        else:
            print 'Game Lost.'
            exit()

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

        #assert(len(rotated_view) == GameState.VIEW_SIZE)  #TODO remove before submitting

        # use agent location to determin which rows and columns of the board to update
        offset = int(math.floor(GameState.VIEW_DIM / 2))  # floor because of zero indexing
        # set board cursor to top left of the view
        row_start = agent_location[1] - offset
        row_end = row_start + GameState.VIEW_DIM
        col_start = agent_location[0] - offset
        col_end = col_start + GameState.VIEW_DIM

        # store current view into board row by row, col by col
        for i, row in enumerate(range(row_start, row_end)):
            for j, col in enumerate(range(col_start, col_end)):
                self.board.board[row][col] = rotated_view[i][j]


    ### other methods
    def printBoard(self):
        self.board.printBoard()


    def sendMove(self, move, agent_location, agent_rotation):
        # Keeps receiving messages from server until connection reset
        # i.e. until game ends and server stops connection
        self.sock.sendall(move)


        try:
            received_data = ""
            data_stream = ""
            while len(received_data) != 24:
                data_stream = self.sock.recv(4092)
                if len(data_stream) == 0:
                    break
                received_data += data_stream
            i = 0
            markers = ['^', '>', 'v', '<']
            received_data = received_data[:12] + markers[agent_rotation] + received_data[12:] #TODO ^ is not going to be rotated properly
            agent_view = ""
            #print "len of thing is", len(received_data)
            while (i < GameState.VIEW_SIZE):
                agent_view = agent_view+received_data[i]
                i += 1
        except (SocketError, IndexError):
            self.sock.close()
            self._nextTurn()
            print "Game Won in", self.getTurn(), "moves."
            exit()
        #self.current_view = agent_view

        self._convertString2List(agent_view)

        # Rotation is incorrect at this point, because you send previous rotation
        # before updating to new one

        # update internal representation of the board
        #TODO support same args as agent.java, but fall back on defaults
        self._storeView(agent_location, agent_rotation)
        self._nextTurn()
        self.printBoard()

    def _convertString2List(self, string):
        i = 0
        j = 0

        self.current_view = []
        while (i < GameState.VIEW_DIM):
            self.current_view.append([])
            i+=1

        i = 0

        #print "string length is ", len(string)
        while (j < GameState.VIEW_SIZE):
            #print "index of string is ", j
            #self.current_view[i].append(string[j])
            if (j % GameState.VIEW_DIM  == 0 and j != 0):
                i+=1
            self.current_view[i].append(string[j])
            j+=1


class Board(object):
    'Board class for internal representation of game board'

    START_LOCATION = (GameState.BOARD_DIM, GameState.BOARD_DIM)

    def __init__(self):
        # make internal board twice as big to guarantee enough space
        side_length = 2 * GameState.BOARD_DIM
        # board is a list of lists initialised to fog
        self.board = []
        for i in range(side_length):
            row = []
            for j in range(side_length):
                row.append(GameState.FEATURES['fog'])
            self.board.append(row)



    # location is a tuple of form (x, y)
    # returns coordinate above
    def getUp(self, location):
        return (location[0], location[1] - 1)


    # returns coordinate to right
    def getRight(self, location):
        return (location[0] + 1, location[1])


    # returns coordinate below
    def getDown(self, location):
        return (location[0], location[1] + 1)


    # returns coordinate to left
    def getLeft(self, location):
        return (location[0] - 1, location[1])


    # returns the contents of the location
    def getLocation(self, location):
        return self.board[location[1]][location[0]]

    # returns adjacent locations that are in the map
    def getAdjacent(self, location):
        valid_adjacent = []
        all_adjacent = {
            'up':       self.getUp(location),
            'right':    self.getRight(location),
            'down':     self.getDown(location),
            'left':     self.getLeft(location)
        }

        for direction, coordinate in all_adjacent.iteritems():
            if all_adjacent[direction] != GameState.FEATURES['edge']:
                valid_adjacent.append(coordinate)

        return valid_adjacent


    def getAdjOnLand(self, location, has_axe, num_dynamite):
        land_adjacent = []
        all_adjacent = self.getAdjacent(location)
        for coordinate in all_adjacent:
            if self.isLand(coordinate):
                land_adjacent.append(coordinate)
            elif self.isTree(coordinate) and has_axe:
                land_adjacent.append(coordinate)
            elif self.isWall(coordinate) and num_dynamite > 0:
                land_adjacent.append(coordinate)
            elif self.isAxe(coordinate):
                land_adjacent.append(coordinate)
            elif self.isDynamite(coordinate):
                land_adjacent.append(coordinate)
            elif self.isGold(coordinate):
                land_adjacent.append(coordinate)
            elif self.isBoat(coordinate):
                land_adjacent.append(coordinate)
        return land_adjacent


    def getAdjOnWater(self, location, has_axe, num_dynamite):
        water_adjacent = []
        all_adjacent = self.getAdjacent(location)
        for coordinate in all_adjacent:
            if self.isWater(coordinate):
                water_adjacent.append(coordinate)
            elif self.isLand(coordinate):
                water_adjacent.append(coordinate)
            elif self.isTree(coordinate) and has_axe:
                water_adjacent.append(coordinate)
            elif self.isWall(coordinate) and num_dynamite > 0:
                water_adjacent.append(coordinate)
            elif self.isAxe(coordinate):
                water_adjacent.append(coordinate)
            elif self.isDynamite(coordinate):
                water_adjacent.append(coordinate)
            elif self.isGold(coordinate):
                water_adjacent.append(coordinate)
            elif self.isBoat(coordinate):
                water_adjacent.append(coordinate)
        return water_adjacent


    def isDynamite(self, location):
        return self.getLocation(location) == GameState.FEATURES['dynamite']


    def isTree(self, location):
        return self.getLocation(location) == GameState.FEATURES['tree']


    def isBoat(self, location):
        return self.getLocation(location) == GameState.FEATURES['boat']


    def isWater(self, location):
        return self.getLocation(location) == GameState.FEATURES['water']


    def isWall(self, location):
        return self.getLocation(location) == GameState.FEATURES['wall']


    def isAxe(self, location):
        return self.getLocation(location) == GameState.FEATURES['axe']


    def isGold(self, location):
        return self.getLocation(location) == GameState.FEATURES['gold']


    def isLand(self, location):
        return self.getLocation(location) == GameState.FEATURES['land']


    def isEdge(self, location):
        return self.getLocation(location) == GameState.FEATURES['land']


    def isFog(self, location):
        return self.getLocation(location) == GameState.FEATURES['fog']


    # returns a list of tuples containing coordinates
    def shortestPath(self, origin, destination):
        path = []
        parent = self.bfs(origin)
        current = destination
        while current != origin:
            path.append(parent[ current[0] ][ current[1] ])

        return reversed(path)


    # Breadth First Search on what has been seen in internal representation of board
    def bfs(self, origin):
        frontier = Queue()
        frontier.put(origin)
        side_length = 2 * GameState.BOARD_DIM
        UNEXPLORED = (0, 0)
        # contains the location that bfs came from, otherwise UNEXPLORED
        parent = [[UNEXPLORED] * side_length] * side_length #TODO worry

        has_axe = False  #TODO  implement these
        num_dynamite = 0

        while not frontier.empty():
            current = frontier.get()
            for adjacent in self.getAdjOnLand(current, has_axe, num_dynamite):  #TODO implement water
                if parent[ adjacent[0] ][ adjacent[1] ] == UNEXPLORED:
                    frontier.put(adjacent)
                    parent[ adjacent[0] ][ adjacent[1] ] = current

        return parent


    def printBoard(self):
        for i in self.board:
            print ' '.join(i)
    
    def directionAdjacent(self, current_location, adjacent):
        # given two coordinates, return direction
        if getUp(current_location) == adjacent:
            return GameState.CARDINAL['north']
        elif getLeft(current_location) == adjacent:
            return GameState.CARDINAL['west']
        elif getDown(current_location) == adjacent:
            return GameState.CARDINAL['south']
        elif getRight(current_location) == adjacent):
            return GameState.CARDINAL['east']

class Agent(object):
    'Agent class for agent of Bounty Game'

    INIT_ROTATION = 0  #change this

    def __init__(self):
        self.state = GameState()
        self.location = self.state.board.START_LOCATION  # start in the middle of the allocated 2D list
        self.origin = self.location
        self.rotation = Agent.INIT_ROTATION  # {0, 1, 2, 3}
        self.is_in_boat = False
        self.num_dynamite = 0
        self.has_axe = False
        self.has_gold = False


    ### getters
    def isInBoat(self):
        return self.is_in_boat


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
        elif (self.rotation == GameState.CARDINAL['east']):
            target = self.state.board.getRight(self.location)
        elif (self.rotation == GameState.CARDINAL['south']):
            target = self.state.board.getDown(self.location)
        else: #(self.rotation == GameState.CARDINAL['west'])
            target = self.state.board.getLeft(self.location)
        return target


    def isFacingDynamite(self):
        return self.state.board.isDynamite(self._getFacing())


    def isFacingTree(self):
        return self.state.board.isTree(self._getFacing())


    def isFacingBoat(self):
        return self.state.board.isBoat(self._getFacing())


    def isFacingWater(self):
        return self.state.board.isWater(self._getFacing())


    def isFacingWall(self):
        return self.state.board.isWall(self._getFacing())


    def isFacingAxe(self):
        return self.state.board.isAxe(self._getFacing())


    def isFacingGold(self):
        return self.state.board.isGold(self._getFacing())


    def isFacingLand(self):
        return self.state.board.isLand(self._getFacing())


    def isFacingEdge(self):
        return self.state.board.isEdge(self._getFacing())


    def canMoveForward(self):
        if self.isFacingLand():
            print 'LAND'
            return True
        if self.isFacingAxe():
            print 'AXE'
            return True
        if self.isFacingDynamite():
            print 'DYNAMITE'
            return True
        if self.isFacingGold():
            print 'GOLD'
            return True
        if self.isFacingBoat():
            return True
        if self.isInBoat():
            print 'IM IN A BOAT'
            if self.isFacingWater():
                return True
            if self.isFacingLand():
                return True
            if self.isFacingAxe():
                return True
            if self.isFacingGold():
                return True
        return False


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
                self.setHasAxe()
            elif self.isFacingDynamite():
                self.gainDynamite()
            elif self.isFacingGold():
                self.setHasGold()
            elif self.isFacingBoat():
                self.setInBoat(True)
            elif self.isInBoat() and self.isFacingLand():
                self.setInBoat(False)

            # note: GameState.sendMove() will update internal representation of the board
            # update agent location
            #self.location = self.state.board.getUp(self.location) #WRONG
            self.location = self._getFacing()
            self.state.sendMove(GameState.MOVES['forward'], self.location, self.rotation)


    def removeTree(self):
        if self.canRemoveTree():
            self.state.sendMove(GameState.MOVES['chop'], self.location, self.rotation)


    def removeWall(self):
        if self.canRemoveWall():
            self.state.sendMove(GameState.MOVES['blast'], self.location, self.rotation)


    def turnLeft(self):
        self.rotation += GameState.DIRECTIONS['left']
        self.rotation %= len(GameState.CARDINAL)
        self.state.sendMove(GameState.MOVES['left'], self.location, self.rotation)


    def turnRight(self):
        self.rotation += GameState.DIRECTIONS['right']
        self.rotation %= len(GameState.CARDINAL)
        self.state.sendMove(GameState.MOVES['right'], self.location, self.rotation)

    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.state.board.getLocation(location)


    ### other methods
    def makeBestMove(self):
        if self.canMoveForward() and random.randint(-1,4):
            self.moveForward()
        else:
            a = random.randint(-1,1)
            print 'hello', a
            if a == 1:
                self.turnLeft()
            else:
                self.turnRight()

        print 'FACING: |' + self.state.board.getLocation(self._getFacing()) + '|', '\t', self._getFacing()
        time.sleep(0.05)


    def userControl(self):
        print 'FACING: |' + self.state.board.getLocation(self._getFacing()) + '|', '\t', self._getFacing()
        print 'Move: ',
        input = raw_input()

        if input == 'f' and self.canMoveForward():
            self.moveForward()
        elif input == 'l':
            self.turnLeft()
        elif input == 'r':
            self.turnRight()
        elif input == 's':
            self.state.board.bfs(self.location)
            raw_input('Enter to continue..')
        elif input == 'b':
            self.removeWall()
        elif input == 'c':
            self.removeTree()            
        else:
            print 'can\'t move!'
            exit()


