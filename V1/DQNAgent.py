import random
import numpy as np
import tensorflow as tf

class DQNAgent:
    def __init__(self, observation_space_size, action_space_size):
        self.observation_space_size = observation_space_size
        self.action_space_size = action_space_size
        
        # Hiperparámetros del modelo
        self.discount_factor = 0.99
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.batch_size = 32
        self.memory_size = 10000
        
        # Modelo
        self.model = self.build_model()
        
        # Memoria de repetición
        self.memory = []
        
    def build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.observation_space_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_space_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.memory_size:
            del self.memory[0]
            
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space_size)
        else:
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])
        
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        minibatch = random.sample(self.memory, self.batch_size)
        states = []
        targets = []
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.discount_factor * np.amax(self.model.predict(next_state)[0])
            q_values = self.model.predict(state)
            q_values[0][action] = target
            states.append(state[0])
            targets.append(q_values[0])
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        self.model.load_weights(name)
        
    def save(self, name):
        self.model.save_weights(name)