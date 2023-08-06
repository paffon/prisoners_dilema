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
        for round_number in range(self.rounds):
            self.round_number = round_number

            action_1, thoughts_1 = self.player_1.get_action_and_thoughts(self.moves_1, self.moves_2)
            action_2, thoughts_2 = self.player_2.get_action_and_thoughts(self.moves_2, self.moves_1)

            flip_1 = random.random() < mistake_chance
            flip_2 = random.random() < mistake_chance

            action_1_final = self.flip(action_1) if flip_1 else action_1
            action_2_final = self.flip(action_2) if flip_2 else action_2

            print_action_1_final = f'->{action_1_final}' if flip_1 else '\t'
            print_action_2_final = f'->{action_2_final}' if flip_2 else '\t'

            print_actions = f'\nRound {str(round_number + 1).zfill(2)}\t\t' \
                            f'{self.player_1.name} {action_1}{print_action_1_final}' \
                            f' \t{self.player_2.name} {action_2}{print_action_2_final}'
            self.my_print(print_actions)
            if self.debug:
                self.print_two_paragraphs(thoughts_1, thoughts_2)

            add_1, sub_1, add_2, sub_2 = self.calculate_gains_losses(action_1_final,
                                                                     action_2_final)
            self.moves_1.append(action_1_final)
            self.moves_2.append(action_2_final)

            self.player_1.update_score(add_1, sub_1)
            self.player_2.update_score(add_2, sub_2)

            tabs = '\t' * 5
            print_scores = f'\t\t\t\t{self.player_1.score}{tabs}{self.player_2.score}'
            self.my_print(print_scores)

    @staticmethod
    def calculate_gains_losses(action_1: int, action_2: int):
        add_1 = 3 if action_2 else 0
        add_2 = 3 if action_1 else 0
        sub_1 = -1 if action_1 else 0
        sub_2 = -1 if action_2 else 0

        return add_1, sub_1, add_2, sub_2

    @staticmethod
    def print_two_paragraphs(sentence_1, sentence_2):
        def split_string_by_length(input_string, n):
            return [input_string[j:j + n] for j in range(0, len(input_string), n)]

        paragraph_width = 15

        res1 = split_string_by_length(sentence_1, paragraph_width)
        res2 = split_string_by_length(sentence_2, paragraph_width)

        left_tabs = '\t' * 4
        middle_tabs = '\t' * 2

        lines = []

        for i in range(max([len(res1), len(res2)])):
            left_text = res1[i] if i < len(res1) else ''
            left_text_length = len(left_text)

            left_padding = paragraph_width - left_text_length
            left_spaces = ' ' * left_padding

            left_part = left_text + left_spaces

            right_text = res2[i] if i < len(res2) else ''

            new_line = left_tabs + left_part + middle_tabs + right_text

            lines.append(new_line)

        print('\n'.join(lines))

if __name__ == '__main__':
    debug = True
    initial_scores = 100
    goody = GoodyTwoShoes()
    cheater = Cheater()
    joker = Joker()
    copycat = CopyCat()
    copy_kitten = CopyKitten(defined_limit=2)
    cowboy = Cowboy(defined_limit=3)
    businessman = Businessman(random_actions=2, kindness_limit=.5, begin_cooperation=2, copy_kitten_limit=2)

    strategy_1 = copy_kitten
    strategy_2 = copycat

    p1 = Player(name=strategy_1.name, strategy=strategy_1, initial_score=initial_scores, debug=debug)
    p2 = Player(name=strategy_2.name, strategy=strategy_2, initial_score=initial_scores, debug=debug)

    game = Game(player_1=p1, player_2=p2,
                name='test game', rounds=10,
                debug=True)

    game.run(mistake_chance=0.75)



