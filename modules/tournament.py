from typing import List
from _strategy import Strategy
from _player import Player
from _game import Game
from strategies.cheater import Cheater
from strategies.goody_two_shoes import GoodyTwoShoes
from strategies.joker import Joker
from strategies.copycat import Copycat


class Tournament:
    def __init__(self, strategies: List[Strategy],
                 copies_of_each_strategy: int,
                 rounds_per_game: int,
                 initial_player_score: int,
                 top_percentage: float):
        self.copies_of_each_strategy = copies_of_each_strategy
        self.rounds_per_game = rounds_per_game
        self.top_percentage = top_percentage  # the percentage of top players to be multiplied to the next round

        self.players: List[Player] = []
        for strategy in strategies:
            strategy_name = strategy.name
            for i in range(self.copies_of_each_strategy):
                new_player = Player(name=strategy_name + ' #' + str(i).zfill(0),
                                    strategy=strategy,
                                    initial_score=initial_player_score)
                self.players.append(new_player)

        self.players_in_tournament = len(self.players)

        self.games: List[Game] = []

        self.setup()

    def setup(self):
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

                    self.games.append(new_game)
                    games_counter += 1

    def run(self):
        print('Running Tournament...')
        for game in self.games:
            game.run()
        print('Tournament finished!')

    def sort_players(self):
        self.players.sort(key=lambda player: player.score, reverse=True)

    def multiply_top_players(self):
        print('Sorting players...')
        self.sort_players()
        print('Players sorted!')

        print('Multiplying top players...')

        top_count = round(len(self.players) * self.top_percentage)
        top_players = self.players[:top_count]

        max_score = max([player.score for player in top_players])
        normalized_scores = [player.score / max_score for player in top_players]
        total_of_normalized_scores = sum(normalized_scores)
        percentages = [ns / total_of_normalized_scores for ns in normalized_scores]
        amounts = [round(self.players_in_tournament * p) for p in percentages]
        amounts[0] = self.players_in_tournament - sum(amounts[1:])

        players = []

        for player, amount in zip(top_players, amounts):
            players += [player.multiply() for _ in range(amount)]

        self.players = players

        print('Top players multiplied!')

    def get_players_data(self):
        return '\n'.join([str(player) for player in self.players])


if __name__ == '__main__':
    tournament_strategies = [
        GoodyTwoShoes(),
        Cheater(),
        Joker(),
        Copycat()
    ]

    tournament = Tournament(strategies=tournament_strategies,
                            copies_of_each_strategy=5,
                            rounds_per_game=10,
                            initial_player_score=100,
                            top_percentage=.8)

    generations = 10

    print(tournament.get_players_data())

    for _ in range(generations):
        tournament.run()
        tournament.multiply_top_players()

    print(tournament.get_players_data())
