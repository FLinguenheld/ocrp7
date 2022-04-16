from dataclasses import dataclass
from typing import(Any)


@dataclass
class Stock:
    """ Container for one ation.
        Allows to compare two stocks directly by their price """

    f_name: str
    f_price: float
    f_profit: float

    def __str__(self):
        return f"{self.f_name} - {self.f_price} - {self.f_profit}"

    def __gt__(self, other):
        return self.f_price > other.f_price

class StocksCombination:
    """ Container for a combination of several stocks
        Performs calculations, checks and allows to compare with other combinations.
        A combination can be create in constructor with a stock's Container
        or stock by stock with the 'add' method. """

    def __init__(self, stocks: Any=None, max_amount: float=500.0):
        self.max_amount =  max_amount

        self.stocks = stocks or []
        self.price = 0.0
        self.profit = 0.0
        self.complete_profit = 0.0

        if stocks:
            # Price
            for s in stocks:
                self.price += s.f_price

                # Gain
                self.profit += s.f_price * s.f_profit / 100
                self.complete_profit += s.f_price * (1 + s.f_profit / 100)

            # Checks if combination is valid :
            if self.price >= self.max_amount:
                self.reset()

    def reset(self):
        """ Reset all combination's values """
        self.price = 0.0
        self.profit = 0.0
        self.complete_profit = 0.0
        self.stocks = []


    def add(self, new_stock: Stock):
        """ Adds a stock and updates price/profit/complete_profit
            Only if the max_amount is not exceeded
            returns True if ok """

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
            return f"combination invalide, prix : {self.price} (maximum autorisé : {self.max_amount})"

    def __lt__(self, other):
        return self.profit < other.profit

    def __len__(self):
        return len(self.stocks)

    def sorted_stocks(self):
        return "\n".join( str(i) for i in sorted(self.stocks))

    # −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    # Static methods to avoid warning due to thread Manager
    @staticmethod
    def best_stock(a, b):
        """ Returns the best stock """
        if a < b:
            return b
        else:
            return a

    @staticmethod
    def best_stock_in_list(stocks_list):
        """ Loops in the list and return the best combination """
        best_stock = StocksCombination()

        for stock in stocks_list:
            best_stock = StocksCombination.best_stock(best_stock, stock)

        return best_stock

    @staticmethod
    def sum(number_list):
        """ Simple addition, to avoid warning with sum() and threads proxies """
        total = 0
        for value in number_list:
            total += value

        return total

