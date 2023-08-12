from typing import List
from _player import Player
from _game import Game
from strategies.strategies import *
import math
from visuals.tournament_visualizer import *


class Tournament:
    def __init__(self, strategies: List[Strategy],
                 copies_of_each_strategy: int,
                 rounds_per_game: int,
                 games_between_players: int,
                 initial_player_score: int,
                 top_percentage: float,
                 mistake_chance: float,
                 debug: bool = False):

        self.rounds_per_game = rounds_per_game
        self.games_between_players = games_between_players
        self.top_percentage = top_percentage  # the percentage of top players to be multiplied to the next round
        self.mistake_chance = mistake_chance
        self.debug = debug

        self.players = self.generate_players(strategies, copies_of_each_strategy, initial_player_score)

        self.total_players = len(self.players)

    def generate_players(self, strategies, copies_of_each_strategy, initial_player_score):
        players = []
        for strategy in strategies:
            self.my_print(f'Generating {strategy.name}')
            for i in range(copies_of_each_strategy):
                new_player = Player(name=f'{strategy.name} #{str(i).zfill(0)}',
                                    strategy=strategy,
                                    initial_score=initial_player_score)
                players.append(new_player)
        return players

    def my_print(self, obj):
        if self.debug:
            print(obj)

    def setup_games(self):
        games = []
        games_counter = 1
        for player_1 in self.players:
            for player_2 in self.players:
                player_1.reset()
                player_2.reset()
                for i in range(self.games_between_players):
                    name_1 = player_1.name
                    name_2 = player_2.name
                    game_name = f'#{str(games_counter).zfill(3)} {name_1} vs. {name_2}'
                    new_game = Game(player_1=player_1,
                                    player_2=player_2,
                                    name=game_name,
                                    rounds=self.rounds_per_game)

                    games.append(new_game)
                    games_counter += 1
        return games

    def run(self):
        games = self.setup_games()
        for game in games:
            game.run(mistake_chance=self.mistake_chance)

    def sort_players(self):
        self.players.sort(key=lambda player: float(player.score), reverse=True)

    def get_top_players(self):
        self.sort_players()

        top_count = math.ceil(len(self.players) * self.top_percentage)

        top_players = self.players[:top_count]
        return top_players

    def multiply_top_players(self):

        top_players = self.get_top_players()

        max_score = max([player.score for player in top_players])
        normalized_scores = [player.score / max_score for player in top_players]
        total_of_normalized_scores = sum(normalized_scores)
        percentages = [ns / total_of_normalized_scores for ns in normalized_scores]
        amounts = [round(self.total_players * p) for p in percentages]
        amounts[-1] = self.total_players - sum(amounts[:-1])

        players = []

        for player, amount in zip(top_players, amounts):
            players += [player.multiply() for _ in range(amount)]

        score_groups = {}
        for player in players:
            score_groups.setdefault(player.score, []).append(player)

        # Shuffle the players within each score group
        for score_group in score_groups.values():
            random.shuffle(score_group)

        # Flatten the list to get the final mixed order of players
        mixed_players = [player for score_group in score_groups.values() for player in score_group]

        # Now mixed_players contains the list of Player objects with the same score shuffled randomly,
        # while still being sorted by their score from high to low.

        self.players = mixed_players

    def get_players_data(self):
        return '\n'.join([f'{i + 1}.\t{player}' for i, player in enumerate(self.players)])

    def get_strategies_counter(self):
        strategies_counter = {}
        for player in self.players:
            strategy_name = str(player.strategy)
            amount = strategies_counter.get(strategy_name, 0) + 1
            strategies_counter[strategy_name] = amount
        return strategies_counter


if __name__ == '__main__':
    tournament_strategies = [
        GoodyTwoShoes(),
        Cheater(),
        Joker(threshold_to_cooperate=0.5),
        CopyCat(start_with=None),
        CopyKitten(defined_limit=2, start_with=1),
        Businessman(random_actions=4, kindness_limit=0, copy_kitten_limit=2, copy_kitten_start_with=1),
        Grudger(defined_limit=3),
        Sequential(sequence=[1, 0, 0, 1, 1, 0]),
        Alternator(alternate_after=2, start_with=1),
        Pavlovian(start_with=1),
        # Forgiver(grudge_limit=3, copy_kitten_limit=2, copy_kitten_start_with=1),
        # GenerousCopyKat(forgiveness_prob=0.2),
        # SoftMajorityRule(start_with=1),
    ]

    tournament = Tournament(strategies=tournament_strategies,
                            copies_of_each_strategy=2,
                            rounds_per_game=100,
                            games_between_players=2,
                            initial_player_score=0,
                            top_percentage=0.5,
                            mistake_chance=0.01,
                            debug=False)

    generations = 3

    strategies_components = []

    names = [str(strategy) for strategy in tournament_strategies]
    for generation in range(generations):
        d = tournament.get_strategies_counter()
        new_d = {name: str(d.get(name, 0)).zfill(3) for name in names}
        strategies_components.append(new_d)
        print(f'\nBefore tournament #{generation + 1}:\n{new_d}\n')

        tournament.run()
        tournament.sort_players()

        tournament.multiply_top_players()

    d = tournament.get_strategies_counter()
    new_d = {name: str(d.get(name, 0)).zfill(3) for name in names}
    strategies_components.append(new_d)
    print(f'\nAfter all tournaments:\n{new_d}\n')

    d = {key: value for key, value in tournament.__dict__.items() if key not in ['players', 'debug']}

    visualize(strategies_components, d)
