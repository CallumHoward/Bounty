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

        #receiving = True
        #while receiving:
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
            #if receiving == False:
            #    break
            i = 0
            #print "out of first loop"
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
        except SocketError as e:
            self.sock.close()
            #break
            #print "stuck in outer loop"
        print agent_view
        #print "size of thing is", len(agent_view)
        self.current_view = agent_view


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

        # Change VIEW_SIZE to 29 - since it must include the newline characters
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
            received_data = received_data[:12]+"^"+received_data[12:]
            agent_view = ""
            while (i < 25):
                agent_view = agent_view+received_data[i]
                i += 1
        except SocketError as e:
            self.sock.close()
            # TODO add in Game Lost or Game Won message if needed for Agent file

        self.current_view = agent_view
        # update internal representation of the board
        self._storeView(agent_location, agent_rotation)
        self._nextTurn()
        self.board.printBoard()


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


    # returns the contents of the location
    def getLocation(self, location):
        return self.board[location[0]][location[1]]

    # returns adjacent locations that are in the map
    def getAdjacent(self, location):
        valid_adjacent = []
        all_adjacent = {
            'up':       self.getUp(location),
            'right':    self.getRight(location),
            'down':     self.getDown(location),
            'left':     self.getLeft(location)
        }

        for direction, coordinate in all_adjacent:
            if all_adjacent[direction] != GameState.FEATURES['edge']:
                valid_adjacent.append(coordinate)

        return valid_adjacent


    def getAdjOnLand(self, location, has_axe, num_dynamite):
        land_adjacent = []
        all_adjacent = self.getAdjacent(location)
        for coordinate in all_adjacent:
            if self.island(location):
                land_adjacent.append(coordinate)
            elif self.istree(coordinate) and has_axe:
                land_adjacent.append(coordinate)
            elif self.iswall(coordinate) and num_dynamite > 0:
                land_adjacent.append(coordinate)
            elif self.isaxe(coordinate):
                land_adjacent.append(coordinate)
            elif self.isdynamite(coordinate):
                land_adjacent.append(coordinate)
            elif self.isgold(coordinate):
                land_adjacent.append(coordinate)
            elif self.isboat(coordinate):
                land_adjacent.append(coordinate)
        return land_adjacent


    def getAdjOnWater(self, location, has_axe, num_dynamite):
        water_adjacent = []
        all_adjacent = self.getAdjacent(location)
        for coordinate in all_adjacent:
            if self.isWater(coordinate):
                water_adjacent.append(coordinate)
            elif self.island(location):
                water_adjacent.append(coordinate)
            elif self.istree(coordinate) and has_axe:
                water_adjacent.append(coordinate)
            elif self.iswall(coordinate) and num_dynamite > 0:
                water_adjacent.append(coordinate)
            elif self.isaxe(coordinate):
                water_adjacent.append(coordinate)
            elif self.isdynamite(coordinate):
                water_adjacent.append(coordinate)
            elif self.isgold(coordinate):
                water_adjacent.append(coordinate)
            elif self.isboat(coordinate):
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
            return True
        if self.isFacingAxe():
            return True
        if self.isFacingDynamite():
            return True
        if self.isFacingGold():
            return True
        if self.isFacingBoat():
            return True
        if self.isInBoat():
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
        self.rotation %= len(GameState.CARDINAL)


    def turnRight(self):
        self.state.sendMove(GameState.MOVES['right'], self.location, self.rotation)
        self.rotation += GameState.DIRECTIONS['right']
        self.rotation %= len(GameState.CARDINAL)


    # location is a tuple of form (x, y)
    def getBoardLocation(self, location):
        return self.board.getLocation()


    ### other methods
    def makeBestMove(self):
        if self.canMoveForward():
            best_move = GameState.MOVES['forward']

        return best_move


def main():
    #TODO support same args as agent.java, but fall back on defaults
    agent = Agent()
    agent.state.printBoard()

    while agent.state.getTurn() <= GameState.MAX_MOVES:
        agent.makeBestMove()


# call main function only if not imported as a module
if __name__ == '__main__':
   main()
