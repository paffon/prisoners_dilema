from abc import ABC, abstractmethod
import random


class Strategy(ABC):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        all_values = ', '.join([str(v) for k,v in self.__dict__.items() if k != 'name'])
        if len(all_values) > 0:
            s = ' [' + all_values + ']'
        else:
            s = ''
        result = f'{self.name}{s}'

        return result

    @abstractmethod
    def get_recommended_action(self, self_moves, opponent_moves):
        pass
