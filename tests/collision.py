import sys
sys.path.append("..")
from environment.environment import Env
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
import numpy as np
from numpy import zeros
import random

print 'Starting test 4, make sure no collision'
mapSize = 5
env = Env(mapSize)
startx = random.randint(1,mapSize-1) - 1
starty = random.randint(1,mapSize-1) - 1
a = GrassEating(0,1,env)
b = GrassEating(0,2,env)
c = Corpse(1,1,env)

GrassEating.ganimats.append(a)
GrassEating.ganimats.append(b)
Corpse.allCorpses.append(c)
env.tick()
a.performAction('south')
a.performAction('east')

