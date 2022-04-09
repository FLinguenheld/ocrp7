from dataclasses import dataclass
from typing import(List)

@dataclass
class Item:
    """ Container for one ation """

    f_name: str
    f_price: int
    f_profit: int

    def __str__(self):
        return f"{self.f_name} - {self.f_price} - {self.f_profit}"

class ItemsCombination:
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
