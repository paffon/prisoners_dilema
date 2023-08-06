from typing import List
from _player import Player
from _game import Game
from strategies.strategies import *
import math


class Tournament:
    def __init__(self, strategies: List[Strategy],
                 copies_of_each_strategy: int,
                 rounds_per_game: int,
                 initial_player_score: int,
                 top_percentage: float,
                 mistake_chance: float,
                 debug: bool = False):

        self.copies_of_each_strategy = copies_of_each_strategy
        self.rounds_per_game = rounds_per_game
        self.top_percentage = top_percentage  # the percentage of top players to be multiplied to the next round
        self.mistake_chance = mistake_chance
        self.debug = debug

        self.players = self.generate_players(strategies, initial_player_score)

        self.total_players = len(self.players)

        self.games = self.setup_games()

    def generate_players(self, strategies, initial_player_score):
        players = []
        for strategy in strategies:
            self.my_print(f'Generating {strategy.name}')
            strategy_name = strategy.name
            for i in range(self.copies_of_each_strategy):
                new_player = Player(name=strategy_name + ' #' + str(i).zfill(0),
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
                for i in range(self.rounds_per_game):
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
        for game in self.games:
            game.run(mistake_chance=self.mistake_chance)

    def sort_players(self):
        self.players.sort(key=lambda player: player.score, reverse=True)

    def multiply_top_players(self):
        self.sort_players()

        top_count = math.ceil(len(self.players) * self.top_percentage)
        top_players = self.players[:top_count]

        max_score = max([player.score for player in top_players])
        normalized_scores = [player.score / max_score for player in top_players]
        total_of_normalized_scores = sum(normalized_scores)
        percentages = [ns / total_of_normalized_scores for ns in normalized_scores]
        amounts = [round(self.total_players * p) for p in percentages]
        amounts[0] = self.total_players - sum(amounts[1:])

        players = []

        for player, amount in zip(top_players, amounts):
            players += [player.multiply() for _ in range(amount)]

        self.players = players

    def get_players_data(self):
        return '\n'.join([f'{i + 1}.\t{player}' for i, player in enumerate(self.players)])

    def get_strategies_counter(self):
        strategies_counter = {}
        for player in self.players:
            strategy_name = player.strategy.name
            amount = strategies_counter.get(strategy_name, 0) + 1
            strategies_counter[strategy_name] = amount
        return strategies_counter


if __name__ == '__main__':
    tournament_strategies = [
        GoodyTwoShoes(),
        Cheater(),
        Joker(),
        CopyCat(),
        CopyKitten(),
        Cowboy(),
        Businessman()
    ]

    tournament = Tournament(strategies=tournament_strategies,
                            copies_of_each_strategy=5,
                            rounds_per_game=100,
                            initial_player_score=100,
                            top_percentage=0.5,
                            mistake_chance=0.05,
                            debug=False)

    generations = 5
    names = [strategy.name for strategy in tournament_strategies]
    d = tournament.get_strategies_counter()
    new_d = {name: str(d.get(name, 0)).zfill(3) for name in names}
    print(f'Initial conditions:\n{new_d}\n')
    for generation in range(generations):
        tournament.run()
        tournament.multiply_top_players()
        d = tournament.get_strategies_counter()
        new_d = {name: str(d.get(name, 0)).zfill(3) for name in names}
        print(f'After tournament #{generation+1}:\n{new_d}\n')
