import random
import numpy as np
from game.model import create_model
from collections import deque
from keras.models import load_model

ACTIONS = ['', 'left', 'right', 'rotate']


def parse_board(state):
    return np.array(state).flatten()


class LearningAgent(object):
    def __init__(self, exploration_rate=.3, memory=10000, model=create_model(), batch_size=100, gamma=0.9):
        self.Q = deque([], memory)
        self.er = exploration_rate
        self.filename = 'cnn_agent.h5'
        self.model = model
        self.batch_size = batch_size
        self.gamma = gamma

    def _update_priority(self):
        for i in range(len(self.Q)):
            parsed_board = parse_board(self.Q[i]['board'])
            action_index = ACTIONS.index(self.Q[i]['action'])
            pv = self.model.predict(parsed_board.reshape((1, 20, 10, 1)))[0][action_index]
            r = self.Q[i]['reward']
            try:
                parsed_board_t1 = parse_board(self.Q[i]['board_t1'])
                pv_t1 = self.model.predict(parsed_board_t1.reshape((1, 20, 10, 1))).max()
                priority = abs(pv - r - pv_t1)

            except KeyError:
                priority = abs(pv - r)

            self.Q[i]['priority'] = priority

    def _select_sample(self, sample_size):
        turns = list(self.Q)

        sorted_turns = sorted(turns, key= lambda turn: turn['priority'], reverse=True)
        return sorted_turns[:sample_size]


    def get_action(self, board):
        if random.random() < self.er:
            return random.choice(ACTIONS)

        parsed_board = parse_board(board)

        y = self.model.predict(parsed_board.reshape((1, 20, 10, 1)))[0]
        index = y.argmax()

        return ACTIONS[index]

    def learn(self):
        self._update_priority()
        self._select_sample(10)
        sample_size = min(len(self.Q), self.batch_size)

        #moves = random.sample(self.Q, sample_size)
        moves = self._select_sample(sample_size)

        states = []
        values = []

        for move in moves:
            parsed_board = parse_board(move['board'])
            action_values = self.model.predict(parsed_board.reshape((1, 20, 10, 1)))[0]
            try:
                parsed_board_t1 = parse_board(move['board_t1'])
                predicted_reward = self.model.predict(parsed_board_t1.reshape((1, 20, 10, 1)))[0].max()
                reward = move['reward'] + self.gamma * predicted_reward
            except KeyError:
                reward = move['reward']

            action_values[ACTIONS.index(move['action'])] = reward

            states.append(parsed_board.reshape((20, 10, 1)))
            values.append(action_values)

        states = np.array(states)
        values = np.array(values)

        self.model.train_on_batch(states, values)

    def memorize(self, moves):
        for move in moves:
            if move['action'] != '':
                move['reward'] -= self.gamma / 10
            self.Q.append(move)

    def save(self):
        self.model.save(self.filename)

    def load(self):
        try:
            self.model = load_model(self.filename)
        except:
            self.model = create_model(lr=0.001)
