from abc import abstractmethod
from _strategy import Strategy


class Player:
    def __init__(self, name: str, strategy: Strategy, initial_score: int):
        self.name = name
        self.strategy = strategy
        self.score = self.initial_score = initial_score
        self.moves = []

    def __repr__(self):
        return f'Player: [{self.name}, {self.strategy}, {self.score:}]'

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
        self.score = self.initial_score

    def multiply(self):
        new_name = f'copy of {self.name}'
        new_player = Player(name=new_name,
                            strategy=self.strategy,
                            initial_score=self.initial_score)
        return new_player
