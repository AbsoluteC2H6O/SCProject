import numpy as np


class MonteCarloDet:
    def __init__(self, states_n, actions_n, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.gamma = gamma
        self.pi = np.zeros((self.states_n))
        self.reset()

    def reset(self):
        self.episode = []  # número de episodios
        # valorar cada par estado-acción
        self.q = np.zeros((self.states_n, self.actions_n))
        self.pi = np.zeros((self.states_n))
        # Acumular los promedios
        self.returns = np.zeros((self.states_n, self.actions_n))
        # acumula el numero de iter
        self.returns_n = np.zeros((self.states_n, self.actions_n))

    def update(self, state, action, reward, terminated):
        self.episode.append((state, action, reward))
        if terminated == True:
            self._update_q()
            self.episode = []  # inicializo de nuevo los episodios

    def _update_q(self):
        G = 0
        self.episode.reverse()
        process = []
        for state, action, reward_a in (self.episode):
            G = self.gamma*G + reward_a

            if ((state, action) not in process):
                process.append((state, action))
                self.returns[state][action] += G  # append G
                self.returns_n[state][action] += 1  # promedio
                self.q[state][action] = (
                    self.returns[state][action] / self.returns_n[state][action])  # average q(st,at)
                self.pi[state] = np.argmax(
                    self.q[state])  # argmax pi(st,at)
      

    def get_action(self, state):
        return np.random.choice(self.actions_n)

    def get_action_greedy(self, state):
        return np.argmax(self.actions_n)

    def get_best_action(self, state):
        return self.pi[state]

    def get_pi_action(self, state):
        epsilon = np.random.uniform()
        if(epsilon < 0.1):
            return np.random.choice(self.actions_n)
        else:
            return int(self.pi[state])
        
    def render(self):
        print(f"Values: {self.q}\n")
