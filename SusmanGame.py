import gym
from gym import spaces
import numpy as np
import random

class SusmanGameEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SusmanGameEnv, self).__init__()
        self.board_width = 10
        self.board_height = 1
        self.board = np.zeros([self.board_height, self.board_width])
        self.player_location = {'x':0, 'y': 0}
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(2) # East, West
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=1, shape=
                    (2, self.board_height, self.board_width), dtype=np.uint8)
        #Dimension 0 = Board (One Hot)
        #Dimension 1 = Player (One Hot)
        self.max_turns = 100
        self.this_turn = 0

        self.reset_board()
        self.set_goal()

    def get_observations(self, reward = 0, done = False, info = ''):
        #state, reward, done, info
        return self.get_state(), reward, done, info

    def get_state(self):
        state = np.zeros([2, self.board_height, self.board_width])

        for y in range(self.board_height):
            for x in range(self.board_width):
                state[0, y, x] = self.board[y, x]
                if self.player_location['x'] == x and self.player_location['y'] == y:
                    state[1, y, x] = 1

        return state

    def set_goal(self):
        rand_y = 0
        rand_x = 0

        while True:
            if self.board_width > 1:
                rand_x = random.randrange(0, self.board_width - 1)
            if self.board_height > 1:
                rand_y = random.randrange(0, self.board_height - 1)
            if self.player_location['x'] != rand_x or self.player_location['y'] != rand_y:
                break

        self.board[rand_y, rand_x] = 1

    def step(self, action):
        reward = 0
        done = False
        self.this_turn += 1

        if action == 0: #Move East
            target_e = self.player_location['x'] + 1
            if target_e >= self.board_width:
                return self.get_observations(reward=-10, done=True, info='Loose')
            self.player_location['x'] += 1
            if self.board[self.player_location['y'], self.player_location['x']] == 1:
                return self.get_observations(reward=10, done=True, info='Win')
            else:
                return self.get_observations(reward=1, done=False, info='Continue')

        if action == 1: #Move West
            target_w = self.player_location['x'] - 1
            if target_w < self.board_width:
                return self.get_observations(reward=-1000, done=True, info='Loose Fall Off Map')
            self.player_location['x'] -= 1
            if self.board[self.player_location['y'], self.player_location['x']] == 1:
                return self.get_observations(reward=1000, done=True, info='Win Got Target')
            else:
                return self.get_observations(reward=1, done=False, info='Continue')

        if self.this_turn == self.max_turns:
            return self.get_observations(reward=-1000, done=True, info='Loose Too Many Moves')

        return self.get_observations(reward, done, '')
        # Execute one time step within the environment

    def reset(self):
        self.this_turn = 0
        self.reset_board()
        self.set_goal()

    def render(self, mode='human', close=False):
        result = ''
        for y in range(self.board_height):
            for x in range(self.board_width):
                result += ' '
                result += str(self.board[y, x])
                if self.player_location['x'] == x and self.player_location['y'] == y:
                    result += 'S'
                else:
                    result += ' '
                result += '|'
            result += '\n'

        print(result)
        # Render the environment to the screen

    def reset_board(self):
        self.board = np.zeros([self.board_height, self.board_width])
