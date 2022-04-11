from dataclasses import dataclass
from random import randint
from time import time

from stockmanager import (Stock, StocksCombination)

@dataclass
class Glutton:
    g_max: int
    g_list: list[Stock]

    def _random(self):

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

        best_combination = StocksCombination(stocks=[])
        counter = 0

        while counter < nb_tries:

            best_combination = StocksCombination.best_stock(best_combination, self._random())
            counter += 1

        return best_combination

    def random_by_time(self, time_in_seconds):

        best_combination = StocksCombination(stocks=[])
        counter = 0

        time_start = time()
        while time() - time_start < time_in_seconds:
            best_combination = StocksCombination.best_stock(best_combination, self._random())
            counter += 1

        return best_combination, counter
