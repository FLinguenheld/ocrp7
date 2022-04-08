from threading import Thread
from random import sample
from random import randint
from dataclasses import dataclass

@dataclass
class Item:
    """ Container for one ation """

    f_name: str
    f_price: float
    f_profit: float

    def __str__(self):
        return f"{self.f_name} - {self.f_price} - {self.f_profit}"

    def __gt__(self, other):
        return self.f_price > other.f_price

class ItemsCombination:
    """ Container for a combination of several actions
        Performs calculations, checks and allows to compare with other combinations """

    def __init__(self, max_amount: int):
        self.max_amount =  max_amount

        self.items = []
        self.gain = 0.0
        self.complete_gain = 0.0
        self.price = 0.0

    def add(self, new_item: Item):

        if (new_item.f_price + self.price) <= self.max_amount:
            self.items.append(new_item)

            #Price
            self.price += new_item.f_price

            #Gain
            self.gain += new_item.f_price * new_item.f_profit / 100
            self.complete_gain += new_item.f_price * (1 + new_item.f_profit / 100)

            return True
        else:
            return False

    def sorted_items(self):
        return "\n".join( str(i) for i in sorted(self.items))

    def __str__(self):
        if self.price <= self.max_amount:
            return f"{len(self.items)} actions : coût {round(self.price, 3)}" \
                                  f" — bénéfice {round(self.gain, 3)}" \
                                  f" — bénéfice total {round(self.complete_gain, 3)}"
        else:
            return f"Invalide, prix trop élevé : {self.price}"

    def __gt__(self, other):                                    # Best choice ?
        return self.gain > other.gain
        # return self.complete_gain > other.complete_gain

    def __len__(self):
        return len(self.items)


@dataclass
class Glouton:
    g_max: int
    g_list: list[Item]
    g_max_items_in_combi: int=25

    def random(self):

        currentCombination = ItemsCombination(max_amount=self.g_max)

        indexes = sample(range(0, len(self.g_list)), len(self.g_list))            # Too long
        # indexes = sample(range(0, len(self.g_list)), self.g_max_items_in_combi)

        while currentCombination.price <= self.g_max and indexes:
            currentCombination.add(self.g_list[indexes.pop()])

        return currentCombination

class GloutonThread(Thread):

    def __init__(self, g_max: int, g_list: list[Item], results: list, id_thread: int, counter: list[int]):
        Thread.__init__(self)
        self.stop = False

        self.g_max = g_max
        self.g_list = g_list
        self.id_thread = id_thread
        self.results = results

        self.glouton = Glouton(self.g_max, self.g_list)
        self.counter = counter

    def run(self):

        self.results[self.id_thread] = ItemsCombination(max_amount=self.g_max)
        while not self.stop:

            self.counter[self.id_thread] += 1
            new_combination = self.glouton.random()
            if new_combination > self.results[self.id_thread]:
                self.results[self.id_thread] = new_combination

