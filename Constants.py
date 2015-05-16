__author__ = 'David'
from pygame import font, init
from random import shuffle

init()

#Colors
#Now, I'm thinking c-background, d-player, e-trees, a/b-CPU
aPURPLE = (117, 108, 169) #Clouds
bPURPLE = (92, 83, 153) #BackGround
cPURPLE = (59, 48, 118) #Platforms
dPURPLE = (33, 25, 82) #Player
ePURPLE = (21, 13, 66)

#Fonts
changeFontSize = 2
tinyFont = font.SysFont(None, 16)
smallFont = font.SysFont(None, 24)
mediumFont = font.SysFont(None, 48)
largeFont = font.SysFont(None, 72)
hugeFont = font.SysFont(None, 150)
enormousFont = font.SysFont(None, 250)
changeFont = font.SysFont(None, 16)

#Window
WINDOWX = 1000
WINDOWY = 600

#Level Dimensions
width = 3000
height = 900

#Battle Room add CPUs
battleRoomChoices = ['+Tiny Floaters+', '-Tiny Floaters-',
                     '+Floaters+', '-Floaters-', '+Large Floaters+',
                     '-Large Floaters-', '+Huge Floaters+', '-Huge Floaters-',
                     '+Shooters+', '-Shooters-', '+Bottom Feeders+', '-Bottom Feeders-',
                     '+Brothers+', '-Brothers-', '+Health+'
                     ]

shuffle(battleRoomChoices)
