# Simple pygame program

# Import and initialize the pygame library

import pygame
import datetime
import random


pygame.init()

LevelData = open("LevelData.txt", "r")

boardWidth = 1250
boardHeight = 750

GameBoard = pygame.display.set_mode([boardWidth, boardHeight])

pygame.display.set_caption("Space Invaders")

xCord = 1150
yCord = 700
width = 30
playerSpeed = 7.5
projectileSpeed = 10
alienProjectileSpeed = -10
running = True
clock = pygame.time.Clock()
red = (255, 0, 0)
maxAliens = 5
alienMoveXDist = 10
alienYStart = 10
alienXStart = 360
alienFireRate = 2.0
lineTimeOnScreen = 20



def redrawBoard():
    GameBoard.fill((0, 0, 0))
    for alien in alienList:
        alien.drawAlien(GameBoard)
    for line in lineList:
        if len(lineList) != 0:
            line.drawLeftLine(GameBoard)
            line.drawRightLine(GameBoard)
            line.counter -= 1
            if line.counter == 0:
                lineList.pop(lineList.index(line))
    playerObject.drawPlayer(GameBoard)
    for pProjectile in playerProjectiles:
        pProjectile.drawProjectile(GameBoard)
    for aProjectile in alienProjectiles:
        aProjectile.drawProjectile(GameBoard)
    pygame.display.update()


#class levelData(object):
    #def __init__(self, alienAmount, alienStartX, alienStartY):


class player(object):
    def __init__(self, playerXCord, playerYCord, playerWidth, playerSpeed, playerColor):
        self.playerXCord = playerXCord
        self.playerYCord = playerYCord
        self.playerWidth = playerWidth
        self.playerSpeed = playerSpeed
        self.playerColor = playerColor

    def drawPlayer(self, GameBoard):
        pygame.draw.rect(GameBoard, self.playerColor, (self.playerXCord, self.playerYCord, self.playerWidth, self.playerWidth))


class projectile(object):
    def __init__(self, pXCord, pYCord, radius, color):
        self.pXCord = pXCord
        self.pYCord = pYCord
        self.radius = radius
        self.color = color
        self.projectileSpeed = projectileSpeed

    def drawProjectile(self, GameBoard):
        pygame.draw.circle(GameBoard, self.color, (self.pXCord, self.pYCord), self.radius)


class aliens(object):
    def __init__(self, aXCord, aYCord, radius, color):
        self.aXCord = aXCord
        self.aYCord = aYCord
        self.radius = radius
        self.color = color
        self.projectileSpeed = projectileSpeed
        self.hitBox = (self.aXCord - 17, self.aYCord - 17, 35, 35)

    def drawAlien(self, GameBoard):
        pygame.draw.circle(GameBoard, self.color, (self.aXCord, self.aYCord), self.radius)
        self.hitBox = (self.aXCord - 17, self.aYCord - 17, 35, 35)
        pygame.draw.rect(GameBoard, (255, 0, 0), self.hitBox, 2)

    def hitDetection(self):
        print("hit")
        pass

    def moveAlien(self, xCord, yCord):
        self.aXCord = self.aXCord + xCord
        self.aYCord = self.aYCord + yCord


class lines(object):
    def __init__(self, xCordLine, yCordLine, lineColor, lineLength, counter):
        self.xCordLine = xCordLine
        self.yCordLine = yCordLine
        self.lineColor = lineColor
        self.lineLength = lineLength
        self.counter = counter

    def drawLeftLine(self, GameBoard):
        pygame.draw.line(GameBoard, self.lineColor, (self.xCordLine - 17, self.yCordLine - 17),
                         (self.xCordLine - 17 + self.lineLength * 2, self.yCordLine - 17 + self.lineLength * 2), 3)

    def drawRightLine(self, GameBoard):
        pygame.draw.line(GameBoard, self.lineColor, (self.xCordLine - 17 + self.lineLength * 2, self.yCordLine - 17),
                         (self.xCordLine - 17, self.yCordLine - 17 + self.lineLength * 2), 3)

    def moveLine(self, xMove, yMove):
        self.xCordLine += xMove
        self.yCordLine += yMove


def initializeAliens():
    alienYStart = 10
    alienXStart = 360
    count = 1
    for i in range(0, maxAliens):
        if((len(alienList) % 10 == 0)):
            alienYStart += 50
            count = 1
        alienXPosition = alienXStart + count * 60
        alienList.append(aliens(alienXPosition, alienYStart, 16, (0, 0, 255)))
        count += 1


def defineLeftEnd():
    min = alienList[0]
    for alien in alienList:
        if alien.aXCord < min.aXCord:
            min = alien
    return min


def defineRightEnd():
    max = alienList[0]
    for alien in alienList:
        if alien.aXCord > max.aXCord:
            max = alien
    return max

def defineEnds():
    return defineLeftEnd(), defineRightEnd()


def initializePlayer():
    playerObject = player(1150, 700, 30, 7.5, red)
    return playerObject


playerObject = initializePlayer()
playerRightMoveLimit = boardWidth - playerObject.playerWidth - 5
playerProjectiles = []
alienProjectiles = []
lineList = []
projectileTimeStamp = datetime.datetime.now()
alienMoveTimeStamp = datetime.datetime.now()
alienProjectileTimeStamp = datetime.datetime.now()
alienList = []
initializeAliens()
leftMostAlien, rightMostAlien = defineEnds()
#leftMostAlien = defineLeftEnd()
#rightMostAlien = defineRightEnd()
print(rightMostAlien.aXCord)


