import sys
import gym
import gym_environments
import numpy as np
from agent import DYNAQ
from gym.envs.registration import register
import os

register(
    id="Pirate-Ship-v0",
    entry_point="pirate.pirate:PiratesEnv"
)

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

def run(env, agent: DYNAQ, selection_method, episodes):
    for episode in range(episodes):
        if episode % 100 == 0:
            print("Episode {} of {}.".format(episode, episodes))
        observation, _ = env.reset()
        agent.start_episode()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, selection_method)
            next_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update_q(observation, action, next_observation, reward)
            agent.update_model(observation, action, reward, next_observation)
            observation = next_observation
        if selection_method == "epsilon-greedy":
            rewardTotal = 0
            for _ in range(100):
                state = np.random.choice(list(agent.visited_states.keys()))
                action = np.random.choice(agent.visited_states[state])
                reward, next_state = agent.model[(state, action)]
                agent.update_q(state, action, next_state, reward)
                rewardTotal = reward
            # print('reward', rewardTotal)



if __name__ == "__main__":
    environments = "Pirate-Ship-v0"
    episodes = 1500 if len(sys.argv) < 3 else int(sys.argv[2])

    env = gym.make(environments)
    agent = DYNAQ(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )

    # Train
    run(env, agent, "epsilon-greedy", episodes)
    env.close()

    # Play
    env = gym.make(environments, render_mode="human")
    run(env, agent, "greedy", 1)
    agent.render()
    env.close()
 