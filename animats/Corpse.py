#!/usr/bin/python
import random

class Corpse:
	count = 0
	allCorpses = []
	
	def __init__(self, startX, startY, env):
		self.x = startX
		self.y = startY
		self.env = env
		self.life = 15

	def tick(self):
		if self.life > 0:
			self.life -= 1
		else:
			Corpse.allCorpses.remove(self)
		return self.life

	def die(self):
		self.life = 0
