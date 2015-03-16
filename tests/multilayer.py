import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
from environment.environment import Env
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Starting test 1, GE animats wandering'
mapSize = 50
env = Env(mapSize)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
a = GrassEating(startx,starty,env)
GrassEating.ganimats.append(a)
fig = plt.figure()
ims = []

for t in range(1,100):
	env.world = zeros((mapSize,mapSize))
	print 'Remaining GE animats '
	print len(GrassEating.ganimats)
	if len(Corpse.allCorpses) > 0:
		for C in Corpse.allCorpses:
			C.tick()
			env.world[C.y, C.x] = 2
	for GE in GrassEating.ganimats:
		GE.tick()
		env.world[GE.y,GE.x] = 1

	world = [[[0 for k in xrange(3)] for j in xrange(mapSize)] for i in xrange(mapSize)]
	for i in xrange(mapSize):
		for j in xrange(mapSize):
			if env.world[i,j] == 1:
				world[i][j][0] = 1
			if env.world[i,j] == 2:
				world[i][j][1] = 1
	
        # animation
	im = plt.imshow(world)
	#im.set_cmap('spectral')
	ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
repeat_delay=1000)

#ani.save('dynamic_images.mp4')
plt.show()
