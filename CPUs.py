__author__ = 'David'

import Constants, pygame, random, math

class floater(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, topSpeed, speed):

        super().__init__()

        #Width, Height, Color
        self.width = width
        self.height = height
        self.color = Constants.ePURPLE
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)

        #Rectange, Left, Top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Misc Qualities
        self.topSpeed = topSpeed
        self.speed = speed
        self.attackPlayer = True
        self.player = None
        self.playerHit = False
        self.xMovement = self.yMovement = 0
        self.xBouncing = self.yBouncing = 0
        self.CPUs = None
        self.walls = None
        self.shooting = False

        self.bullets = pygame.sprite.Group()
        self.counter = 0

    def followPlayer(self):

        #Horizontal Movement
        if self.player.rect.left < self.rect.left:
            if self.xMovement > -self.topSpeed:
                self.xMovement -= self.speed
        elif self.player.rect.left > self.rect.left:
            if self.xMovement < self.topSpeed:
                self.xMovement += self.speed

        #Vertical Movement
        if self.player.rect.top < self.rect.top:
            if self.yMovement > - self.topSpeed:
                self.yMovement -= self.speed
        elif self.player.rect.top > self.rect.top:
            if self.yMovement < self.topSpeed:
                self.yMovement += self.speed


    def update(self):

        self.followPlayer()

        #Bullets
        self.counter += 0.1
        if self.counter > random.randint(5, 8) and self.shooting:
            self.shootBullet()
            self.counter = 0
        for bullet in self.bullets:
            if pygame.sprite.spritecollide(bullet, self.walls, False):
                bullet.kill()

        #Horizontal Collisions
        self.rect.x += self.xMovement + self.xBouncing

        collidedBoxes = pygame.sprite.spritecollide(self, self.walls, False)
        for box in collidedBoxes:
            if box.rect.left != self.rect.left:
                if self.xMovement + self.xBouncing > 0:
                    self.rect.right = box.rect.left
                    self.xBouncing -= random.randint(3,5)
                elif self.xMovement + self.xBouncing < 0:
                    self.rect.left = box.rect.right
                    self.xBouncing += random.randint(3,5)
            #Horizontal Bounce
        if self.xBouncing > 0:
            self.xBouncing -= 0.05
        else:
            self.xBouncing += 0.05

        #Vertical Collisions
        self.rect.y += self.yMovement + self.yBouncing

        collidedBoxes = pygame.sprite.spritecollide(self, self.walls, False)
        for box in collidedBoxes:
            if box.rect.top != self.rect.top:
                if self.yMovement + self.yBouncing > 0:
                    self.rect.bottom = box.rect.top
                    self.yBouncing -= random.randint(3,5)
                elif self.yMovement + self.yBouncing < 0:
                    self.rect.top = box.rect.bottom
                    self.yBouncing += random.randint(3,5)
            #Vertical Bounce
        if self.yBouncing > 0:
            self.yBouncing -= 0.05
        else:
            self.yBouncing += 0.05


    def shootBullet(self):

        bullet = Bullet(self, self.player)
        self.bullets.add(bullet)


    def worldShift(self, x, direction):
        x = int(x)
        if direction == 'x':
            self.rect.x += x
        if direction == 'y':
            self.rect.y += x

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, player, walls):
        super().__init__()

        #Width, Height, Color
        self.width = 13
        self.height = 13
        self.color = (175, 175, 20)
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)
        self.collected = False

        #Rectangle, centerX, centerY
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.player = player
        self.walls = walls

    def changeLocation(self):
        #Change if Overlapping Platforms
        for i in self.walls:
            if self.rect.colliderect(i.rect):
                self.rect.center = (random.randint(-Constants.width * 0.22, Constants.width * 0.72), random.randint(-Constants.height * 0.22, Constants.height * 0.72))

    def playerGrabbed(self):
        #Collided With Player
        if self.rect.colliderect(self.player.rect):
            return True

class HealthBox(pygame.sprite.Sprite):
    def __init__(self, x, y, player, walls):
        super().__init__()

        #Width, Height, Color
        self.width = 50
        self.height = 50
        self.color = (150, 255, 255)
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)
        self.collected = False

        #Rectangle, centerX, centerY
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.player = player
        self.walls = walls

    def changeLocation(self):
        #Move if Overlapping Platform
        for i in self.walls:
            if self.rect.colliderect(i.rect):
                self.rect.center = (random.randint(-Constants.width * 0.22, Constants.width * 0.72), random.randint(-Constants.height * 0.22, Constants.height * 0.72))

    def playerGrabbed(self):
        #Collided With Player
        if self.rect.colliderect(self.player.rect):
            return True

