from itertools import combinations as itertools_combinations
from multiprocessing import (Process, Manager)
from math import factorial
from time import time

from stockmanager import (Stock, StocksCombination)
from views.view import View
from selectfile import SelectionFile


MAX_AMOUNT = 500.0


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Mix/Max −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def search_last_indice_before_maxi(list_of_actions: list[Stock], maxi: float):
    """ Loops in list_of_actions and adds action's prices.
        Returns last index before price > maxi """

    addition = 0
    for i, a in enumerate(list_of_actions):
        addition += a.f_price

        if addition > maxi:
            return i

    return 0


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def search_best(list_of_actions: list[Stock], nb_actions_per_combination: int, combinations, counters):
    """ BruteForce algorithm with itertools_combinations. It finds all combinations for n stocks and saved the
        best one.
        Allows to use it with threads. Give two manager.list to 'combinations'and 'counters'
        These lists will be shared and filled by all threads.
        Once all threads finished, just sort or sum manager.lists """

    best_combination = StocksCombination()
    counter = 0

    for c in itertools_combinations(list_of_actions, nb_actions_per_combination):
        counter += 1

        best_combination = StocksCombination.best_stock(best_combination, StocksCombination(stocks=c))

    combinations.append(best_combination)
    counters.append(counter)


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Force brute", sf_bodies=['Selectionnez un fichier'])
list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')
# list_of_actions = select.select_file('essai_28_actions.csv')
# list_of_actions = select.select_file('dataset1_Python+P7.csv')
# list_of_actions = select.select_file('dataset2_Python+P7.csv')

t0 = time()

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Min / Max to reduce the list_combinations amount −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
max = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price), maxi=MAX_AMOUNT)
min = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price, reverse=True), maxi=MAX_AMOUNT)

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− combinaisons number ? −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
total_to_do = 0
for i in range(min, max +1):
    total_to_do += int(factorial(len(list_of_actions)) / (factorial(i) * (factorial(len(list_of_actions) - i))))

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− view −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}\n'
              f'{len(list_of_actions)} actions\n'
              f'Nombre de combinaisons à tester : {total_to_do}')

my_view = View(header='Force brute', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Lauching threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
manager = Manager()
combinations = manager.list()
counters = manager.list()
threads = []

for i in range(min, max + 1):
    p = Process(target=search_best, args=(list_of_actions, i, combinations, counters))
    threads.append(p)
    p.start()

for t in threads:
    my_view.update_loading(round(sum(counters) / total_to_do * 100))
    t.join()

my_view.update_loading(100)
best_combination = StocksCombination.best_stock_in_list(combinations)
counter = sum(counters)

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append(f'{counter} combinaisons en {time() - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(f'{best_combination.sorted_stocks()}')

my_view.stop_loading()
my_view.show()
