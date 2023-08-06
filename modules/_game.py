from abc import abstractmethod
from _player import Player
from modules.strategies.strategies import *


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

    @staticmethod
    def flip(action_value):
        return 0 if action_value == 1 else 1

    def run(self, mistake_chance: float = .0):
        self.my_print(f'\t\t\t{self.player_1.strategy.name}\t\t\t{self.player_2.strategy.name}')
        self.my_print('-' * 50)
        for round_number in range(self.rounds):
            self.round_number = round_number

            action_1 = self.player_1.act(self.moves_1, self.moves_2)
            action_2 = self.player_2.act(self.moves_2, self.moves_1)

            flip_1 = random.random() < mistake_chance
            flip_2 = random.random() < mistake_chance

            action_1_final = self.flip(action_1) if flip_1 else action_1
            action_2_final = self.flip(action_2) if flip_2 else action_2

            print_action_1_final = f'->{action_1_final}' if flip_1 else '\t'
            print_action_2_final = f'->{action_2_final}' if flip_2 else '\t'

            print_actions = f'\nRound {round_number}\t\t{action_1 = }{print_action_1_final}' \
                            f' \t{action_2 = }{print_action_2_final}'
            self.my_print(print_actions)

            add_1, sub_1, add_2, sub_2 = self.calculate_gains_losses(action_1_final,
                                                                     action_2_final)
            self.moves_1.append(action_1_final)
            self.moves_2.append(action_2_final)

            self.player_1.update_score(add_1, sub_1)
            self.player_2.update_score(add_2, sub_2)

            tabs = '\t' * 5
            print_scores = f'\t\t\t{self.player_1.score}{tabs}{self.player_2.score}'
            self.my_print(print_scores)

    @staticmethod
    def calculate_gains_losses(action_1: int, action_2: int):
        add_1 = 3 if action_2 else 0
        add_2 = 3 if action_1 else 0
        sub_1 = -1 if action_1 else 0
        sub_2 = -1 if action_2 else 0

        return add_1, sub_1, add_2, sub_2


if __name__ == '__main__':
    initial_scores = 100
    p1 = Player(name='p1', strategy=CopyKitten(), initial_score=initial_scores)
    p2 = Player(name='p2', strategy=CopyCat(), initial_score=initial_scores)

    game = Game(player_1=p1, player_2=p2,
                name='test game', rounds=10,
                debug=True)

    game.run(mistake_chance=0.25)

    # print(p1, '\n\t', game.moves_1)
    # print(p2, '\n\t', game.moves_2)