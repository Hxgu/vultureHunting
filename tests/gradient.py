import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
from environment.environment import Env
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
import numpy as np
from numpy import zeros
import random

print 'Starting test 1, GE animats wandering'
mapSize = 5
env = Env(mapSize)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
a = GrassEating(startx,starty,env)
GrassEating.ganimats.append(a)

for t in range(1,100):
	env.world = zeros((mapSize,mapSize))
	env.gradientMap = zeros((mapSize, mapSize))
	env.tick()
#	if len(Corpse.allCorpses) > 0:
#		for C in Corpse.allCorpses:
#			C.tick()
#			env.world[C.y, C.x] = 2
	for GE in GrassEating.ganimats:
		GE.tick()
		env.world[GE.y, GE.x] = 1
	print 'make gradient'
#	print GrassEating.dyinganimats
	env.makeGradient(GrassEating.dyinganimats)	
	
print env.gradientMap

