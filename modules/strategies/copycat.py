from modules._strategy import Strategy


class Copycat(Strategy):

    def __init__(self):
        super().__init__('Copycat')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        if len(self_moves) == 0:
            return 1
        else:
            return opponent_moves[-1]
