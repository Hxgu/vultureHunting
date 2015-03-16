#!/usr/bin/env python
"""
An animated image
"""

import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
from environment.environment import Env
from animats.GrassEatingAnimat import GrassEating
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
GE = GrassEating(startx,starty,env)
fig = plt.figure()
ims = []

for t in range(1,200):
        #time.sleep(.05)
        #print 'Time: '+str(t)

       GE.tick()
        # Update the evironment's map with animat's new location
       env.world = zeros((mapSize,mapSize));
       env.world[GE.y,GE.x] = 1
#        print env.worldi
        # animation
       im = plt.imshow(env.world)
       ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
    repeat_delay=1000)

#ani.save('dynamic_images.mp4')


plt.show()
