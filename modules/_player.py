from abc import abstractmethod
from _strategy import Strategy
import re


class Player:
    def __init__(self, name: str, strategy: Strategy, initial_score: int, version: int = 0, debug: bool = False):
        self.name = name
        self.strategy = strategy
        self.score = self.initial_score = initial_score
        self.moves = []
        self.version = version
        self.scores_history = []
        self.debug = debug

    def my_print(self, obj):
        if self.debug:
            print(obj)

    def __repr__(self):
        return f'"{self.name}" [{self.strategy}, {self.score:}]'

    def update_score(self, add, subtract):
        # Subtract is negative
        self.score += add
        self.score += subtract

    def get_action_and_thoughts(self, self_moves, opponent_moves):
        action, thoughts = self.strategy.get_recommended_action(self_moves, opponent_moves)
        self.moves.append(action)
        return action, thoughts

    def reset(self):
        self.moves = []
        self.scores_history.append(self.score)
        self.score = self.initial_score

    def multiply(self):
        new_player = Player(name=self.name,
                            strategy=self.strategy,
                            initial_score=self.initial_score)
        return new_player
