import time
import numpy as np
import gym
from gym import spaces
import pygame
from . import settings
from .world import World
import maze_generators
class FrozenLakeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.delay = settings.DEFAULT_DELAY
        # Maze
        self._rows = kwargs.get("rows", settings.ROWS)
        self._cols = kwargs.get("cols", settings.COLS)
        maze_generator = kwargs.get(
            "maze_generator_class", maze_generators.KruskalMazeGenerator
        )(self._rows, self._cols)
        self.walls = maze_generator.generate()
        M= maze_generator.generatePMatrix()
        self.P = M[0]
        self.current_action = 0
        self.state =  M[1]
        self.current_reward = 0.0
        self.world = World(
            "Robot battery Environment as maze",
            M[1],
            self.current_action,
            self.P,
            self.walls,
            M[1],
        )
        self.initialState = M[1]
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        np.random.seed(seed)
        self.state = self.state
        self.current_action = 0
        self.world.reset(self.state, self.current_action)
        return 0, {}

    def step(self, action):
        self.current_action = action
        _, self.state, self.current_reward, terminated = self.P[self.state][self.current_action][0]
        if(terminated):
            self.world.update(
                self.state,
                self.current_action,
                self.current_reward,
                terminated,
            )
            # self.render()
            # time.sleep(3)
            # self.close()
        else:
            self.world.update(
                self.state,
                self.current_action,
                self.current_reward,
                terminated,
            )

            # self.render()
            # time.sleep(self.delay)

        return self.state, self.current_reward, terminated, False, {}

    def render(self):
        # print(
        #     "Action {}, reward {}, state {}".format(
        #         self.current_action, self.current_reward, self.state
        #     )
        # )
        # self.renderInConsole()
        # self.world.render()
        c= 0

    def close(self):
        self.world.close()
    
    def renderInConsole(self):
        # print("-" * int(self._cols * 2 + 1))
        for i in range(self._rows):
            for j in range(self._cols):
                # evaluate if there is a left wall
                current_index = i * self._cols + j
                left_index = i * self._cols + j - 1
                has_left_wall = (
                    j == 0
                    or (current_index, left_index) in self.walls
                    or (left_index, current_index) in self.walls
                )

                # render the left wall if exists
                # if has_left_wall:
                #     print("|", end="")
                # else:
                #     # space if there is no a left wall
                #     print(" ", end="")

                # render the cell
                # print(' ', end="")

            # render the right wall for the current row
            # print("|")

            # render the first bottom wall
            # print("-", end="")

            # render the bottom wall when if exists
            for j in range(self._cols):
                current_index = i * self._cols + j
                bottom_index = (i + 1) * self._cols + j
                has_bottom_wall = (
                    i == self._rows - 1
                    or (current_index, bottom_index) in self.walls
                    or (bottom_index, current_index) in self.walls
                )
                # if has_bottom_wall:
                #     print("-", end="")
                # else:
                #     # space if there is not a bottom wall
                #     print(" ", end="")
                
                # render the next bottom wall
                # print("-", end="")

            # finally, end of line
            # print("")
