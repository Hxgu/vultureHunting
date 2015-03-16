#!/usr/bin/python

import random

class QLearn:

#possible states
#1. sense dying grass eating animat gradient north
#2. sense dying grass eating animat gradient south
#3. sense dying grass eating animat gradient west
#4. sense dying grass eating animat gradient east
#5. wander around
#6. standing on top of a dead corpse
#7. standing on top of a dying animat (ready to attack or wait)

#possible actions
#1. move north
#2. move south
#3. move west
#4. move east
#5. wait and do nothing
#6. eat
#7. attack

#total number of states is 8
#total number of actions is 7

	def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
		self.qtable = {}
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		self.actions = actions

	def getQ(self, state, action):
		return self.qtable.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

	def learnQ(self, state, action, reward, value):
		oldv = self.qtable.get((state, action), None)
		if oldv is None:
			self.qtable[(state, action)] = reward
		else:
			self.qtable[(state, action)] = oldv + self.alpha * (value - oldv)

	def chooseAction(self, state, return_q=False):
		#find all possible actions in current state
		q = [self.getQ(state, a) for a in self.actions]
		maxQ = max(q)
		#exploring
		if random.random() < self.epsilon:
			action = random.choice(self.actions)
			return action
		#if more than one action has highest Qvalue, choose randomly from
		#the highest
		count = q.count(maxQ)
		if count > 1:
			best = [i for i in range(len(self.actions)) if q[i] == maxQ]
			i = random.choice(best)
		else:
			i = q.index(maxQ)
		#return the action
		action = self.actions[i]

		if return_q:
			return action, q
		return action

	def learn(self, state1, action1, reward, state2):
		maxqnew = max([self.getQ(state2, a) for a in self.actions])
		self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)
