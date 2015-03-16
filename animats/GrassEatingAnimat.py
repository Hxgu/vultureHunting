#!/usr/bin/python
import random
from Corpse import Corpse

class GrassEating:
	dyingThreshold = 15
	count = 0;
	probOfReprod = 0.02
	actions = ["north", "south", "west", "east", "copy", "stay"]
	ganimats = []
	dyinganimats = []
	def __init__(self,startX, startY, env):
	#starting variables
		self.x = startX
		self.y = startY
		self.env = env
		self.health = 70
		self.attackTillDeath = -1
	#staring flags
		self.moved = False
		self.alive = True
		self.dying = False

	#Global variable
		GrassEating.count += 1
		

	def tick(self):
		if self.health > 0:
			self.moved = False
			if self.health == 30:
				GrassEating.ganimats.remove(self)
                                GrassEating.dyinganimats.append(self)
			action = self.getAction()
			#print action
			while self.performAction(action) == False:
				action = self.getAction()
			self.health -= 1
		else:
			GrassEating.count -= 1
                        GrassEating.dyinganimats.remove(self)
                        newCorpse = Corpse(self.x, self.y, self.env)
                        Corpse.allCorpses.append(newCorpse)
		return self.alive

	
	def performAction(self, action):
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
		if action == 'stay':
			self.move(self.x, self.y)
			return True
		if action == 'copy':
			self.copy()
			return True
		return False


	def getAction(self):
		rand = random.random()
		#print rand
		if self.checkDeath() == False:
			if self.health > 30:
				if rand < 0.025:
					return 'copy'
				if rand >= 0.025 and rand < 0.2:
					return 'stay'
				if rand >= 0.2 and rand < 0.4:
					return 'north'
				if rand >= 0.4 and rand < 0.6:
                       	        	return 'south'
				if rand >= 0.6 and rand < 0.8:
                                	return 'west'
				if rand >= 0.8 and rand < 1.0:
                                	return 'east'
			else:
                        	if rand >= 0.1 and rand < 0.4:
                                	return 'stay'
                        	if rand >= 0.4 and rand < 0.55:
                                	return 'north'
                        	if rand >= 0.55 and rand < 0.7:
                                	return 'south'
                        	if rand >= 0.7 and rand < 0.85:
                               		return 'west'
                        	if rand >= 0.85 and rand < 1.0:
                                	return 'east'
			
			
	def checkDeath(self):
		if self.health <= 0:
			return True
		else:
			return False

		
	def move(self, destx, desty):
		if self.env.validMove(self.x,self.y,destx,desty):
			self.x = destx
			self.y = desty
			self.moved = True
		

	def copy(self):
		curx = self.x
		cury = self.y
		curenv = self.env
		copied = False
		seed = random.random()
		if seed < 0.25 and self.env.validMove(self.x, self.y, curx-1, cury):
			GrassEating.ganimats.append(GrassEating(curx-1, cury, curenv))
			copied = True
		if seed >= 0.25 and seed < 0.5 and self.env.validMove(self.x, self.y, curx+1, cury):
			GrassEating.ganimats.append(GrassEating(curx+1, cury, curenv))
			copied = True
		if seed >= 0.5 and seed < 0.75 and self.env.validMove(self.x, self.y, curx, cury-1):
			GrassEating.ganimats.append(GrassEating(curx, cury-1, curenv))
			copied = True
		if seed >= 0.75 and self.env.validMove(self.x, self.y, curx, cury+1):
			GrassEating.ganimats.append(GrassEating(curx, cury+1, curenv))
			copied = True
		if copied == True:
			GrassEating.count += 1
	 	
	def attacksToKill(self):
		return self.attackTillDeath
