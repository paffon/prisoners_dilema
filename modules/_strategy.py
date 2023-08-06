from abc import ABC, abstractmethod
import random


class Strategy(ABC):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Strategy: {self.name}'

    @staticmethod
    def get_recommended_action(self_moves, opponent_moves):
        return round(random.random())
