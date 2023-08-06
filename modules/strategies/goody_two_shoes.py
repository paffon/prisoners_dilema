from modules._strategy import Strategy


class GoodyTwoShoes(Strategy):

    def __init__(self):
        super().__init__('Goody Two Shoes')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return 1
