from modules._strategy import Strategy
import random


class GoodyTwoShoes(Strategy):
    """Always cooperate"""

    def __init__(self):
        super().__init__('GoodyTwoShoes')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return 1, "I always cooperate"


class Cheater(Strategy):
    """Always cheat"""

    def __init__(self):
        super().__init__('Cheater')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return 0, "I always cheat"


class Joker(Strategy):
    """Random behavior"""

    def __init__(self):
        super().__init__('Joker')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return round(random.random()), "I am crazy!"


class CopyCat(Strategy):
    """Starts by cooperating,
    then imitates opponent"""

    def __init__(self):
        super().__init__('CopyCat')

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        if len(self_moves) == 0:
            return 1, "I start by cooperating"
        else:
            return opponent_moves[-1], "I just copy you"


class CopyKitten(Strategy):
    """Like CopyKay,
    but changes action only after n consistently opposite actions from opponent"""

    def __init__(self, defined_limit: int = 2):
        super().__init__('CopyKitten')
        self.limit = defined_limit

    def get_recommended_action(self, self_moves, opponent_moves):
        limit = self.limit
        if len(self_moves) < limit:
            return 1, "I am starting by cooperating"
        else:
            my_last_action = self_moves[-1]
            sum_of_last_n_opponent_actions = sum(opponent_moves[-limit:0])

            if my_last_action == 1 and sum_of_last_n_opponent_actions == 0:
                # I was cooperating, but opponent cheated too many times and now I'll cheat
                return 0, "I was cooperating, but you cheated more than my limit"
            elif my_last_action == 0 and sum_of_last_n_opponent_actions == limit:
                # I was cheating, but opponent cooperated enough times for me to cooperate
                return 1, "I was cheating, but you cooperated more than my limit"
            else:
                return my_last_action, "You haven not given me a reason to change my action"


class Cowboy(Strategy):
    """I will cooperate,
    but once you cheat me more times than my limit,
    I'll never cooperate again"""

    def __init__(self, defined_limit: int = 2):
        super().__init__('Cowboy')
        self.limit = defined_limit

    def get_recommended_action(self, self_moves, opponent_moves):
        opponent_cheating_counter = sum([opponent_action == 0 for opponent_action in opponent_moves])

        if opponent_cheating_counter >= self.limit:
            return 0, f"My limit was {self.limit} and you have broken my trust {opponent_cheating_counter} time(s) ({opponent_moves})"
        else:
            return 1, "You have not yet broken my trust, so I am cooperating"


class Businessman(Strategy):
    """I start with random_actions random actions.

    If you forgive my betrayals >= kindness_limit % of the times,
    then I'll assume you'll always cooperate,
    take advantage of your kindness and will always cheat.

    Otherwise, I'll assume you can retaliate and will from then on will
    behave like a CopyKitten(copy_kitten_limit)"""

    def __init__(self, random_actions: int = 2,
                 kindness_limit: float = 1.0,
                 begin_cooperation: int = 2,
                 copy_kitten_limit: int = 2):
        if random_actions < copy_kitten_limit:
            raise ValueError('cannot be')

        super().__init__('Businessman')

        self.random_actions = random_actions
        self.kindness_limit = kindness_limit
        self.begin_cooperation = begin_cooperation
        self.copy_kitten = CopyKitten(copy_kitten_limit)
        self.behave_like_copy_kitten = False
        self.they_are_suckers = False

    def get_recommended_action(self, self_moves, opponent_moves):
        if self.they_are_suckers:
            return 0, "I am taking advantage of your kindness"

        if self.behave_like_copy_kitten:
            return self.copy_kitten.get_recommended_action(
                self_moves=self_moves,
                opponent_moves=opponent_moves)

        rounds_played = len(self_moves)

        if rounds_played < self.random_actions:
            return round(random.random()), "I am testing the waters with random actions"

        elif rounds_played == self.random_actions:
            forgiveness_percentage = self.calculate_forgiveness_percentage(self_moves, opponent_moves)

            if forgiveness_percentage >= self.kindness_limit:
                self.they_are_suckers = True
                return self.get_recommended_action(self_moves, opponent_moves)
            else:
                self.behave_like_copy_kitten = True
                return self.copy_kitten.get_recommended_action(
                    self_moves=self_moves,
                    opponent_moves=opponent_moves)

    @staticmethod
    def calculate_forgiveness_percentage(self_moves, opponent_moves):
        my_moves_without_last = self_moves[:-1]
        their_moves_without_first = opponent_moves[1:]
        zipped = zip(my_moves_without_last, their_moves_without_first)

        forgiveness = sum([tup[0] == 0 and tup[1] == 1 for tup in zipped])

        forgiveness_percentage = forgiveness / len(my_moves_without_last)

        return forgiveness_percentage


class EverythingEveryWhereAllAtOnce(Strategy):
    # TODO: a strategy that randomly picks another strategy to use each time
    pass


if __name__ == '__main__':
    pass
