from dataclasses import dataclass
from typing import(Any)

from time import sleep

@dataclass
class Stock:
    """ Container for one ation """

    f_name: str
    f_price: float
    f_profit: float

    def __str__(self):
        return f"{self.f_name} - {self.f_price} - {self.f_profit}"

    def __gt__(self, other):
        return self.f_price > other.f_price

class StocksCombination:
    """ Container for a combination of several stocks
        Performs calculations, checks and allows to compare with other combinations """

    def __init__(self, stocks: Any, max_amount: float=500.0):
        self.max_amount =  max_amount
        # self.valid = False

        self.stocks = stocks
        self.price = 0.0
        self.profit = 0.0
        self.complete_profit = 0.0

        if stocks:
            #Price
            for it in stocks:
                self.price += it.f_price

            if self.price <= self.max_amount:
                self.valid = True

                #Gain
                for it in stocks:
                    self.profit += it.f_price * it.f_profit / 100
                    self.complete_profit += it.f_price * (1 + it.f_profit / 100)

    def add(self, new_stock: Stock):
        """ Adds an item and update price/profit/complete_profit """

        if (new_stock.f_price + self.price) <= self.max_amount:
            self.stocks.append(new_stock)

            #Price
            self.price += new_stock.f_price

            #Gain
            self.profit += new_stock.f_price * new_stock.f_profit / 100
            self.complete_profit += new_stock.f_price * (1 + new_stock.f_profit / 100)

            return True
        else:
            return False

    def __str__(self):
        if self.price > 0 and self.price <= self.max_amount:
            return f"{len(self.stocks)} actions : coût {round(self.price, 3)}" \
                                  f" — bénéfice {round(self.profit, 3)}" \
                                  f" — bénéfice total {round(self.complete_profit, 3)}"
        else:
            return f"Invalide, prix : {self.price}"

    def __lt__(self, other):
        return self.profit < other.profit

    def __len__(self):
        return len(self.stocks)

    def sorted_stocks(self):
        return "\n".join( str(i) for i in sorted(self.stocks))

    @staticmethod
    def best_stock(a, b):
        if a < b:
            return b
        else:
            return a

    @staticmethod
    def best_stock_in_list(stocks_list):
        best_stock = StocksCombination(stocks=[])

        for stock in stocks_list:
            best_stock = StocksCombination.best_stock(best_stock, stock)

        return best_stock
