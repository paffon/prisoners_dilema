import random

from modules._strategy import Strategy


class Joker(Strategy):

    def __init__(self):
        super().__init__('Joker')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return round(random.random())
