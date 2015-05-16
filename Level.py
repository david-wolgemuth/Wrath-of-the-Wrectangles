__author__ = 'David'

import pygame, Constants, random, Player, CPUs, Stages

class Rectangles(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        #Image
        self.image = pygame.Surface([width,height])
        self.color = color
        self.image.fill(self.color)

        #Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.player = None

class Level_One(object):
    def __init__(self, player):

        self.player = player

        #Lists and Groups
        platforms = []
        self.platforms = pygame.sprite.Group()
        self.surroundingPlatforms = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.levelLoadPlatforms = pygame.sprite.Group()

        self.bottomFeeders = pygame.sprite.Group()
        self.coins = []
        self.healthBoxes = []
        self.floaters = pygame.sprite.Group()
        self.itsMe = pygame.sprite.Group()
        self.targetingFloaters = pygame.sprite.Group()

        #World Shift
        self.worldShiftX = 0
        self.worldShiftY = 0

        #Current Stage
        self.currentStage = Stages.whichStage[self.player.stage]

        #Size of Level
        self.width = Constants.width
        self.height = Constants.height
        self.left = -self.width * 0.25
        self.right = self.width * 0.75
        self.top = -self.height * 0.25
        self.bottom = self.height * 0.75
        wallwidth = 10


        #Level Boundary Walls:
        leftWall = (-self.width * 0.25, -self.height * 0.25, wallwidth, self.height)
        rightWall = (self.width * 0.75, -self.height * 0.25, wallwidth, self.height)
        topWall = (-self.width * 0.25, -self.height * 0.25, self.width, wallwidth)
        bottomWall = (-self.width * 0.25, self.height * 0.75, self.width + wallwidth, wallwidth)

        surroundingPlatforms = [leftWall,rightWall,topWall,bottomWall]

        for i in range(len(surroundingPlatforms)):
            platforms.append(surroundingPlatforms[i])


        #Level Select
        if self.currentStage == Stages.LevelSelect:

            #Unlocked Stages, Rectangles to Stand On
            for i in range(self.player.stagesUnlocked):
                platforms.append((self.left + i * 300 + 50, self.bottom - 80 * (i+1), 200, wallwidth))

            if self.player.stagesUnlocked == 11:
                platforms.append((self.left + 50, self.top + 40, 200, wallwidth))

            #About Me / Options / Reset
            for i in range(3):
                platforms.append((self.right - (i + 1) * 200, self.bottom - 70 * (i+1), 100, wallwidth))

            for i in platforms:
                platform = Rectangles(i[0],i[1],i[2],i[3], Constants.cPURPLE)
                self.platforms.add(platform)

            #Clouds
            clouds = []
            for i in range(15):
                size = random.randint(100, 300)
                clouds.append((random.randint(-self.width * 0.3, self.width),
                                  random.randint(-self.height * 0.3, self.height),
                                  size,
                                  size,
                                  ))
            for i in clouds:
                cloud = Rectangles(i[0],i[1],i[2],i[3], Constants.aPURPLE)
                self.clouds.add(cloud)


        #The Battle Room
        elif self.currentStage == Stages.WonGame:

            #Clouds
            clouds = []
            for i in range(15):
                size = random.randint(100, 300)
                clouds.append((random.randint(-self.width * 0.3, self.width),
                                  random.randint(-self.height * 0.3, self.height),
                                  size,
                                  size,
                                  ))
            for i in clouds:
                cloud = Rectangles(i[0],i[1],i[2],i[3], Constants.aPURPLE)
                self.clouds.add(cloud)

            #Special Platforms, To Add / Remove CPUs
            for i in range(15):
                platforms.append((random.randint(self.left + 200, self.right - 200), self.bottom - 50 * (i+1), 100, wallwidth))

            #horizontal
            for i in range(40):
                platforms.append((random.randrange(-self.width * 0.25 + wallwidth + Player.width, self.width * 0.75 - (4 * wallwidth + Player.width), Player.width),
                                  random.randrange(-self.height * 0.25 + wallwidth + Player.height, self.height * 0.75 - (2*wallwidth + Player.height), Player.height),
                                  wallwidth * 4,
                                  wallwidth,
                                  ))

            #vertical
            for i in range(40):
                platforms.append((random.randrange(-self.width * 0.25 + wallwidth + Player.width, self.width * 0.75 - (2 * wallwidth + Player.width), Player.width),
                                  random.randrange(-self.height * 0.25 + wallwidth + Player.height, self.height * 0.75 - (4*wallwidth + Player.height), Player.height),
                                  wallwidth,
                                  wallwidth * 4,
                                  ))

            #Add to Platforms
            for i in platforms:
                platform = Rectangles(i[0],i[1],i[2],i[3], Constants.cPURPLE)
                self.platforms.add(platform)



        #Normal Stages
        else:
            #platforms
            length = 300
            height = 200

            #Horizontal Platforms
            for i in range(18):
                platforms.append((random.randrange(-self.width * 0.25 + wallwidth + Player.width, self.width * 0.75 - (length + wallwidth + Player.width), Player.width),
                                  random.randrange(-self.height * 0.25 + wallwidth + Player.height, self.height * 0.75 - (wallwidth + Player.height), Player.height),
                                  length,
                                  wallwidth,
                                  ))

            #Vertical Platforms
            for i in range(10):
                platforms.append((random.randrange(-self.width * 0.25 + wallwidth + Player.width, self.width * 0.75 - (wallwidth + Player.width), Player.width),
                                  random.randrange(-self.height * 0.25 + wallwidth + Player.height, self.height * 0.75 - (height + wallwidth + Player.height), Player.height),
                                  wallwidth,
                                  height,
                                  ))

            for i in platforms:
                platform = Rectangles(i[0],i[1],i[2],i[3], Constants.cPURPLE)
                self.platforms.add(platform)

            #Clouds
            clouds = []
            for i in range(15):
                size = random.randint(100, 300)
                clouds.append((random.randint(-self.width * 0.3, self.width),
                                  random.randint(-self.height * 0.3, self.height),
                                  size,
                                  size,
                                  ))
            for i in clouds:
                cloud = Rectangles(i[0],i[1],i[2],i[3], Constants.aPURPLE)
                self.clouds.add(cloud)

            #Coins
            for i in range(10):
                self.coins.append(CPUs.Coin(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6),self.player,self.platforms))

            #Health Box
            for i in range(1):
                self.healthBoxes.append(CPUs.HealthBox(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6),self.player,self.platforms))

            #Bottom Feeders
            for i in range(self.currentStage['bottom feeders']):
                i = CPUs.BottomFeeder(random.randint(-self.width * 0.1, self.width * 0.6))
                i.player = self.player
                self.platforms.add(i)
                i.walls = self.platforms
                self.bottomFeeders.add(i)

            #It's Me
            for i in range(self.currentStage['itsme']):
                i = CPUs.ItsMe(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6))
                i.player = self.player
                i.walls = self.platforms
                self.platforms.add(i)
                self.itsMe.add(i)


            #Normal Size Floaters
            for i in range(self.currentStage['normal floaters']):
                i = CPUs.floater(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6), 15, 15, 4, 0.2)
                i.player = self.player
                self.platforms.add(i)
                i.walls = self.platforms
                self.floaters.add(i)

            #Large Size Floaters
            for i in range(self.currentStage['large floaters']):
                i = CPUs.floater(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6), 30, 30, 2.5, 0.12)
                i.player = self.player
                self.platforms.add(i)
                i.walls = self.platforms
                #i.walls.add(i)
                self.floaters.add(i)

            #Huge Size Floaters
            for i in range(self.currentStage['huge floaters']):
                i = CPUs.floater(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6), 60, 60, 1.0, 0.1)
                i.player = self.player
                self.platforms.add(i)
                i.walls = self.platforms
                #i.walls.add(self.floaters)
                self.floaters.add(i)
                #self.targetingFloaters.add(i)

            #Tiny Size Floaters
            for i in range(self.currentStage['tiny floaters']):
                i = CPUs.floater(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6), 5, 5, 3.5, 0.2)
                i.player = self.player
                self.platforms.add(i)
                i.walls = self.platforms
                #self.floaters.add(i)

            #Shooting Floaters
            for i in range(self.currentStage['shooters']):
                i = i = CPUs.floater(random.randint(-self.width * 0.1, self.width * 0.6),random.randint(-self.height * 0.1, self.height * 0.6), 5, 5, 1.5, 0.05)
                i.player = self.player
                i.walls = self.platforms
                self.floaters.add(i)
                self.targetingFloaters.add(i)


    def worldShift(self, x, direction):
        #Shift in the Platform or Cloud Plane
        x = int(x)

        #Horizontal Movement
        if direction == 'x':
            self.worldShiftX += x
            self.right += x
            self.left += x
            for platform in self.platforms:
                platform.rect.x += x
            for coin in self.coins:
                coin.rect.x += x
            for cloud in self.clouds:
                cloud.rect.x += x/2 #Cloud Plane moves at different speed
            for box in self.healthBoxes:
                box.rect.x += x
            for floater in self.targetingFloaters:
                floater.rect.x += x
                for bullet in floater.bullets:
                    bullet.rect.x += x

        #Vertical Movement
        if direction == 'y':
            self.worldShiftY += x
            self.top += x
            self.bottom += x
            for platform in self.platforms:
                platform.rect.y += x
            for coin in self.coins:
                coin.rect.y += x
            for cloud in self.clouds:
                cloud.rect.y += x/2 #Cloud Plane moves at different speed
            for box in self.healthBoxes:
                box.rect.y += x
            for floater in self.targetingFloaters:
                floater.rect.y += x
                for bullet in floater.bullets:
                    bullet.rect.y += x

    def update(self):
        self.platforms.update()
        self.clouds.update()
        self.coins.update()
        self.floaters.update()
