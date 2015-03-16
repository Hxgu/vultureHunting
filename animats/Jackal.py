#!/usr/bin/python
from numpy import zeros
import random
from Corpse import Corpse
from GrassEatingAnimat import GrassEating
from Qlearner import QLearn

class Jackal:
	count = 0;
	actions = ["north", "south", "west", "east", "eat", "attack"]
	jackals = []
	attackIn = 0
	c = 0
	
	#initialization
	def __init__(self,startX, startY, env, ID):
	#starting variables
		self.x = startX
		self.y = startY
		self.env = env
		self.ID = ID
		self.health = 100			
		
	#staring flags
		self.targetLocked = True
		self.moved = False
		self.alive = True
		self.alerted = False

	
	def tick(self):
		curState = self.getState()
		if curState == 'wander':
			action = self.wander()
			self.performQlearnedAction(action)
		else:	
			action = self.getAction(curState)
			self.performQlearnedAction(action)
			#self.health -= 1
			self.checkDeath()
		return self.alive
	

	def wander(self):
		seed = random.random()
                if seed < 0.25:
			action = 'east'
		elif seed >= 0.25 and seed < 0.5:
			action = 'west'
		elif seed >= 0.5 and seed < 0.75:
			action = 'south'
		else:
			action = 'north'
		return action

	def getAction(self, state):
		if state == 'onCorpse':
			return 'eat'
		elif state == 'onTarget':
			return 'attack'
		else:
			return state

	def checkDeath(self):
		if self.health <= 0:
			Jackal.count -= 1
			Jackal.jackals.remove(self)
			newCorpse = Corpse(self.x, self.y, self.env)
			Corpse.allCorpses.append(newCorpse)
			return True
		return False

	def performQlearnedAction(self, action):
		#if the action chosen is not feasible, it will just stay
		if action == 'north':
			self.move(self.x, self.y - 1)
			return self.moved
		if action == 'south':
			self.move(self.x, self.y + 1)
			return self.moved
		if action == 'west':
			self.move(self.x - 1, self.y)
			return self.moved
		if action == 'east':
			self.move(self.x + 1, self.y)
			return self.moved
		if action == 'eat':
			if self.findCorpse():
				self.eat(self.findCorpse())
				return True
			return False
		if action == 'attack':
			if self.findTarget():
				self.attack(self.findTarget())
				return True
			return False
		return False
	
	def move(self, destx, desty):
		if self.env.validMove2(self.x,self.y,destx,desty):
			self.x = destx
			self.y = desty
			self.moved = True

	def getState(self):
		self.env.gradientMap = zeros((self.env.size, self.env.size))
		self.env.makeGradient(GrassEating.dyinganimats, Corpse.allCorpses)
		sense = self.senseEnvironment()
		if self.env.gradientMap[self.y, self.x] >= 1000 and self.env.gradientMap[self.y, self.x] < 2000:
			return 'onTarget'
		elif self.env.gradientMap[self.y,self.x] >= 2000:
			return 'onCorpse'
		elif sense == 'noFood':
			return 'wander'
		else:
			return sense
			
	def senseEnvironment(self):
		values = self.env.getScents(self.x,self.y)
		maxValue = max(values)
		maxIndeces = [i for i, mymax in enumerate(values) if mymax == maxValue]
		if maxIndeces:
			if maxValue == 0 and len(maxIndeces) == 4:
				return 'noFood'
			else:
				maxIndex = random.choice(maxIndeces)
		if maxIndex == 0:
			state = 'north'
		if maxIndex == 1:
			state = 'south'
		if maxIndex == 2:
			state = 'west'
		if maxIndex == 3:
			state = 'east'

		return state

	def findTarget(self):
		for da in GrassEating.dyinganimats:
			if da.x == self.x and da.y == self.y:
				return da

	def findCorpse(self):
		for c in Corpse.allCorpses:
                        if c.x == self.x and c.y == self.y:
                                return c
	
	def attack(self, prey):
		print 'attacked', prey.health
		prey.health -= 15
			
				
	def eat(self, corpse):
		self.health += 10
		corpse.die()


