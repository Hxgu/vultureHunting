import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
from environment.environment import Env
from animats.VultureAnimat import Vulture
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Starting test 6, Vulture animats wandering'
mapSize = 50
env = Env(mapSize)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
a = Vulture(25,25,env,1)
Vulture.vanimats.append(a)

startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b = GrassEating(startx,starty,env)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b2 = GrassEating(startx,starty,env)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b3 = GrassEating(startx,starty,env)
GrassEating.ganimats.append(b)
GrassEating.ganimats.append(b2)
GrassEating.ganimats.append(b3)


startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
c = Corpse(startx,starty,env)
Corpse.allCorpses.append(c)

for t in range(1,10000):
	env.world = zeros((mapSize,mapSize))
	env.gradientMap = zeros((mapSize, mapSize))
        for GE in GrassEating.ganimats:
                GE.tick()
	if len(Corpse.allCorpses) > 0:
                for C in Corpse.allCorpses:
                        C.tick()
	for DG in GrassEating.dyinganimats:
                DG.tick()
        env.tick()
        env.makeGradient(GrassEating.dyinganimats, Corpse.allCorpses)
	for v in Vulture.vanimats:
                v.tick()
#	print t

del GrassEating.ganimats[:]
del Corpse.allCorpses[:]
del GrassEating.dyinganimats[:]
#while len(GrassEating.ganimats) > 0: GrassEating.ganimats.pop()
#while len(Corpse.allCorpses) > 0: Corpse.allCorpses.pop()

print "train finished"

startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b = GrassEating(startx,starty,env)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b2 = GrassEating(startx,starty,env)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
b3 = GrassEating(startx,starty,env)
GrassEating.ganimats.append(b)
GrassEating.ganimats.append(b2)
GrassEating.ganimats.append(b3)


for t in range(1,10000):
        env.world = zeros((mapSize,mapSize))
        env.gradientMap = zeros((mapSize, mapSize))
        for GE in GrassEating.ganimats:
                GE.tick()
        if len(Corpse.allCorpses) > 0:
                for C in Corpse.allCorpses:
                        C.tick()
        for DG in GrassEating.dyinganimats:
                DG.tick()
        env.tick()
	env.makeGradient(GrassEating.dyinganimats, Corpse.allCorpses)
        for v in Vulture.vanimats:
                v.tick()

print Vulture.attackIn
print Vulture.c
