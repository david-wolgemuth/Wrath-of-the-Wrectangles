__author__ = 'David'

import pygame, Constants, Lines
from Constants import *
from pygame import *

width = 10
height = 25

class Players(pygame.sprite.Sprite):

    level = None
    stage = 10

    #Players Groups
    CPUs = pygame.sprite.Group()
    itsMe = pygame.sprite.Group()
    targetedCPUs = pygame.sprite.Group()
    bottomFeeders = pygame.sprite.Group()


    def __init__(self, x, y):

        super().__init__()
        #Width, Height, Color
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(dPURPLE)

        #Rectange, Left, Top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Movement Speed
        self.playerSpeed = 4
        self.sprintSpeedLeft = self.sprintSpeedRight = 0
        self.leftMovement = self.rightMovement = self.verticalMovement = 0

        #Jumping Stuff
        self.leftKey = self.rightKey = False
        self.jumpingRight = self.jumpingLeft = 0
        self.stoppingLeftRightJump = True

        #Health
        self.stagesUnlocked = 1
        self.healthCounter = 0
        self.health = 0
        self.score = 0
        self.topScore = 0
        self.highScores = None
        self.paused = False

    def leftRightJump(self):

        #Slow Down Horizontal Movement If player hits left/right key
        if self.leftKey or self.rightKey:
            self.stoppingLeftRightJump = True
            if self.jumpingLeft > 0:
                self.jumpingLeft -= 0.25
            else:
                self.jumpingLeft = 0
            if self.jumpingRight > 0:
                self.jumpingRight -= 0.25
            else:
                self.jumpingRight = 0

        #Slows Down Horizontal Movement with a mild Drag
        elif not self.stoppingLeftRightJump:
            if self.jumpingLeft > 0:
                self.jumpingLeft -= 0.1
            else:
                self.jumpingLeft = 0
            if self.jumpingRight > 0:
                self.jumpingRight -= 0.1
            else:
                self.jumpingRight = 0

        #Not Sure if this is redundant...
        elif self.stoppingLeftRightJump:
            self.jumpingRight = self.jumpingLeft = 0

            

    def gravity(self):
        #Gravity
        if self.verticalMovement == 0:
            self.verticalMovement = 1
        else: self.verticalMovement += 0.2


    def update(self):

        self.gravity()
        self.leftRightJump()
        self.gotHit()

        #Sprinting
        if self.leftKey:
            if self.sprintSpeedRight > 0:
                self.sprintSpeedRight -= 1
            else:
                self.sprintSpeedRight = 0
        if self.rightKey:
            if self.sprintSpeedLeft > 0:
                self.sprintSpeedLeft -= 1
            else:
                self.sprintSpeedLeft = 0
        if not self.leftKey:
            self.stopLeft()
        if not self.rightKey:
            self.stopRight()
        if self.rect.right > Constants.width * 0.75:
            self.rect.right = Constants.width * 0.74

        #Horizontal Movement / Collision
        self.rect.x += (self.rightMovement - self.leftMovement) + (self.jumpingRight - self.jumpingLeft) + (self.sprintSpeedRight - self.sprintSpeedLeft)

        objectsHit = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for i in objectsHit:
            if self.leftMovement + self.jumpingLeft + self.sprintSpeedLeft > self.rightMovement + self.jumpingRight + self.sprintSpeedRight:
                self.rect.left = i.rect.right
                if self.leftKey and self.verticalMovement >= 0: #Cling to Wall
                    self.verticalMovement -= 0.15
            else:
                self.rect.right = i.rect.left
                if self.rightKey and self.verticalMovement >= 0: #Cling to Wall
                    self.verticalMovement -= 0.15

                    #Stop sprinting / leftright jump
            self.stoppingLeftRightJump = True
            self.sprintSpeedRight = self.sprintSpeedLeft = 0

        #Vertical Movement / Collision
        self.rect.y += self.verticalMovement

        objectsHit = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for i in objectsHit:
            if self.verticalMovement > 0:
                self.rect.bottom = i.rect.top
            elif self.verticalMovement < 0:
                self.rect.top = i.rect.bottom

            self.verticalMovement = 0 #Stops all Vertical Momentum if hits ceiling or floor

            if self.jumpingLeft != 0 or self.jumpingRight != 0: #Stops left / right jump if hit ceiling or floor
                self.jumpingLeft = self.jumpingRight = 0

            #Sprint If Player Touching Floor and Holding Left/Right Key
            if not self.leftKey and self.sprintSpeedLeft > 0:
                self.sprintSpeedLeft -= 0.5
            elif self.leftKey and self.sprintSpeedLeft + self.playerSpeed <= 20:
                self.sprintSpeedLeft += 0.15
            elif self.leftKey and self.sprintSpeedLeft + self.playerSpeed > 20:
                pass
            else:
                self.sprintSpeedLeft = 0

            #Slow Down Sprint If Left/Right Key Lifted
            if not self.rightKey and self.sprintSpeedRight > 0:
                self.sprintSpeedRight -= 0.5
            elif self.rightKey and self.sprintSpeedRight + self.playerSpeed <= 20:
                self.sprintSpeedRight += 0.15
            elif self.rightKey and self.sprintSpeedRight + self.playerSpeed > 20:
                pass
            else:
                self.sprintSpeedRight = 0

    def gotHit(self):

        self.healthCounter += 0.5 #Keep Player from losing Health too quickly

        #CPU group (Floaters / Bullets)
        for cpu in self.CPUs:
            if self.healthCounter > 20 and cpu.attackPlayer:
                collided = pygame.sprite.spritecollide(self, self.CPUs, False)
                if collided:
                    self.health -= 1
                    self.healthCounter = 0
            for bullet in cpu.bullets:
                if pygame.sprite.spritecollide(self, cpu.bullets, False):
                    self.health -= 1
                    bullet.kill()

        #Bottom Feeder Group
        for feeder in self.bottomFeeders:
            if self.healthCounter > 20:
                self.rect.y += 2
                collided = pygame.sprite.spritecollide(self, self.bottomFeeders, False)
                if collided:
                    self.health -= 1
                    self.healthCounter = 0
                self.rect.y -= 2

        #It's Me Group
        for me in self.itsMe:
            if self.healthCounter > 20:
                collided = pygame.sprite.spritecollide(self, self.itsMe, False)
                if collided:
                    self.health -= 1
                    self.healthCounter = 0

    def jump(self):

        #Floor Beneath?
        self.rect.y += 10
        floorsHit = pygame.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 10

        #Wall To Left / Right?
        self.rect.x -= 7
        leftWallsHit = pygame.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.x += 14
        rightWallsHit = pygame.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.x -= 7

        #Start With Floors, Then Check Walls... Then Jump If Applicable...
        if len(floorsHit) > 0:
            self.verticalMovement = -11
        elif len(leftWallsHit) > 0:
            self.verticalMovement = -9
            self.jumpingRight = self.playerSpeed * 2
            self.stoppingLeftRightJump = False
        elif len(rightWallsHit) > 0:
            self.verticalMovement = -9
            self.jumpingLeft = self.playerSpeed * 2
            self.stoppingLeftRightJump = False

    def newShowLines(self, screen):

        #Show Lines Between Player And Shooters
        if self.targetedCPUs:

            for j in self.level.platforms: #Platforms Blocking
                listPlatforms = self.level.platforms.sprites()

            for i in self.targetedCPUs: #Shooter Group
                listCPUs = self.targetedCPUs.sprites()

            for i in listCPUs:
                target = i.rect.center
                if Lines.can_see(self, target, listPlatforms): #Stolen Script.. On "Lines.py"
                    pygame.draw.aaline(screen, (255,255,255), self.rect.center, target, 1)
                    i.shooting = True
                else:
                    i.shooting = False


    def stopJump(self):

        #Slow Down Vertical Movement When SpaceBar Lifted
        if self.verticalMovement < 0:
            self.verticalMovement = self.verticalMovement / 3

    def goLeft(self):
        self.leftMovement += self.playerSpeed

    def stopLeft(self):
        #Player Slides Slightly After Lifting Left
        if self.leftMovement > 0:
            self.leftMovement -= 0.75
        else:
            self.leftMovement = 0

    def goRight(self):
        self.rightMovement += self.playerSpeed

    def stopRight(self):
        #Player Slides Slightly After Lifting Right
        if self.rightMovement > 0:
            self.rightMovement -= 0.75
        else:
            self.rightMovement = 0

    def chooseLevel(self):
        #Return Which Stage Platform Player Is Standing On in Main Menu (Stage Select)
        for i in range(self.stagesUnlocked):
            if self.rect.bottom == self.level.bottom - 80 * (i+1):
                return int(i) + 1
        if self.rect.bottom == self.level.top + 40:
            return 11
        return 0 #Return Nothing If Not on platform

    def chooseLevelText(self):
        #Return which platform player is standing on, between Help / Reset / Credits
        if self.rect.bottom == self.level.bottom - 70 * (1):
            return 'help'
        elif self.rect.bottom == self.level.bottom - 70 * (2):
            return 'reset'
        elif self.rect.bottom == self.level.bottom - 70 * (3):
            return 'credits'

        return None #Return Nothing If Not On Platform

    def chooseCPUs(self):
        #Return which CPUs platform.. Battle Room
        for i in range(15):
            if self.rect.bottom == self.level.bottom - 50 * (i+1):
                return Constants.battleRoomChoices[i]

one = Players(0,0)
print(one.rect)
