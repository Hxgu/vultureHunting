#! /usr/bin/python

from numpy import *
from animats.GrassEatingAnimat import GrassEating
from animats.Corpse import Corpse
from animats.Jackal import Jackal
import random
from math import *

class Env:
# constructor
	def __init__(self, mapSize):
        	self.world = zeros((mapSize,mapSize))
        	self.size = mapSize
		self.gradientMap = zeros((mapSize, mapSize))
  		self.positionArray = []
		self.jackalGradient = zeros((mapSize, mapSize))
			
	def allPositions(self):
		for a in GrassEating.ganimats:
			self.positionArray.append((a.x, a.y))
		for d in GrassEating.dyinganimats:
                        self.positionArray.append((d.x, d.y))
		for c in Corpse.allCorpses:
			self.positionArray.append((c.x, c.y))

	def tick(self):
		del self.positionArray[:]
		self.allPositions()
 
 	def validPoint(self, x, y):
		#is x,y in the map?
		return (0 <= x and 0 <= y and x < self.size and y < self.size)
	
	def validMove(self, x, y, destx, desty):
		#if not within the map it is not a valid move
		if (x < 0 or x > self.size -1 or y < 0 or y > self.size -1 or destx < 0 or destx > self.size -1 or desty < 0 or desty > self.size -1):
			return False
			
		# destination spot should be adjacent to current spot
		if (x == destx and (y == desty + 1 or y == desty - 1)) and ((destx, desty) not in self.positionArray):
			return True
		elif (y == desty and (x == destx + 1 or x == destx - 1)) and ((destx, desty) not in self.positionArray):
			return True
		return False

	def validMove2(self, x, y, destx, desty):
                #if not within the map it is not a valid move
		if (x < 0 or x > self.size -1 or y < 0 or y > self.size -1 or destx < 0 or destx > self.size -1 or desty < 0 or desty > self.size -1):
			return False

                # destination spot should be adjacent to current spot
		if (x == destx and (y == desty + 1 or y == desty - 1)):
			return True
		elif (y == desty and (x == destx + 1 or x == destx - 1)):
			return True
		return False



	def makeGradient(self, dyinganimats, allCorpses):
		#make gradient map for all dying grass eating animats
		if dyinganimats:	
			for dyingone in dyinganimats:
				x = dyingone.x
				y = dyingone.y
				#print (x,y)
				self.gradientMap[y, x] += 1000.0
				param = 50
				for j in range(1, 21):
					for i in range(1, 21):
						distance = sqrt((j*j) + (i*i))
						if distance != 0:
							if self.validPoint(y-j, x-i):
								self.gradientMap[y-j, x-i] += param/distance
							#print (i,j,x-i, y-j,50.0/distance)
							if self.validPoint(y+j, x-i):
								self.gradientMap[y+j, x-i] += param/distance
								#print (i,j,x-i, y+j,50.0/distance)
							if self.validPoint(y-j, x+i):
								self.gradientMap[y-j, x+i] += param/distance
								#print (i,j,x+i, y-j,50.0/distance)
							if self.validPoint(y+j, x+i):
								self.gradientMap[y+j, x+i] += param/distance	
								#print (i,j,x+i, y+j,50.0/distance)
				for k in range(1,21):
					if self.validPoint(y-k,x):
						self.gradientMap[y-k, x] += param/k
					if self.validPoint(y+k,x):
						self.gradientMap[y+k, x] += param/k

				for l in range(1,21):
                        	        if self.validPoint(y,x-l):
                                	        self.gradientMap[y, x-l] += param/l
                            	    	if self.validPoint(y,x+l):
                               			self.gradientMap[y, x+l] += param/l
		if allCorpses:
			for corp in allCorpses:
	                        x = corp.x
        	                y = corp.y
	                        #print (x,y)
        	                self.gradientMap[y, x] += 2000.0
                	        for j in range(1, 21):
                        	        for i in range(1, 21):
                                	        distance = sqrt((j*j) + (i*i))
    	                                	if distance != 0:
        	                                        if self.validPoint(y-j, x-i):
                                                	        self.gradientMap[y-j, x-i] += 200.0/distance
        	                                                #print (i,j,x-i, y-j,50.0/distance)
                	                                if self.validPoint(y+j, x-i):
                        	                                self.gradientMap[y+j, x-i] += 200.0/distance
                                	                        #print (i,j,x-i, y+j,50.0/distance)
                                        	        if self.validPoint(y-j, x+i):
              		                                        self.gradientMap[y-j, x+i] += 200.0/distance
                                                        #print (i,j,x+i, y-j,50.0/distance)
                                                	if self.validPoint(y+j, x+i):
                                                        	self.gradientMap[y+j, x+i] += 200.0/distance
                                                        #print (i,j,x+i, y+j,50.0/distance)
                        	for k in range(1,21):
                                	if self.validPoint(y-k,x):
                                        	self.gradientMap[y-k, x] += 200/k
                                	if self.validPoint(y+k,x):
                                        	self.gradientMap[y+k, x] += 200/k

                        	for l in range(1,21):
                                	if self.validPoint(y,x-l):
                                        	self.gradientMap[y, x-l] += 200/l
                                	if self.validPoint(y,x+l):
                                        	self.gradientMap[y, x+l] += 200/l	



	def getScents(self, x, y):
		values = []
		north = 0
		south = 0
		west = 0
		east = 0
		if self.validPoint(y-1, x):
			north = self.gradientMap[y-1, x] - self.gradientMap[y, x]
		if self.validPoint(y+1, x):
                        south = self.gradientMap[y+1, x] - self.gradientMap[y, x]
		if self.validPoint(y, x-1):
                        west = self.gradientMap[y, x-1] - self.gradientMap[y, x]
		if self.validPoint(y, x+1):
                        east = self.gradientMap[y, x+1] - self.gradientMap[y, x]
		values.append(north)
		values.append(south)
		values.append(west)
		values.append(east)
		return values


	def makeJackalGradient(self, jackals):
		if jackals:
			for jack in jackals:
				x = jack.x
				y = jack.y
                                #print (x,y)
                                self.jackalGradient[y, x] += 1000.0
                                for j in range(1, 11):
                                        for i in range(1, 11):
                                                distance = sqrt((j*j) + (i*i))
                                                if distance != 0:
                                                        if self.validPoint(y-j, x-i):
                                                                self.jackalGradient[y-j, x-i] += 50.0/distance
                                                        #print (i,j,x-i, y-j,50.0/distance)
                                                        if self.validPoint(y+j, x-i):
                                                                self.jackalGradient[y+j, x-i] += 50.0/distance
                                                                #print (i,j,x-i, y+j,50.0/distance)
                                                        if self.validPoint(y-j, x+i):
                                                                self.jackalGradient[y-j, x+i] += 50.0/distance
                                                                #print (i,j,x+i, y-j,50.0/distance)
                                                        if self.validPoint(y+j, x+i):
                                                                self.jackalGradient[y+j, x+i] += 50.0/distance
                                                                #print (i,j,x+i, y+j,50.0/distance)
                                for k in range(1,11):
                                        if self.validPoint(y-k,x):
                                                self.jackalGradient[y-k, x] += 50/k
                                        if self.validPoint(y+k,x):
                                                self.jackalGradient[y+k, x] += 50/k

                                for l in range(1,11):
                                        if self.validPoint(y,x-l):
                                                self.jackalGradient[y, x-l] += 50/l
                                        if self.validPoint(y,x+l):
                                                self.jackalGradient[y, x+l] += 50/l

	def getJackalScents(self, x, y):
                values = []
                north = 0
                south = 0
                west = 0
                east = 0
                if self.validPoint(y-1, x):
                        north = self.jackalGradient[y-1, x] - self.jackalGradient[y, x]
                if self.validPoint(y+1, x):
                        south = self.jackalGradient[y+1, x] - self.jackalGradient[y, x]
                if self.validPoint(y, x-1):
                        west = self.jackalGradient[y, x-1] - self.jackalGradient[y, x]
                if self.validPoint(y, x+1):
                        east = self.jackalGradient[y, x+1] - self.jackalGradient[y, x]
                values.append(north)
                values.append(south)
                values.append(west)
                values.append(east)
                return values
