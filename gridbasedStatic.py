#!/usr/bin/env python

import random
import pygame, sys
from pygame.locals import *
from decisionF import decisionF

#colors
BLACK = (0, 0, 0 )
RED = (255, 0, 0 ) #walls
WHITE = (255, 255, 255 ) #open space
BLUE = (0, 0, 225 ) #hero
GREEN = (0, 255, 0 ) #portal

#game dimensions
tileSize = 60       #pixel sizes for grid squares
mapSize = 10        #M x M mapSize
margin = 5

#numbers representing
FLOOR = 0
WALL = 1
HERO = 2
PORTAL = 3

#setting up display
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(((mapSize * (margin+tileSize))+margin, (mapSize * (margin+tileSize))+margin))
Done = False
decisionCount = 0


class moveHero():                    #Characters can move around and do cool stuff
    global Done
    def Move(self, decision):

        if decision == "up":
            if self.CollisionCheck("up") == False:          #And nothing in the way
                    if self.PortalCheck("up") == True:
                        Done = True
                        DF.put_result('Portal')
                    elif self.PortalCheck("up") == False:     #No Portal
                       # DF.put_check('No portal')
                        Map.tileMap[Map.heroRow-1][Map.heroColumn] = 2
                        Map.tileMap[Map.heroRow][Map.heroColumn] = 0
                        Map.heroRow = Map.heroRow-1
                        print "Direction:", decision
                        DF.put_result('Success')
        elif decision == "down":
            if self.CollisionCheck("down") == False:          #And nothing in the way
                    if self.PortalCheck("down") == True:     #Portal
                        Done = True
                        DF.put_result('Portal')
                    if self.PortalCheck("down") == False:     #No Portal
                      #  DF.put_check('No portal')
                        Map.tileMap[Map.heroRow+1][Map.heroColumn] = 2
                        Map.tileMap[Map.heroRow][Map.heroColumn] = 0
                        Map.heroRow = Map.heroRow+1
                        print "Direction:", decision
                        DF.put_result('Success')
        elif decision == "right":
            if self.CollisionCheck("right") == False:          #And nothing in the way
                    if self.PortalCheck("right") == True:     #No Portal
                        Done = True
                        DF.put_result('Portal')
                    if self.PortalCheck("right") == False:
                       # DF.put_check('No portal')
                        Map.tileMap[Map.heroRow][Map.heroColumn+1] = 2
                        Map.tileMap[Map.heroRow][Map.heroColumn] = 0
                        Map.heroColumn = Map.heroColumn+1
                        print "Direction:", decision
                        DF.put_result('Success')
        elif decision == "left":
            if self.CollisionCheck("left") == False:          #And nothing in the way
                    if self.PortalCheck("left") == True:
                        Done = True
                        DF.put_result('Portal')
                    if self.PortalCheck("left") == False:     #No Portal
                       # DF.put_check('No portal')
                        Map.tileMap[Map.heroRow][Map.heroColumn-1] = 2
                        Map.tileMap[Map.heroRow][Map.heroColumn] = 0
                        Map.heroColumn = Map.heroColumn-1
                        print "Direction:", decision
                        DF.put_result('Success')
    def CollisionCheck(self, decision):
        if decision == "up":
            if Map.tileMap[Map.heroRow-1][Map.heroColumn] == 1:
                print "Direction:", decision
                DF.put_result('wall')
                return True
        if decision == "down":
            if Map.tileMap[Map.heroRow+1][Map.heroColumn] == 1:
                print "Direction:", decision
                DF.put_result('wall')
                return True
        if decision == "right":
            if Map.tileMap[Map.heroRow][Map.heroColumn+1] == 1:
                print "Direction:", decision
                DF.put_result('wall')
                return True
        if decision == "left":
            if Map.tileMap[Map.heroRow][Map.heroColumn-1] == 1:
                print "Direction:", decision
                DF.put_result('wall')
                return True
       # print "Direction:", decision
       # DF.put_result('Success')
        return False

    def PortalCheck(self, decision):      #checks portal relative to player
        if decision == "up":
            if Map.tileMap[Map.heroRow-1][Map.heroColumn] == 3:
                DF.put_result('portal')
                print "Number of decisions: " + str(decisionCount)
                return True

        if decision == "down":
            if Map.tileMap[Map.heroRow+1][Map.heroColumn] == 3:
                DF.put_result('portal')
                print "Number of decisions: " + str(decisionCount)
                return True

        if decision == "right":
            if Map.tileMap[Map.heroRow][Map.heroColumn+1] == 3:
                DF.put_result('portal')
                print "Number of decisions: " + str(decisionCount)
                return True

        if decision == "left":
            if Map.tileMap[Map.heroRow][Map.heroColumn-1] == 3:
                DF.put_result('portal')
                print "Number of decisions: " + str(decisionCount)
                return True

        return False


class Map(object):              #The main class
    #our map
    tileMap = [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,1,0,0,1],
                [1,0,0,0,0,0,1,0,0,1],
                [1,1,1,1,0,0,1,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ]
    #place maze gangsta
    randomHeroRow = 8 #random.randint(1, mapSize - 2)
    randomHeroColumn = 2 #random.randint(1, mapSize - 2)
    tileMap[randomHeroRow][randomHeroColumn] = 2
    heroRow = randomHeroRow
    heroColumn = randomHeroColumn

    while True:  #make sure gansta doesn't get beemed up at beginning
        randomPortalRow = 2  #random.randint(1, mapSize - 2)
        randomPortalColumn = 8 #random.randint(1, mapSize - 2)
        if randomPortalRow != randomHeroRow & randomPortalColumn != randomHeroColumn:
            break
    #Place portal
    tileMap[randomPortalRow][randomPortalColumn] = 3
    portalRow = randomPortalRow
    portalColumn = randomPortalColumn


Map = Map()
DF = decisionF()
turd = moveHero()


while not Done:     #Main pygame loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
            sys.exit()

    decision = DF.get_decision()
    #result = results(decision)
    if decision == "up":
        turd.Move("up")
    if decision == "down":
        turd.Move("down")
    if decision == "left":
        turd.Move("left")
    if decision == "right":
        turd.Move("right")

    decisionCount += 1

    screen.fill(BLACK)

    # Draw the grid
    for row in range(mapSize):
        for column in range(mapSize):
            color = WHITE
            if Map.tileMap[row][column] == 1:
                color = RED
            if Map.tileMap[row][column] == 0:
                color= WHITE
            if Map.tileMap[row][column] == 2:  #Character
               color = BLUE
            if Map.tileMap[row][column] == 3:  #Portal
               color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(margin + tileSize) * column + margin,
                              (margin + tileSize) * row + margin,
                              tileSize,
                              tileSize])

    #update display
    pygame.display.update()


    clock.tick(20)      #speed of the tile
    pygame.display.flip()

pygame.quit()
