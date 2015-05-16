__author__ = 'David'

import Constants, Stages
from pygame import font

def drawText(text, font, surface, x, y, center):

    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()

    if center:
        textrect.center = (x,y)
    else:
        textrect.topleft = (x,y)

    surface.blit(textobj, textrect)

class TextOnScreen(object):

    def __init__(self, player, CPUs, coins, surface, level):

        #Incoming information to process
        self.player = player
        self.coins = coins
        self.CPUs = CPUs
        self.surface = surface
        self.fontSize = 12 # Used to make "Battle Room" text zoom
        self.level = level
        self.helpResetCredits = None

        #Time
        self.counter = 0
        self.timer = 50
        self.onBoxCounter = 0


        #Positions
        self.healthPos = [10,10]
        self.stagePos = [Constants.width * 0.22, Constants.height * 0.3]
        self.readySetGoPos = [Constants.width * 0.22, Constants.height * 0.5]

        #Titles
        self.title = 'WRECKTANGLES'
        self.newtitle = '' #Add each letter from title
        self.titleLine2 = ['of   ','  the']
        self.newTitleLine2 = '' #Add each letter from Title

    def updateFront(self):
        if self.player.stage != 0:
            drawText('Player Health: %s' % self.player.health, Constants.smallFont, self.surface, self.healthPos[0] - 2, self.healthPos[1] - 5, False)
            drawText('Press P to Pause', Constants.smallFont, self.surface, self.healthPos[0] - 2, self.healthPos[1] + 12, False)

    def updateBack(self):
        #Either in Platform Plane, or in between Platforms and Clouds

        self.readySetGo()

        #Player Is Dead
        if self.player.health < 1:
            self.playerDead()

        #Main Screen / Choose Level
        elif self.player.stage == 0:

            #Numbers 1 - 10
            for i in range(10):
                drawText('%s' % str(int(i)+1), Constants.largeFont, self.surface, self.level.left + i * 300 + 140, self.level.bottom - (80 * (i+1) + 50), False)

            #Help / Reset / Credits Boxes
            drawText('Help', Constants.mediumFont, self.surface, self.level.right - 185, self.level.bottom - 110, False)
            drawText('Reset', Constants.mediumFont, self.surface, self.level.right - 395, self.level.bottom - 180, False)
            drawText('Credits', Constants.mediumFont, self.surface, self.level.right - 610, self.level.bottom - 250, False)

            #Above the player's head as he stands on box
            onBox = []
            for i in range(self.player.stagesUnlocked): #Stages Boxes
                if self.player.rect.bottom == self.player.level.bottom - 80 * (i+1):
                    self.onBoxCounter += 1
                    onBox.append(i)
                    if self.onBoxCounter > 4:
                        drawText('%s' % Stages.whichStage[int(i+1)]['text'], Constants.smallFont, self.surface, self.level.left + i * 300 + 150, self.level.bottom - (80 * (i+1) + 82), True)
                        drawText('Press ENTER to Load', Constants.smallFont, self.surface, self.level.left + i * 300 + 65, self.level.bottom - (80 * (i+1) - 15), False)
                        drawText('High Score: %s' % self.player.highScores[int(i+1)], Constants.smallFont, self.surface, self.level.left + i * 300 + 105, self.level.bottom - (80 * (i+1) + 70), False)

            for i in range(3): #Help / Reset / Credits Boxes
                if self.player.rect.bottom == self.player.level.bottom - 70 * (i+1):
                    self.onBoxCounter += 1
                    onBox.append(i)
                    if self.onBoxCounter > 4:
                        drawText('Press ENTER', Constants.smallFont, self.surface, self.level.right - (i * 200 + 200), self.level.bottom - (70 * (i+1) - 15), False)
                        if self.player.rect.bottom == self.player.level.bottom - 70 * (2):
                            drawText('(ALL highscores = zero ... Stages re-locked)', Constants.tinyFont, self.surface, self.level.right - (450), self.level.bottom - (70 * (2) - 30), False)





            if self.player.stagesUnlocked == 11:
                drawText('^^ Look Up ^^', Constants.tinyFont, self.surface, self.level.left + 20, self.level.bottom - 20, False)


                if self.player.rect.bottom == self.player.level.top + 40:
                    self.onBoxCounter += 1
                    onBox.append('i')
                    if self.onBoxCounter > 30:
                        drawText('Press ENTER to Load', Constants.smallFont, self.surface, self.level.left + 67, self.level.top + 55, False)
                        drawText('the Battle Room', Constants.mediumFont, self.surface, self.level.left + 30, self.level.top + 70, False)


            #Only show text if standing on box for some time
            if not onBox:
                self.onBoxCounter = 0

            #Dramatic Opening Title
            if self.helpResetCredits == None:
                if self.counter > 10:
                    drawText('Wrath', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 125, True)
                if self.counter == 30:
                    self.newTitleLine2 += self.titleLine2[0]
                if self.counter == 40:
                    self.newTitleLine2 += self.titleLine2[1]
                if 134 > self.counter > 49 and self.counter % 7 == 0:
                    self.newtitle += self.title[int((self.counter - 49) / 7) - 1]

                drawText(self.newTitleLine2, Constants.largeFont, self.surface, self.readySetGoPos[0] - 100, self.readySetGoPos[1] - 75, False)
                drawText(self.newtitle, Constants.enormousFont, self.surface, self.readySetGoPos[0] - 700, self.readySetGoPos[1] - 20, False)

            #If Help / Reset / Credits
            elif self.helpResetCredits == 'help':
                drawText('It really is pretty self-explanatory...', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 150, True)
                drawText('Use the ARROW keys to move and SPACEBAR to jump.', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 120, True)
                drawText('(If you\'re reading this, you already knew that)', Constants.tinyFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 105, True)
                drawText('<< Look Over There <<', Constants.mediumFont, self.surface, self.level.right - (450), self.level.bottom - (70 * (4)), False)
                drawText('You need at least 5 coins to pass a stage.', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 90, True)
                drawText('Press ESCAPE at any time to quit.', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 60, True)
                drawText('(Highscores / Unlocked Stages will not save)', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 40, True)
                drawText('Press F to toggle FULLSCREEN mode.', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1], True)
            elif self.helpResetCredits == 'reset':
                drawText('RESET!', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 50, True)
            elif self.helpResetCredits == 'credits':
                drawText('created by:', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 200, True)
                drawText('David  Wolgemuth', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 125, True)
                drawText('thank  you  for  playing', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1], True)
                drawText('<< Look Over There <<', Constants.mediumFont, self.surface, self.level.right - (450), self.level.bottom - (70 * (4)), False)

        #The Battle Room (Stage 11)
        elif self.player.stage == 11:

            #Welcome to the Battle Room!
            if 40 > self.counter > 20:
                drawText('Welcome', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 25, True)
            elif 50 > self.counter > 45:
                drawText('to', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 25, True)
            elif 55 > self.counter > 50:
                drawText('the', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 25, True)
            elif self.counter > 70:
                drawText('Battle Room', font.SysFont(None, int(self.fontSize)), self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 20, True)
                if self.fontSize < 250: #Zoom Text
                    self.fontSize *= 1.1

            #Player Standing On a Box
            onBox = []
            for i in range(15):
                if self.player.rect.bottom == self.level.bottom - 50 * (i+1):
                    self.onBoxCounter += 1
                    if self.onBoxCounter > 4:
                        drawText('%s' % Constants.battleRoomChoices[i], Constants.smallFont, self.surface, self.player.rect.centerx, self.player.rect.top - 10, True)
                    onBox.append(i)

            #Only show text if standing on box for some time
            if not onBox:
                self.onBoxCounter = 0


        #Regular Stages During Game Play
        elif self.player.health > 0 and self.timer > 1 and len(self.coins) > 0 and not self.player.paused:
            drawText('High Score: %s' % self.player.highScores[self.player.stage], Constants.smallFont, self.surface, self.stagePos[0], self.stagePos[1] - 160, True)
            #drawText('Score: %s' % self.player.score, Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 110, True)
            #drawText('Stage: %s' % self.player.stage, Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1], True)
            drawText('%s' % int(self.timer), Constants.largeFont, self.surface, self.stagePos[0], self.stagePos[1] + 20, True)
            drawText('%s' % self.level.currentStage['text'], Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] + 90, True)
            #if len(self.coins) > 5:
            drawText('Coins Left: %s' % len(self.coins), Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 80, True)
            if len(self.coins) < 6:
                drawText('Stage Cleared! Stay Alive!', Constants.smallFont, self.surface, self.stagePos[0], self.stagePos[1] - 40, True)
                #drawText('Coins Left: %s' % len(self.coins), Constants.smallFont, self.surface, self.stagePos[0], self.stagePos[1] - 40, True)

        #Out of Time / Stage Complete
        elif self.timer < 1:
            if len(self.coins) <= 5:
                if self.player.score > self.player.highScores[self.player.stage]:
                    drawText('High Score: %s' % int(self.player.score), Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 40, True)
                else:
                    drawText('High Score: %s' % self.player.highScores[self.player.stage], Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 20, True)
                drawText('Score: %s' % self.player.score, Constants.largeFont, self.surface, self.stagePos[0], self.stagePos[1] + 25, True)
                drawText('Level Complete!', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 50, True)
                drawText('Press ENTER to Continue', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 40, True)
            else:
                drawText('High Score: %s' % self.player.highScores[self.player.stage], Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 20, True)
                drawText('Score: %s' % self.player.score, Constants.largeFont, self.surface, self.stagePos[0], self.stagePos[1] + 35, True)
                drawText('Not Enough Coins', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 50, True)
                drawText('Press ENTER to Try Again', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 50, True)

        #All Coins Bonus
        elif len(self.coins) < 1:
            if self.player.score + int(self.timer) > self.player.highScores[self.player.stage]:
                drawText('High Score: %s' % int(self.player.score + int(self.timer)), Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 40, True)
            else:
                drawText('High Score: %s' % self.player.highScores[self.player.stage], Constants.mediumFont, self.surface, self.stagePos[0], self.stagePos[1] - 40, True)
            drawText('Score: %s ' % int(self.player.score + int(self.timer)), Constants.largeFont, self.surface, self.stagePos[0], self.stagePos[1] + 10, True)
            drawText('Level Complete!', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 70, True)
            drawText('All Coins Bonus!', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 20, True)
            drawText('Press ENTER to Continue', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 70, True)

        #Paused
        elif self.player.paused:
            drawText('PAUSED', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] - 50, True)
            drawText('Press "P" to Continue', Constants.mediumFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 40, True)
            drawText('Press ENTER to Return To Menu', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + 80, True)




    def readySetGo(self):
        #Only for Game Stages
        if self.player.stage != 0 and self.player.stage != 11:
            if 10 < self.counter < 30:
                drawText('Ready', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1], True)
            elif 31 < self.counter < 50:
                drawText('Set', Constants.largeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1], True)
            elif 51 < self.counter < 100:
                drawText('GO!', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1], True)

    def playerDead(self):
        for i in range(6):
            #Player is Dead
            drawText('Player Dead', Constants.hugeFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + ((i - 1) * 300), True)
            drawText('Player Dead', Constants.hugeFont, self.surface, self.readySetGoPos[0] - 700, self.readySetGoPos[1] + ((i - 1) * 300), True)
            drawText('Player Dead', Constants.hugeFont, self.surface, self.readySetGoPos[0] + 700, self.readySetGoPos[1] + ((i - 1) * 300), True)
            #Press Enter to Continue
            drawText('press ENTER to continue', Constants.smallFont, self.surface, self.readySetGoPos[0], self.readySetGoPos[1] + ((i - 1) * 300) + 100, True)
            drawText('press ENTER to continue', Constants.smallFont, self.surface, self.readySetGoPos[0] - 700, self.readySetGoPos[1] + ((i - 1) * 300) + 100, True)
            drawText('press ENTER to continue', Constants.smallFont, self.surface, self.readySetGoPos[0] + 700, self.readySetGoPos[1] + ((i - 1) * 300) + 100, True)


    def textWorldShift(self, x, direction):
        #Only StagePos / ReadySetGoPos (In between Clouds and Platforms) -- (Other Text is in Same plain as Player/Platforms or in the GUI plane)
        x = int(x)
        if direction == 'x':
            self.stagePos[0] += x/1.5
            self.readySetGoPos[0] += x / 1.5

        if direction == 'y':
            self.stagePos[1] += x/1.5
            self.readySetGoPos[1] += x / 1.5