while running:
    clock.tick(60)
    timeNow = datetime.datetime.now()
    alienTime = timeNow - alienMoveTimeStamp
    alienProjectileTime = timeNow - alienProjectileTimeStamp

    if alienProjectileTime.seconds >= alienFireRate:
        sp = random.choice(alienList)
        ap = projectile(round(sp.aXCord + sp.radius // 2), round(sp.aYCord + sp.radius // 2), 6, (255, 255, 255))
        alienProjectiles.append(ap)
        alienProjectileTimeStamp = datetime.datetime.now()

    for aProjectile in alienProjectiles:
        if aProjectile.pYCord < boardHeight and aProjectile.pYCord > 0:
            aProjectile.pYCord -= alienProjectileSpeed
            if aProjectile.pYCord > playerObject.playerYCord - width and aProjectile.pYCord < playerObject.playerYCord:
               if aProjectile.pXCord > playerObject.playerXCord and aProjectile.pXCord < playerObject.playerXCord + width:
                 pygame.quit()
                 exit()

        else:
            alienProjectiles.pop(alienProjectiles.index(aProjectile))

    if alienMoveXDist < 0 and leftMostAlien.aXCord + alienMoveXDist < 40:
        alienMoveXDist = alienMoveXDist * -1
        for alien in alienList:
            alien.aYCord += 10
        for line in lineList:
            if len(lineList) != 0:
                line.yCordLine += 10
    if alienMoveXDist > 0 and rightMostAlien.aXCord + alienMoveXDist > boardWidth - rightMostAlien.radius - 30:
        alienMoveXDist = alienMoveXDist * -1
        for alien in alienList:
            alien.aYCord += 10
        for line in lineList:
            if len(lineList) != 0:
                line.yCordLine += 10

    for alien in alienList:
        if alienTime.microseconds / 1000000 > .9:
            alienMoveTimeStamp = datetime.datetime.now()
            alien.moveAlien(alienMoveXDist, 0)

    for line in lineList:
        if alienTime.microseconds / 1000000 > .9:
            alienMoveTimeStamp = datetime.datetime.now()
            line.moveLine(alienMoveXDist, 0)

    for pProjectile in playerProjectiles:
        for alien in alienList:
            if pProjectile.pYCord - pProjectile.radius < alien.hitBox[1] + alien.hitBox[3] and pProjectile.pYCord + pProjectile.radius > alien.hitBox[1]:
                if pProjectile.pXCord - pProjectile.radius > alien.hitBox[0] and pProjectile.pXCord - pProjectile.radius < alien.hitBox[0] + alien.hitBox[2]:
                    alien.hitDetection()
                    playerProjectiles.pop(playerProjectiles.index(pProjectile))
                    xLine = alien.aXCord
                    yLine = alien.aYCord
                    lineRadius = alien.radius
                    lineList.append(lines(xLine, yLine, red, lineRadius, lineTimeOnScreen))
                    #pygame.draw.line(GameBoard, red, (xLine - 17, yLine - 17), (xLine - 17 + lineRadius * 2, yLine - 17 + lineRadius * 2), 3)
                    #pygame.draw.line(GameBoard, red, (xLine - 17 + lineRadius * 2, yLine - 17), (xLine - 17, yLine - 17 + lineRadius * 2), 3)
                    #pygame.display.flip()
                    alienList.pop(alienList.index(alien))
                    if not alienList:
                        maxAliens += 5
                        if(alienMoveXDist < 0):
                            alienMoveXDist *= -1
                        alienMoveXDist += 15
                        alienYStart += 10
                        alienXStart += 360
                        alienFireRate -= .5
                        initializeAliens()
                        initializePlayer()
                        redrawBoard()
                        leftMostAlien = defineLeftEnd()
                        rightMostAlien = defineRightEnd()
                        lineList = []
                        break
                    leftMostAlien = defineLeftEnd()
                    rightMostAlien = defineRightEnd()
                    print(rightMostAlien.aXCord)


        if pProjectile.pYCord < boardHeight and pProjectile.pYCord > 0:
            pProjectile.pYCord -= projectileSpeed
        else:
            playerProjectiles.pop(playerProjectiles.index(pProjectile))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()

    keyPress = pygame.key.get_pressed()

    timeDiff = timeNow - projectileTimeStamp
    if keyPress[pygame.K_SPACE]:
        if len(playerProjectiles) < 5 and timeDiff.microseconds / 1000000 > .5:
            playerProjectiles.append(projectile(round(playerObject.playerXCord + width // 2), round(playerObject.playerYCord + width // 2), 6, (255, 255, 255)))
            projectileTimeStamp = datetime.datetime.now()

    if keyPress[pygame.K_LEFT] and playerObject.playerXCord > playerSpeed:
        playerObject.playerXCord -= playerObject.playerSpeed
    if keyPress[pygame.K_RIGHT] and playerObject.playerXCord < playerRightMoveLimit:
        playerObject.playerXCord += playerObject.playerSpeed
    redrawBoard()
pygame.quit()


