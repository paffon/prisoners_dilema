from abc import abstractmethod
from _player import Player
from modules.strategies.goody_two_shoes import GoodyTwoShoes
from modules.strategies.cheater import Cheater
from modules.strategies.joker import Joker
from modules.strategies.copycat import Copycat


class Game:
    def __init__(self, player_1: Player, player_2: Player,
                 name: str, rounds: int, debug: bool = False):
        self.player_1 = player_1
        self.player_2 = player_2
        self.name = name
        self.rounds = rounds
        self.moves_1 = []
        self.moves_2 = []
        self.debug = debug
        self.round_number = 1

    def my_print(self, obj):
        if self.debug:
            print(obj)

    def run(self):
        for round_number in range(self.rounds):
            self.round_number = round_number

            action_1 = self.player_1.act(self.moves_1, self.moves_2)
            action_2 = self.player_2.act(self.moves_2, self.moves_1)

            add_1, sub_1, add_2, sub_2 = self.calculate_gains_losses(action_1,
                                                                     action_2)
            self.moves_1.append(action_1)
            self.moves_2.append(action_2)

            self.player_1.update_score(add_1, sub_1)
            self.player_2.update_score(add_2, sub_2)
            self.my_print(self.get_status())

    def get_status(self):
        p1_score = f'p1_score={self.player_1.score}'
        p2_score = f'p2_score={self.player_2.score}'
        return f'Round {self.round_number}: {p1_score}, {p2_score}'

    @staticmethod
    def calculate_gains_losses(action_1: int, action_2: int):
        add_1 = 3 if action_2 else 0
        add_2 = 3 if action_1 else 0
        sub_1 = -1 if action_1 else 0
        sub_2 = -1 if action_2 else 0

        return add_1, sub_1, add_2, sub_2


if __name__ == '__main__':
    initial_scores = 100
    p1 = Player(name='p1', strategy=Cheater(), initial_score=initial_scores)
    p2 = Player(name='p2', strategy=Copycat(), initial_score=initial_scores)

    game = Game(player_1=p1, player_2=p2,
                name='test game', rounds=10,
                debug=True)

    game.run()
