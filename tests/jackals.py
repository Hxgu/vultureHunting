import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
from environment.environment import Env
from animats.VultureAnimat import Vulture
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
from animats.Jackal import Jackal
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
a = Jackal(25,25,env,1)
Jackal.jackals.append(a)


for i in range(1, 20):
	startx = random.randint(1,mapSize-1) - 1
	starty = random.randint(1,mapSize-1) - 1
	b = GrassEating(startx,starty,env)
	GrassEating.ganimats.append(b)


fig = plt.figure()
ims = []



for t in range(1,1000):
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
        for j in Jackal.jackals:
                j.tick()
	print t

del GrassEating.ganimats[:]
del Corpse.allCorpses[:]
del GrassEating.dyinganimats[:]
#while len(GrassEating.ganimats) > 0: GrassEating.ganimats.pop()
#while len(Corpse.allCorpses) > 0: Corpse.allCorpses.pop()


for i in range(1, 4):
        startx = random.randint(1,mapSize-1) - 1
        starty = random.randint(1,mapSize-1) - 1
        b = GrassEating(startx,starty,env)
        GrassEating.ganimats.append(b)

for t in range(1,1000):
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
	for j in Jackal.jackals:
		j.tick()

	for C in Corpse.allCorpses:
		env.world[C.y, C.x] = 2
	for GE in GrassEating.ganimats:
                env.world[GE.y,GE.x] = 1
	for DG in GrassEating.dyinganimats:
		env.world[DG.y, DG.x] = 4
	for j in Jackal.jackals:
                env.world[j.y,j.x] = 3
	
	world = [[[0 for k in xrange(3)] for j in xrange(mapSize)] for i in xrange(mapSize)]
	for i in xrange(mapSize):
		for j in xrange(mapSize):
			if env.world[i,j] == 1:
				world[i][j][0] = 1
			if env.world[i,j] == 2:
				world[i][j][1] = 1
			if env.world[i,j] == 3:
				world[i][j][2] = 1
			if env.world[i,j] == 4:
				world[i][j][0] = 1
				world[i][j][1] = 1
        # animation
	im = plt.imshow(world)
	
	ims.append([im])
	ims.append([im])
#	print t

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)

plt.show()
