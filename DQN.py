from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
import collections
from operator import add

prev_x = 0
prev_y = 0

class DQNAgent(object):
	def __init__(self, params):
		global x_prev, y_prev
		x_prev = 0
		y_prev = 0
		self.reward = 0
		self.gamma = 0.9
		self.dataframe = pd.DataFrame()
		self.short_memory = np.array([])
		self.agent_target = 1
		self.agent_predict = 0
		self.learning_rate = params['learning_rate']        
		self.epsilon = 1
		self.actual = []
		self.layer1 = params['layer1']
		self.layer2 = params['layer2']
		self.layer3 = params['layer3']
		self.memory = collections.deque(maxlen=params['memory_size'])
		self.weights = params['weights_path']
		self.load_weights = params['load_weights']
		self.model = self.network()

	def network(self):
		model = Sequential()
		model.add(Dense(output_dim=self.layer1, activation='relu', input_dim=20))
		model.add(Dropout(0.2))
		model.add(Dense(output_dim=self.layer2, activation='relu'))
		model.add(Dropout(0.2))
		model.add(Dense(output_dim=self.layer3, activation='relu'))
		model.add(Dropout(0.2))
		model.add(Dense(output_dim=3, activation='relu'))
		opt = Adam(self.learning_rate)
		model.summary()
		model.compile(loss='mse', optimizer=opt)

		if self.load_weights:
			model.load_weights(self.weights)
		return model
	
	def get_state(self, game, player, food, params):
		state = [
			player.head_distance1 == (params['block_size']), #Danger Immediate Straight
			player.head_distance2 == (params['block_size']), #Danger Immediate Right
			player.head_distance3 == (params['block_size']), #Danger Immediate Left
			
	
			player.head_distance1 == (2 * params['block_size']), #Danger 2 Blocks Straight
			player.head_distance2 == (2 * params['block_size']), #Danger 2 Blocks Right
			player.head_distance3 == (2 * params['block_size']), #Danger 2 Blocks Left
			
			player.head_distance1 == (3 * params['block_size']), #Danger 3 Blocks Straight
			player.head_distance2 == (3 * params['block_size']), #Danger 3 Blocks Right
			player.head_distance3 == (3 * params['block_size']), #Danger 3 Blocks Left
			
			player.head_distance1 == (4 * params['block_size']), #Danger 4 Blocks Straight
			player.head_distance2 == (4 * params['block_size']), #Danger 4 Blocks Right
			player.head_distance3 == (4 * params['block_size']), #Danger 4 Blocks Left
			
			player.x_change == -params['block_size'],  # move left
			player.x_change == params['block_size'],  # move right
			player.y_change == -params['block_size'],  # move up
			player.y_change == params['block_size'],  # move down
			
			food.x_food < player.x,  # food left
			food.x_food > player.x,  # food right
			food.y_food < player.y,  # food up
			food.y_food > player.y  # food down
			]
			
		for i in range(len(state)):
			if state[i]:
				state[i]=1
			else:
				state[i]=0

		return np.asarray(state)

	def set_reward(self, player, crash, food, counter_games, action):
		self.reward = 0
		global x_prev, y_prev
        
		if crash:
			self.reward = -150
			return self.reward

		if player.eaten:
			self.reward = 15

		else:
			if action[1] == 1:
				self.reward -= 10/(abs(food.food_prev_x - food.x_food) + abs(food.food_prev_y - food.y_food))
	            
			elif action[2] == 1:
				self.reward -= 10/(abs(food.food_prev_x - food.x_food) + abs(food.food_prev_y - food.y_food))
	            
			if abs(x_prev - food.x_food) > abs(player.x - food.x_food) or abs(y_prev - food.y_food) > abs(player.y - food.y_food):
				self.reward += 100/(abs(food.food_prev_x - food.x_food) + abs(food.food_prev_y - food.y_food)) 
				
			elif abs(x_prev - food.x_food) < abs(player.x - food.x_food) or abs(y_prev - food.y_food) < abs(player.y - food.y_food):
				self.reward -= 100/(abs(food.food_prev_x - food.x_food) + abs(food.food_prev_y - food.y_food))

		
		x_prev = player.x
		y_prev = player.y            
		
		return self.reward

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	def replay_new(self, memory, batch_size):
		if len(memory) > batch_size:
			minibatch = random.sample(memory, batch_size)
		else:
			minibatch = memory
		for state, action, reward, next_state, done in minibatch:
			target = reward
			if not done:
				target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
			target_f = self.model.predict(np.array([state]))
			target_f[0][np.argmax(action)] = target
			self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

	def train_short_memory(self, state, action, reward, next_state, done):
		target = reward
		if not done:
			target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 20)))[0])
		target_f = self.model.predict(state.reshape((1, 20)))
		target_f[0][np.argmax(action)] = target
		self.model.fit(state.reshape((1, 20)), target_f, epochs=1, verbose=0)