class Bullet(pygame.sprite.Sprite):

    def __init__(self, floater, player):
        super().__init__()

        #center of floater and player
        self.floaterX = floater.rect.centerx
        self.floaterY = floater.rect.centery
        self.playerX = player.rect.centerx
        self.playerY = player.rect.centery

        #bullet size / image
        self.size = 8
        self.speed = 8
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(Constants.ePURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = self.floaterX
        self.rect.y = self.floaterY

    def update(self):

        #distances / norms
        distance = [self.floaterX - self.playerX, self.floaterY - self.playerY]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        vector = [direction[0] * self.speed, direction[1] * self.speed]

        #move
        self.rect.x -= vector[0]
        self.rect.y -= vector[1]

class BottomFeeder(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.width = 150
        self.height = 10
        self.color = Constants.ePURPLE
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)

        #Rectange, Left, Top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = Constants.height * 0.75 - 10

        #Various Qualities
        self.topSpeed = 30
        self.speed = 0.5
        self.player = None
        self.xMovement = 0
        self.xBouncing = 0
        self.walls = None

    def followPlayer(self):

        #Only Horizontal Movement
        if self.player.rect.bottom > self.rect.top: #If player is on Ground
            if self.player.rect.left < self.rect.left:
                if self.xMovement > -self.topSpeed:
                    self.xMovement -= self.speed

            elif self.player.rect.left > self.rect.left:
                if self.xMovement < self.topSpeed:
                    self.xMovement += self.speed

    def update(self):

        self.followPlayer()

        #Horizontal Collision
        self.rect.x += self.xMovement + self.xBouncing

        collidedBoxes = pygame.sprite.spritecollide(self, self.walls, False)
        for box in collidedBoxes:
            if box.rect.left != self.rect.left:
                if self.xMovement + self.xBouncing > 0:
                    self.rect.right = box.rect.left
                    self.xBouncing -= random.randint(3,5)
                elif self.xMovement + self.xBouncing < 0:
                    self.rect.left = box.rect.right
                    self.xBouncing += random.randint(3,5)
            #Bounce
        if self.xBouncing > 0:
            self.xBouncing -= 0.05
        else:
            self.xBouncing += 0.05

class ItsMe(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        #Width, Height, Color
        self.width = 10
        self.height = 25
        self.color = Constants.ePURPLE
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)

        #Rectange, Left, Top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Various Qualities
        self.jumpCounter = 0
        self.topSpeed = 6
        self.speed = 0.15
        self.player = None
        self.xMovement = 0
        self.sprintingX = 0
        self.verticalMovement = 0
        self.CPUs = None
        self.walls = None
        self.touching = False

    def jump(self):

        #If Touching Floor
        self.rect.y += 10
        floorsHit = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -= 10

        #If Touching Walls
        self.rect.x -= 7
        leftWallsHit = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.x += 14
        rightWallsHit = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.x -= 7

        #Start By Testing Walls, Then Floor... If touching, Jumps
        if len(leftWallsHit) > 1:
            self.verticalMovement = -9
            self.xMovement += 4
        elif len(rightWallsHit) > 1:
            self.verticalMovement = -9
            self.xMovement -= 4
        elif len(floorsHit) > 1:
            self.verticalMovement = -11

    def stopJump(self):
        #Slows Down the Vertical Movement
        if self.verticalMovement < 0:
            self.verticalMovement = self.verticalMovement / 1.1

    def followPlayer(self):
        #Horizontal Movement
        if self.player.rect.left < self.rect.left:
            if self.xMovement > -self.topSpeed:
                self.xMovement -= self.speed
                if self.touching and self.sprintingX > -5:
                    self.sprintingX -= 0.1
        elif self.player.rect.left > self.rect.left:
            if self.xMovement < self.topSpeed:
                self.xMovement += self.speed
                if self.touching and self.sprintingX < 5:
                    self.sprintingX += 0.1

        #Vertical Movement (Jumping / Stop Jumping)
        if self.player.rect.top < self.rect.top:
            self.jumpCounter += 0.5
            if self.jumpCounter > 20:
                self.jump()
                self.jumpCounter = 0
        elif self.player.rect.top > self.rect.top:
            self.stopJump()

    def gravity(self):
        #Same As Player
        if self.verticalMovement == 0:
            self.verticalMovement = 1
        else: self.verticalMovement += 0.2

    def update(self):
        self.gravity()
        self.followPlayer()

        #Horizonal Collisions
        self.rect.x += self.xMovement + self.sprintingX
        collidedBoxes = pygame.sprite.spritecollide(self, self.walls, False)
        for box in collidedBoxes:
            if box.rect.left != self.rect.left:
                if self.xMovement + self.sprintingX > 0:
                    self.rect.right = box.rect.left
                    self.sprintingX = 0
                    self.xMovement = 0
                elif self.xMovement + self.sprintingX < 0:
                    self.rect.left = box.rect.right
                    self.sprintingX = 0
                    self.xMovement = 0

        #Vertical Collisions
        self.rect.y += self.verticalMovement
        collidedBoxes = pygame.sprite.spritecollide(self, self.walls, False)
        if len(collidedBoxes) < 2:
            self.touching = False
        for box in collidedBoxes:
            if box.rect.top != self.rect.top:
                if self.verticalMovement > 0:
                    self.rect.bottom = box.rect.top
                    self.touching = True
                elif self.verticalMovement < 0:
                    self.rect.top = box.rect.bottom

                self.verticalMovement = 0 #Stops vertical momentum if hits ceiling / floor

class myHalo(pygame.sprite.Sprite):

    #Behind Player to Give the Sense of Movement / Show When Receiving Input

    def __init__(self, player):

        super().__init__()
        self.player = player
        self.width = 10
        self.height = 25
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill((200,255,255))
        self.rect = self.image.get_rect()

    def update(self):

        #Horizontal
        if self.player.leftMovement > 0:
            self.rect.right = self.player.rect.right + 1
        elif self.player.rightMovement > 0:
            self.rect.left = self.player.rect.left - 1
        else:
            self.rect.left = self.player.rect.left

        #Vertical (Only for Jumping Up)
        if self.player.verticalMovement < 0:
            self.rect.bottom = self.player.rect.bottom + 3
        else:
            self.rect.top = self.player.rect.top
