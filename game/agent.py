import random
import numpy as np
import operator
import pickle

ACTIONS = ['', 'left', 'right', 'rotate']


def parse_board(state):
    return ''.join(map(str, list(np.array(state).flatten())))


class LearningAgent(object):
    def __init__(self, exploration_rate=.3):
        self.Q = {}
        self.er = exploration_rate
        self.alpha = 0.5
        self.pickle_file = 'learning_agent.pickle'

    def get_action(self, board):
        if random.random() < self.er:
            return random.choice(ACTIONS)

        parsed_board = parse_board(board)
        self.add_state(parsed_board)
        possible_actions = self.Q[parsed_board].items()
        best_action = max(possible_actions, key=operator.itemgetter(1))[0]

        return best_action

    def learn(self, moves):
        for move in moves:
            parsed_board = parse_board(move['board'])
            self.add_state(parsed_board)
            self.Q[parsed_board][move['action']] = (1 - self.alpha) * self.Q[parsed_board][move['action']] + self.alpha * move['reward']

    def add_state(self, parsed_board):
        try:
            self.Q[parsed_board]
        except KeyError:
            self.Q[parsed_board] = {}
            for action in ACTIONS:
                self.Q[parsed_board][action] = 0

    def save(self):
        data_set = {'learning_agent': self.Q}

        with open(self.pickle_file, 'wb') as pickle_file:
            pickle.dump(data_set, pickle_file, pickle.HIGHEST_PROTOCOL)
        pickle_file.close()

    def load(self):
        try:
            with open(self.pickle_file, 'rb') as f:
                save = pickle.load(f)
                q = save['learning_agent']
                del save
            self.Q = q
        except FileNotFoundError:
            print('the picle file was not found')
