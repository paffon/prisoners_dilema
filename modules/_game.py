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

            if self.debug:
                print_action_1_final = f'->{action_1_final}' if flip_1 else '\t'
                print_action_2_final = f'->{action_2_final}' if flip_2 else '\t'

                left_part = f'{self.player_1.strategy.name} {action_1}{print_action_1_final}'

                paragraph_width = 25

                left_part = self.bring_to_length(left_part, paragraph_width)

                print_actions = f'\nRound {str(round_number + 1).zfill(2)}\t\t' +\
                                left_part +\
                                f'\t{self.player_2.strategy.name} {action_2}{print_action_2_final}\n'

                self.my_print(print_actions)

                self.print_two_paragraphs(thoughts_1, thoughts_2, paragraph_width)

            self.moves_1.append(action_1_final)
            self.moves_2.append(action_2_final)

            add_1, sub_1, add_2, sub_2 = self.calculate_gains_losses(action_1_final,
                                                                     action_2_final)

            self.player_1.update_score(add_1, sub_1)
            self.player_2.update_score(add_2, sub_2)

            tabs = '\t' * 8
            print_scores = f'\t\t\t\t{self.player_1.score}{tabs}{self.player_2.score}'
            self.my_print('\n' + print_scores)

    @staticmethod
    def bring_to_length(string, min_allowed_length):
        spaces = ''
        if len(string) < min_allowed_length:
            spaces = ' ' * (min_allowed_length - len(string))
        return string + spaces

    @staticmethod
    def calculate_gains_losses(action_1: int, action_2: int):
        add_1 = 3 if action_2 else 0
        add_2 = 3 if action_1 else 0
        sub_1 = -1 if action_1 else 0
        sub_2 = -1 if action_2 else 0

        return add_1, sub_1, add_2, sub_2

    @staticmethod
    def print_two_paragraphs(sentence_1, sentence_2, paragraph_width):
        def split_string_by_length(input_string, n):
            return [input_string[j:j + n] for j in range(0, len(input_string), n)]

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
    joker = Joker(threshold_to_cooperate=0.5)
    copycat = CopyCat(start_with=None)
    copy_kitten = CopyKitten(defined_limit=2, start_with=1)
    businessman = Businessman(random_actions=4, kindness_limit=0, copy_kitten_limit=2, copy_kitten_start_with=1)
    grudger = Grudger(defined_limit=3)
    sequential = Sequential(sequence=[1, 0, 0, 1, 1, 0])
    alternator = Alternator(alternate_after=2, start_with=1)
    pavlovian = Pavlovian(start_with=1)
    forgiver = Forgiver(grudge_limit=3, copy_kitten_limit=2, copy_kitten_start_with=1)
    generous_cat = GenerousCopyKat(forgiveness_prob=0.2)
    soft_majority = SoftMajorityRule(start_with=1)

    strategy_1 = soft_majority
    strategy_2 = copy_kitten

    p1 = Player(name=strategy_1.name.lower(), strategy=strategy_1, initial_score=initial_scores, debug=debug)
    p2 = Player(name=strategy_2.name.lower(), strategy=strategy_2, initial_score=initial_scores, debug=debug)

    game = Game(player_1=p1, player_2=p2,
                name='test game', rounds=100,
                debug=True)

    game.run(mistake_chance=0.05)
