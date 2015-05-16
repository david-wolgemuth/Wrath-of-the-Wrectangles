__author__ = 'David'

import pygame, Player, Constants, Level, CPUs, TextOnScreen
from pygame import *
from Constants import *
from random import randint
import shelve
import pickle

#Open Scores File (Pickle)
scores_file = open('scores_file', 'rb')
highScores = pickle.load(scores_file)
scores_file.close()

screen = pygame.display.set_mode((400,100))

#Because FULLSCREEN IS BEING A BITCH!
screen.fill((0,0,0))
TextOnScreen.drawText('Press any key to start', Constants.mediumFont, screen, 200, 50, True)
pygame.display.flip()
def Wait():
    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                return
Wait()

def main():

    pygame.init()
    screen = pygame.display.set_mode((WINDOWX,WINDOWY), FULLSCREEN)
    pygame.display.set_caption('Wrath of the Wrecktangles')
    pygame.mouse.set_visible(False)


    clock = pygame.time.Clock()
    stageCounter =  0
    score = 0

    #Load Stages (Shelve)
    d = shelve.open('score.txt')
    stagesUnlocked = d['stagesUnlocked']

    running = True
    while running:

        #Set Up Groups
        backgroundSprites = pygame.sprite.Group()
        foregroundSprites = pygame.sprite.Group()
        playerSprite = pygame.sprite.Group()
        haloSprite = pygame.sprite.Group()
        coinsSprite = pygame.sprite.Group()
        healthBoxes = pygame.sprite.Group()

        #Battle Room Groups
        tinyFloaters = pygame.sprite.Group()
        normalFloaters = pygame.sprite.Group()
        largeFloaters = pygame.sprite.Group()
        hugeFloaters = pygame.sprite.Group()
        shooters = pygame.sprite.Group()
        bottomFeeders = pygame.sprite.Group()
        brothers = pygame.sprite.Group()

        def worldShiftBattleRoom(x, direction):
            if direction == 'x':
                for floater in normalFloaters:
                    floater.rect.x += x
                for floater in largeFloaters:
                    floater.rect.x += x
                for floater in hugeFloaters:
                    floater.rect.x += x
                for floater in shooters:
                    floater.rect.x += x
                    for bullet in floater.bullets:
                        bullet.rect.x += x
                for floater in bottomFeeders:
                    floater.rect.x += x

            if direction == 'y':
                for floater in normalFloaters:
                    floater.rect.y += x
                for floater in largeFloaters:
                    floater.rect.y += x
                for floater in hugeFloaters:
                    floater.rect.y += x
                for floater in shooters:
                    floater.rect.y += x
                    for bullet in floater.bullets:
                        bullet.rect.y += x
                for floater in bottomFeeders:
                    floater.rect.y += x


        #player and level
        player = Player.Players(350,40)
        player.stage = stageCounter
        if player.stagesUnlocked > stagesUnlocked:
            stagesUnlocked = player.stagesUnlocked
        else:
            player.stagesUnlocked = stagesUnlocked
        player.score = score
        player.highScores = highScores
        player.CPUs.empty()
        player.itsMe.empty()
        player.bottomFeeders.empty()
        player.targetedCPUs.empty()
        thisLevel = Level.Level_One(player)
        player.level = thisLevel
        player.rect.center = (Constants.width * 0.25, Constants.height * 0.73)

        #add all to groups
        foregroundSprites.add(thisLevel.platforms)
        backgroundSprites.add(thisLevel.clouds)
        playerSprite.add(player)

        #add CPUS to Player and ForeGround
        foregroundSprites.add(thisLevel.floaters)
        player.targetedCPUs.add(thisLevel.targetingFloaters)
        player.CPUs.add(thisLevel.floaters)
        player.bottomFeeders.add(thisLevel.bottomFeeders)
        player.itsMe.add(thisLevel.itsMe)
        for i in range(len(thisLevel.coins)):
            thisLevel.coins[i].changeLocation()
            foregroundSprites.add(thisLevel.coins[i])
            coinsSprite.add(thisLevel.coins[i])
        for i in range(len(thisLevel.healthBoxes)):
            thisLevel.healthBoxes[i].changeLocation()
            foregroundSprites.add(thisLevel.healthBoxes[i])
            healthBoxes.add(thisLevel.healthBoxes[i])
        for i in range(1):
            halo = CPUs.myHalo(player)
            haloSprite.add(halo)

        #text
        displayText = TextOnScreen.TextOnScreen(player, thisLevel.floaters, coinsSprite, screen, thisLevel)

        #Set All Values Back to Normal
        counter = 0
        player.health = 5
        playerAlive = True
        timeLeft = True
        coinsLeft = True
        paused = False
        levelChosen = False
        HealthGet = False
        Fullscreen = True

        #Main Game Loop
        while playerAlive and timeLeft and coinsLeft and not levelChosen:

            #Quit
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    running = playerAlive = False

                #KeyDown
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        player.goLeft()
                        player.leftKey = True
                    if event.key == K_RIGHT:
                        player.goRight()
                        player.rightKey = True
                    if event.key == K_SPACE:
                        player.jump()

                #KeyUp
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        player.stopLeft()
                        player.leftKey = False
                    if event.key == K_RIGHT:
                        player.stopRight()
                        player.rightKey = False
                    if event.key == K_SPACE:
                        player.stopJump()
                    if event.key == K_p:
                        paused = not paused
                        player.paused = paused

                    #FullScreen
                    if event.key == K_f:
                        if Fullscreen:
                            screen = pygame.display.set_mode((WINDOWX,WINDOWY))
                            Fullscreen = False
                        else:
                            screen = pygame.display.set_mode((WINDOWX,WINDOWY), FULLSCREEN)
                            Fullscreen = True

                    #Return Key
                    if event.key == K_RETURN:

                        if paused: #Return Back to Stage Select / Main Menu
                            stageCounter = 0
                            levelChosen = True
                            continue

                        elif stageCounter != 0 and stageCounter != 11:
                            if player.health < 1: #Player Dead
                                playerAlive = False
                            elif displayText.timer < 1: #Out of Time
                                timeLeft = False
                            elif len(coinsSprite) < 1: #Out of Coins
                                coinsLeft = False

                        elif stageCounter == 0:
                            stageCounter = player.chooseLevel() #Determines if the Player is standing on a Stage Select Box
                            if stageCounter != 0:
                                levelChosen = True
                                continue

                            displayText.helpResetCredits = player.chooseLevelText() #Determines if Player is on a Help / Reset / Credits box
                            if displayText.helpResetCredits == 'reset': #Reset All of the Information
                                levelChosen = True
                                player.stagesUnlocked = stagesUnlocked = d['stagesUnlocked'] = 1
                                for i in player.highScores:
                                    player.highScores[i] = 0

                        elif stageCounter == 11:
                            if player.health < 1: #Player Dead
                                playerAlive = False
                            addCPU = player.chooseCPUs()
                            if addCPU == '+Tiny Floaters+':
                                i = CPUs.floater(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom), 5, 5, 3.5, 0.2)
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.level.platforms.add(i)
                                tinyFloaters.add(i)
                            if addCPU == '-Tiny Floaters-':
                                chosenOne = None
                                for i in tinyFloaters:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Floaters+':
                                i = CPUs.floater(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom), 15, 15, 4, 0.2)
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.CPUs.add(i)
                                normalFloaters.add(i)
                            if addCPU == '-Floaters-':
                                chosenOne = None
                                for i in normalFloaters:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Large Floaters+':
                                i = CPUs.floater(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom), 30, 30, 2.5, 0.12)
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.CPUs.add(i)
                                largeFloaters.add(i)
                            if addCPU == '-Large Floaters-':
                                chosenOne = None
                                for i in largeFloaters:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Huge Floaters+':
                                i = CPUs.floater(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom), 60, 60, 1.0, 0.1)
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.CPUs.add(i)
                                hugeFloaters.add(i)
                            if addCPU == '-Huge Floaters-':
                                chosenOne = None
                                for i in hugeFloaters:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Bottom Feeders+':
                                i = CPUs.BottomFeeder(randint(thisLevel.left, thisLevel.right))
                                i.rect.bottom = thisLevel.bottom
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.bottomFeeders.add(i)
                                bottomFeeders.add(i)
                            if addCPU == '-Bottom Feeders-':
                                chosenOne = None
                                for i in bottomFeeders:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Brothers+':
                                i = CPUs.ItsMe(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom))
                                i.player = player
                                thisLevel.platforms.add(i)
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.itsMe.add(i)
                                brothers.add(i)
                            if addCPU == '-Brothers-':
                                chosenOne = None
                                for i in brothers:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Shooters+' or (event.type == KEYUP and event.key == K_s):
                                i = CPUs.floater(randint(thisLevel.left, thisLevel.right),randint(thisLevel.top, thisLevel.bottom), 5, 5, 3.5, 0.2)
                                i.player = player
                                i.walls = thisLevel.platforms
                                foregroundSprites.add(i)
                                player.targetedCPUs.add(i)
                                player.CPUs.add(i)
                                shooters.add(i)
                            if addCPU == '-Shooters-':
                                chosenOne = None
                                for i in shooters:
                                    chosenOne = i
                                if chosenOne:
                                    chosenOne.kill()
                            if addCPU == '+Health+':
                                HealthGet = True






            #WorldShift
            if player.rect.x >= WINDOWX - 300: #Right Side of Screen
                x = player.rect.x - (WINDOWX - 300)
                player.rect.x = WINDOWX - 300
                thisLevel.worldShift(-x, 'x')
                displayText.textWorldShift(-x, 'x')
                worldShiftBattleRoom(-x, 'x')

            if player.rect.x <= 300: #Left Side of Screen
                x = 300 - player.rect.x
                player.rect.x = 300
                thisLevel.worldShift(x, 'x')
                displayText.textWorldShift(x, 'x')
                worldShiftBattleRoom(x, 'x')

            if player.rect.y >= WINDOWY - 150: #Bottom of Screen
                y = player.rect.y - (WINDOWY - 150)
                player.rect.y = WINDOWY - 150
                thisLevel.worldShift(-y, 'y')
                displayText.textWorldShift(-y, 'y')
                worldShiftBattleRoom(-y, 'y')

            if player.rect.y <= 150: #Top of Screen
                y = 150 - player.rect.y
                player.rect.y = 150
                thisLevel.worldShift(y, 'y')
                displayText.textWorldShift(y, 'y')
                worldShiftBattleRoom(y, 'y')


            #Add Bullets
            for floater in thisLevel.floaters:
                foregroundSprites.add(floater.bullets)
            for shooter in shooters:
                foregroundSprites.add(shooter.bullets)

            #Health / Coins
            currentHealth = player.health
            numHealth = len(healthBoxes)
            numCoins = len(coinsSprite)
            displayText.counter += 0.25
            counter += 0.25

            #If Player is Alive, Player Can Move
            if player.health > 0 and not paused:
                playerSprite.update()

                #Is Player Outside the Box??
                if player.rect.centerx < thisLevel.left or\
                            player.rect.centerx > thisLevel.right or\
                                player.rect.centery < thisLevel.top or\
                                player.rect.centery > thisLevel.bottom:
                    if counter % 5 == 0:
                        player.health -= 1

            #If Time and Coins Left, and Not Paused, (Or if Player is Dead) Everything Else Can Move
            if (counter > 50 and displayText.timer > 1 and len(coinsSprite) > 0 and not paused) or player.health < 1 or stageCounter == 11:
                displayText.timer -= 0.02
                backgroundSprites.update()
                foregroundSprites.update()
                for i in range(len(thisLevel.coins)):
                    if thisLevel.coins[i].playerGrabbed():
                        thisLevel.coins[i].kill()

                for i in range(len(thisLevel.healthBoxes)):
                    if thisLevel.healthBoxes[i].playerGrabbed():
                        thisLevel.healthBoxes[i].kill()

            #Player Halo
            haloSprite.update()

            #Draw To Screen
            screen.fill(bPURPLE)
            backgroundSprites.draw(screen)
            displayText.updateBack()
            foregroundSprites.draw(screen)
            haloSprite.draw(screen)
            playerSprite.draw(screen)
            displayText.updateFront()
            player.newShowLines(screen)

            #Flashes Display on Screen
            if player.health != currentHealth: #Flash White if Player Hurt
                screen.fill((255,255,255))
            if numHealth != len(healthBoxes) or HealthGet: #Flash Turquoise if Health Box, and Give Player Health
                screen.fill((0,255,255))
                player.health += 3
                if player.health > 5:
                    player.health = 5
                HealthGet = False
            if numCoins != len(coinsSprite): #Flash Yellow if Coin, Give Player a Point
                screen.fill((175, 175, 20))
                score += 1
                player.score += 1

            pygame.display.flip()

        #Score Reset To Zero When Player Goes to Main Menu
        if stageCounter == 0:
            score = 0

        #Player Died, Back to Main Menu
        elif not playerAlive:
            stageCounter = 0
            score = 0

        #All Coins, Display Scores, Send On to Next Level
        elif not coinsLeft:
            player.score += int(displayText.timer)
            if player.score > player.highScores[stageCounter]:
                player.highScores[stageCounter] = player.score
            stageCounter += 1
            if stageCounter > stagesUnlocked:
                stagesUnlocked = stageCounter

        #No Time Left
        elif not timeLeft:
            if len(coinsSprite) > 5: #Player Didn't Get Enough Coins, Back to Menu
                score = 0
            else:
                if player.score > player.highScores[stageCounter]: #Player Sent One to Next Level
                    player.highScores[stageCounter] = player.score
                player.score = 0
                stageCounter += 1
                if stageCounter > stagesUnlocked:
                    stagesUnlocked = stageCounter

        score = 0

    #Save Stages and High Scores
    d['stagesUnlocked'] = stagesUnlocked
    d.close()
    scores_file = open('scores_file', 'wb')
    pickle._dump(player.highScores, scores_file)
    scores_file.close()

#Run Main
if __name__ == '__main__':
    main()