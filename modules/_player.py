from abc import abstractmethod
from _strategy import Strategy
import re


class Player:
    def __init__(self, name: str, strategy: Strategy, initial_score: int, version: int = 0):
        self.name = name
        self.strategy = strategy
        self.score = self.initial_score = initial_score
        self.moves = []
        self.version = version
        self.scores_history = []

    def __repr__(self):
        return f'"{self.name}" [{self.strategy.name}, {self.score:}]'

    def update_score(self, add, subtract):
        # Subtract is negative
        self.score += add
        self.score += subtract

    def act(self, self_moves, opponent_moves):
        action = self.strategy.get_recommended_action(self_moves, opponent_moves)
        self.moves.append(action)
        return action

    def reset(self):
        self.moves = []
        self.scores_history.append(self.score)
        self.score = self.initial_score

    def multiply(self):
        new_name = self.increment_copy_number(self.name)
        new_player = Player(name=new_name,
                            strategy=self.strategy,
                            initial_score=self.initial_score)
        return new_player

    @staticmethod
    def increment_copy_number(name):
        # Define the regular expression pattern
        pattern = r'^Copy #(\d+)'

        match = re.match(pattern, name)
        if match:
            # If the name matches the pattern, extract the copy number
            copy_number = int(match.group(1))
            name_without_original_copy = name.replace(f'Copy #{copy_number} ', '')
            new_name = f"Copy #{copy_number + 1} {name_without_original_copy}"
        else:
            # If the name doesn't match the pattern, set copy_number to 1
            new_name = f"Copy #1 of {name}"

        return new_name
