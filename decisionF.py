import random
import sys
import numpy as np
import collections
import pickle
import os

#Decision Factory class
class decisionF:
    def __init__ ( self, name= 'Davros' ):
        self.name = name
        self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
        self.last_result = 'Success'
        self.last_direction = 'down' #stores last direction moved
        self.switchx = 'right' #for switching directions left or right
        self.switchy = 'up' #for switching directions up or down
        self.pivot = 'up' #switching directions
        self.trackRow = 20 #for origin
        self.trackColumn = 20 #for origin
        self.trackMapTemp = [['' for j in range(40)] for i in range(40)] #for keeping track of moves/walls
        self.portal = (0,0)
        self.start = (20,20)
        self.position = (0,0)
        self.next = (21,20)
        self.secondRun = 0
        self.trackMapFinal = np.zeros((40, 40), dtype=int)
        self.exists = os.path.isfile('dump.txt')
        self.path = []
        if self.exists:
            self.fileR = open('dump.txt', 'r')
            self.path = pickle.load(self.fileR)
            self.fileR.close()
            self.fileR = open('dump2.txt', 'r')
            self.secondRun = pickle.load(self.fileR)
            self.fileR.close()

    # origin @ (20,20) in 40x40 2d array (i'm sure there is a more "intelligent" way of doing this)
    def put_trackMap_success(self): # keeping track of tiles visited placing a 1 on success
        if self.last_direction == "up":
            self.trackMapTemp[self.trackRow-1][self.trackColumn] = 2
            self.trackMapFinal[self.trackRow-1][self.trackColumn] = 2
            self.trackRow = self.trackRow-1
        elif self.last_direction == "down":
            self.trackMapTemp[self.trackRow+1][self.trackColumn] = 2
            self.trackMapFinal[self.trackRow+1][self.trackColumn] = 2
            self.trackRow = self.trackRow+1
        elif self.last_direction == "right":
            self.trackMapTemp[self.trackRow][self.trackColumn+1] = 2
            self.trackMapFinal[self.trackRow][self.trackColumn+1] = 2
            self.trackColumn = self.trackColumn+1
        elif self.last_direction == "left":
            self.trackMapTemp[self.trackRow][self.trackColumn-1] = 2
            self.trackMapFinal[self.trackRow][self.trackColumn-1] = 2
            self.trackColumn = self.trackColumn-1

    def put_trackMap_wall(self): # keeping track of tiles of walls placing a 2
        if self.last_direction == "up":
            self.trackMapTemp[self.trackRow-1][self.trackColumn] = 1
            self.trackMapFinal[self.trackRow-1][self.trackColumn] = 1
        elif self.last_direction == "down":
            self.trackMapTemp[self.trackRow+1][self.trackColumn] = 1
            self.trackMapFinal[self.trackRow+1][self.trackColumn] = 1
        elif self.last_direction == "right":
            self.trackMapTemp[self.trackRow][self.trackColumn+1] = 1
            self.trackMapFinal[self.trackRow][self.trackColumn+1] = 1
        elif self.last_direction == "left":
            self.trackMapTemp[self.trackRow][self.trackColumn-1] = 1
            self.trackMapFinal[self.trackRow][self.trackColumn-1] = 1

    def get_decision(self, verbose = True): #return move to framework
        if self.last_result == 'Portal':
            self.port()

        if self.secondRun: # If this is second Run
            return self.second()


        if not self.path:
            return self.better_direction()

    def random_direction(self): #for random decision
        r = random.randint(1,4)
        self.last_direction = self.directions[r]
        return self.directions[r]

    def put_result(self, result): #keep track of last result
        self.last_result = result

    def bfs(self):
        width = 40
        height = 40
        queue = collections.deque([[self.start]])
        seen = set([self.start])
        while queue:
            pathTemp = queue.popleft()
            x, y = pathTemp[-1]
            if self.trackMapFinal[x][y] == 3:
                return pathTemp
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < width and 0 <= y2 < height and self.trackMapFinal[x2][y2] != 0 and self.trackMapFinal[x2][y2] != 1 and (x2, y2) not in seen:
                    queue.append(pathTemp + [(x2, y2)])
                    seen.add((x2, y2))

    def second(self):
        self.position = self.next
        self.next = self.path.pop(0)

        if self.next[0] < self.position[0]:
            return self.directions[1]
        elif self.next[0] > self.position[0]:
            return self.directions[2]
        elif self.next[1] > self.position[1]:
            return self.directions[3]
        elif self.next[1] < self.position[1]:
            return self.directions[4]
        else:
            print "You screwed up!!!!" , self.path
            sys.exit()
            os.remove('dump.txt')
            os.remove('dump2.txt')

    def port(self): #when portal is found do some stuff
        if self.secondRun: #remove variable files
            os.remove('dump.txt')
            os.remove('dump2.txt')
            sys.exit()
        if self.last_direction == "up":
            self.portal = (self.trackRow-1,self.trackColumn)
            self.trackMapFinal[self.trackRow-1][self.trackColumn] = 3
            self.trackRow = self.trackRow-1
        elif self.last_direction == "down":
            self.portal = (self.trackRow+1,self.trackColumn)
            self.trackMapFinal[self.trackRow+1][self.trackColumn] = 3
            self.trackRow = self.trackRow+1
        elif self.last_direction == "right":
            self.portal = (self.trackRow,self.trackColumn+1)
            self.trackMapFinal[self.trackRow][self.trackColumn+1] = 3
            self.trackColumn = self.trackColumn+1
        elif self.last_direction == "left":
            self.portal = (self.trackRow,self.trackColumn-1)
            self.trackMapFinal[self.trackRow][self.trackColumn-1] = 3
            self.trackColumn = self.trackColumn-1
        self.trackMapFinal[20][20] = 5 #for us to visualize when printing matrix

        #set path for second run
        self.path = self.bfs()
        self.secondRun = 1

        #save to file for second run
        self.fileW = open('dump.txt', 'w')
        pickle.dump(self.path, self.fileW)
        self.fileW.close()
        self.fileW = open('dump2.txt', 'w')
        pickle.dump(self.secondRun, self.fileW)
        self.fileW.close()

        sys.exit()

    def better_direction(self): # better than random decision

        #Didn't hit a wall and last move wasn't a portal or second run
        if self.last_result == 'Success': #basicly keep it moving until hits wall
            self.put_trackMap_success()

            #the main deal hear is the "pivot" if the agent can't traverse rows any longer
            if self.pivot == 'up': #traversing the tile map one row at a time moving upwards
                if self.last_direction == 'up': #('up')
                    if self.switchx == 'right':
                        self.switchx = 'left'
                        self.last_direction = self.directions[4]
                        return self.directions[4] #start moving to the left
                    elif self.switchx == 'left':
                        self.switchx = 'right'
                        self.last_direction = self.directions[3]
                        return self.directions[3] #start moving to the right
                else: #keeps moving up until hits wall
                    return self.last_direction
            if self.pivot == 'down': #traversing the tile map one row at a time in a downward motion
                if self.last_direction == 'down': #('down'):
                    if self.switchx == 'right':
                        self.switchx = 'left'
                        self.last_direction = self.directions[4]
                        return self.directions[4] #start moving to the left
                    elif self.switchx == 'left':
                        self.switchx = 'right'
                        self.last_direction = self.directions[3]
                        return self.directions[3] #start moving right
                else: #keeps going down until hits wall
                    return self.last_direction
            if self.pivot == 'right': #traversing the tile map one column at a time heading right
                if self.last_direction == 'right': #('right'):
                    if self.switchy == 'up':
                        self.switchy = 'down'
                        self.last_direction = self.directions[2]
                        return self.directions[2] #start moving downward
                    elif self.switchy == 'down':
                        self.switchy = 'up'
                        self.last_direction = self.directions[1]
                        return self.directions[1] #start moving upward
                else: #keeps going right until hits wall
                    return self.last_direction
            if self.pivot == 'left': #traversing the tile map one column at a time heading left
                if self.last_direction == 'left': #('left'):
                    if self.switchy == 'up':
                        self.switchy = 'down'
                        self.last_direction = self.directions[2]
                        return self.directions[2] #start moving downward
                    elif self.switchy == 'down':
                        self.switchy = 'up'
                        self.last_direction = self.directions[1]
                        return self.directions[1] #start moving upward
                else: #keeps going left until hits wall
                    return self.last_direction

        if self.last_result == 'wall': #these functions change stuff up to change row,column, or direction
            self.put_trackMap_wall()
            if self.pivot == 'up': #traversing the tile map one row at a time moving upwards
                if self.last_direction == 'up': #can't search rows upwards any longer
                    self.trackMapTemp = [['' for j in range(40)] for i in range(40)] #clear the "trackMapTemp"
                    self.pivot = 'down' #switch the piviot to search rows heading downwards
                    self.last_direction = self.directions[2]
                    return self.directions[2]
                elif self.last_direction == 'down': #this is just here to get agent down as far as possible before searching rows up
                    if self.switchx == 'right':
                        self.switchx = 'left'
                        self.last_direction = self.directions[4]
                        return self.directions[4] #start moving left
                    elif self.switchx == 'left':
                        self.switchx = 'right'
                        self.last_direction = self.directions[3]
                        return self.directions[3] #start moving right
                elif self.last_direction == 'left' or 'right' : #hits wall so move up a row
                    self.last_direction = self.directions[1]
                    return self.directions[1]
                else:
                    oops = self.random_direction() #if all else fails generate a random decision
                    return oops
            if self.pivot == 'down':
                if self.last_direction == 'down': #can't search rows downwards any longer
                    self.trackMapTemp = [['' for j in range(40)] for i in range(40)]
                    self.pivot = 'right' #switch the piviot to search columns heading right
                    self.last_direction = self.directions[1]
                    return self.directions[1]
                elif self.last_direction == 'up':
                    if self.switchx == 'right':
                        self.switchx = 'left'
                        self.last_direction = self.directions[4]
                        return self.directions[4] #moves in new direction
                    elif self.switchx == 'left':
                        self.switchx = 'right'
                        self.last_direction = self.directions[3]
                        return self.directions[3] #moves in new direction
                elif self.last_direction == 'left' or 'right' :
                    self.last_direction = self.directions[2]
                    return self.directions[2]
                else:
                    oops = self.random_direction() #if all else fails generate a random decision
                    return oops
            if self.pivot == 'right':
                if self.last_direction == 'right':
                    self.trackMapTemp = [['' for j in range(40)] for i in range(40)]
                    self.pivot = 'left'
                    self.last_direction = self.directions[4]
                    return self.directions[4]
                elif self.last_direction == 'left':
                    if self.switchy == 'up':
                        self.switchy = 'down'
                        self.last_direction = self.directions[2]
                        return self.directions[2] #moves in new direction
                    elif self.switchy == 'down':
                        self.switchy = 'up'
                        self.last_direction = self.directions[1]
                        return self.directions[1] #moves in new direction
                elif self.last_direction == 'up' or 'down' :
                    self.last_direction = self.directions[3]
                    return self.directions[3]
                else:
                    oops = self.random_direction() #if all else fails generate a random decision
                    return oops
            if self.pivot == 'left':
                if self.last_direction == 'left':
                    self.trackMapTemp = [['' for j in range(40)] for i in range(40)]
                    self.pivot = 'up'
                    self.last_direction = self.directions[1]
                    return self.directions[1]
                elif self.last_direction == 'right':
                    if self.switchy == 'up':
                        self.switchy = 'down'
                        self.last_direction = self.directions[2]
                        return self.directions[2] #moves in new direction
                    elif self.switchy == 'down':
                        self.switchy = 'up'
                        self.last_direction = self.directions[1]
                        return self.directions[1] #moves in new direction
                elif self.last_direction == 'up' or 'down' :
                    self.last_direction = self.directions[4]
                    return self.directions[4]
                else:
                    oops = self.random_direction() #if all else fails generate a random decision
                    return oops

        else:
            oops = self.random_direction()
            return oops
