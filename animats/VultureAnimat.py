#!/usr/bin/python
from numpy import zeros
import random
from Corpse import Corpse
from GrassEatingAnimat import GrassEating
from Jackal import Jackal
from Qlearner import QLearn

class Vulture:
	dyingThreshold = 15
	count = 0;
	actions = ["north", "south", "west", "east", "wait", "eat", "attack"]
	vanimats = []
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
		self.qLearn = QLearn(Vulture.actions)
		
	#staring flags
		self.targetLocked = True
		self.moved = False
		self.alive = True
		self.alerted = False

	
	def tick(self):
		#get current state
		curState = self.getState()
		#if current state is just wandering around, do random action
		if curState == 'wander':
			action = self.wander()
			self.performQlearnedAction(action)
		else:
		#if not, find Qvalue for all actions in current state
		#and choose the one with highest value	
			action = self.qLearn.chooseAction(curState)
			self.performQlearnedAction(action)
			reward = self.getReward(curState, action)
			nextState = self.getState()
			#update Q table
			self.qLearn.learn(curState, action, reward, nextState)
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

	def checkDeath(self):
		if self.health <= 0:
			Vulture.count -= 1
			Vulture.vanimats.remove(self)
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
		if action == 'wait':
			self.move(self.x, self.y)
			return True
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
		self.env.jackalGradient = zeros((self.env.size, self.env.size))
                self.env.makeJackalGradient(Jackal.jackals)
                senseJ = self.senseJackals()
		if self.env.gradientMap[self.y, self.x] >= 1000 and self.env.gradientMap[self.y, self.x] < 2000:
			if senseJ == 'noJackal':
				return 'onTarget'
			else:
				return 'onTargetJ'
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

	def senseJackals(self):
		values = self.env.getJackalScents(self.x, self.y)
		maxValue = max(values)
		maxIndeces = [i for i, mymax in enumerate(values) if mymax == maxValue]
		if maxIndeces:
			if maxValue == 0 and len(maxIndeces) == 4:
				return 'noJackals'
			else:
				return 'Jackals'
			



	def findTarget(self):
		for da in GrassEating.dyinganimats:
			if da.x == self.x and da.y == self.y:
				return da

	def findCorpse(self):
		for c in Corpse.allCorpses:
                        if c.x == self.x and c.y == self.y:
                                return c
	
	def attack(self, prey):
		if prey.health >= 0:
			Vulture.attackIn +=  prey.health
			Vulture.c += 1
		print "attacked at ", prey.health
		self.health -= 3
		prey.health -= 5
		
				
	def eat(self, corpse):
		print 'ate!'
		self.health += 10
		corpse.die()


	def getReward(self, curState, action):
		followed = 0
		attacked = 0
		ate = 0
		on_corp = 0
		on_target = 0
		LIVING_COST     = 1.0
		EATING_REWARD   = 100   # Reward for eating one food source
		ATTACK_GAIN = 10
		GRADIENT_FOLLOW_REWARD = 0.1
		STAY_ON_CORP = 1
		STAY_ON_TARGET = 1
	
		#reward for following gradient
		self.env.jackalGradient = zeros((self.env.size, self.env.size))
                self.env.makeJackalGradient(Jackal.jackals)
		senseJ = self.senseJackals()
		if action == curState:
			followed = 1
		if action == 'attack':
			if curState == 'onTarget':
				attacked = 1
			if curState == 'onTargetJ':
				attacked = 10
		if action == 'eat':
			if curState == 'onCorpse':
				ate = 1
		if action == 'wait':
			if curState == 'onCorpse':
				on_corp = 1
			elif curState == 'onTarget':
				on_target = 1
			else:
				on_corp = -1
				on_target = -1
		
		reward = (followed * GRADIENT_FOLLOW_REWARD + attacked * ATTACK_GAIN + ate * EATING_REWARD + on_corp * STAY_ON_CORP + on_target * STAY_ON_TARGET)
		return reward		
		
		#reward for eating
			



