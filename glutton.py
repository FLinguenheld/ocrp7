from dataclasses import dataclass
from random import randint
from time import time

from stockmanager import (Stock, StocksCombination)


@dataclass
class Glutton:
    """ Glutton algorithm, give the maximum price and the list of stocks.
        Then, use random by number of tries or by time.
        Simple but fast, it compares a lot of combinations and keeps the best one O(n) """

    g_max: int
    g_list: list[Stock]

    def _random(self):
        """ Algorithm, takes random index in stocks list to create and return a new combination.
            Prevents duplications.
            When price is close to maximum, it tries 5 more stocks to avoid a complete loop in stocks list """

        currentCombination = StocksCombination(stocks=[], max_amount=self.g_max)
        current_indexes = []
        counter_extra = 0                                               # Allows to try again after a refusal

        while len(current_indexes) < len(self.g_list):

            index = randint(0, len(self.g_list) -1)
            
            if index not in current_indexes:
                current_indexes.append(index)

                if not currentCombination.add(self.g_list[index]):
                    counter_extra += 1                                  # Refused by StocksCombination

                    if counter_extra > 5:                               # 5 tests more
                        break

                if currentCombination.price == self.g_max:
                    break

        return currentCombination

    def random_by_tries(self, nb_tries):
        """ Calls _random nb times and keeps the best combination """

        best_combination = StocksCombination()
        counter = 0

        while counter < nb_tries:

            best_combination = StocksCombination.best_stock(best_combination, self._random())
            counter += 1

        return best_combination

    def random_by_time(self, time_in_seconds):
        """ Calls _random nb during 'time' and keeps the best combination.
            Returns the best and a counter """

        best_combination = StocksCombination()
        counter = 0

        time_start = time()
        while time() - time_start < time_in_seconds:
            best_combination = StocksCombination.best_stock(best_combination, self._random())
            counter += 1

        return best_combination, counter
