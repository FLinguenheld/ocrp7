from copy import deepcopy
from threading import Thread
from itertools import combinations

from dataclasses import dataclass
from typing import(Any,
                   Optional,
                   List)

@dataclass
class Item:
    """ Container for one ation """

    f_name: str
    f_price: float
    f_profit: float

    def __str__(self):
        return f"{self.f_name} - {self.f_price} - {self.f_profit}"

class Items_Combination:
    """ Container for a combination of several actions
        Performs calculations, checks and allows to compare with other combinations """

    def __init__(self, items : List[Item], max_amount: int=500):
        self.max_amount =  max_amount

        self.valid = False
        self.items = items
        self.gain = 0.0
        self.complete_gain = 0.0
        self.price = 0.0

        #Price
        for it in items:
            self.price += it.f_price

        if self.price <= self.max_amount:
            self.valid = True

            #Gain
            for it in items:
                self.gain += it.f_price * it.f_profit / 100
                self.complete_gain += it.f_price * (1 + it.f_profit / 100)

    def __str__(self):
        if self.valid:
            return f"{len(self.items)} actions : coût {round(self.price, 3)}" \
                                  f" — bénéfice {round(self.gain, 3)}" \
                                  f" — bénéfice total {round(self.complete_gain, 3)}"
        else:
            return f"Invalide, prix trop élevé : {self.price}"

    def __gt__(self, other):
        return self.gain > other.gain

    def __len__(self):
        return len(self.items)


class Combinations_manager(Thread):
    """ Test to dispatch all researches """

    def __init__(self, list_of_actions: list[Items_Combination], r: int, best_of_the_best: list[Items_Combination]):
        Thread.__init__(self)
        
        self.list_of_actions = list_of_actions
        self.r = r
        self.best_of_the_best = best_of_the_best


    def run(self):

        best_combination = None
        for c in combinations(self.list_of_actions, self.r):
                # self.nb_combinaisons += 1
                new_combination = Items_Combination(c)

                if not best_combination or new_combination > best_combination:
                    best_combination = new_combination
        
        self.best_of_the_best.append(best_combination)

        # return best_combination

