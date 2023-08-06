from modules._strategy import Strategy


class Cheater(Strategy):

    def __init__(self):
        super().__init__('Cheater')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return 0
