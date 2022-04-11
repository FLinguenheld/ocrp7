from multiprocessing import (Process, Manager)

from time import time
from itertools import combinations as itertools_combinations

from stockmanager import (Stock, StocksCombination)
from views.view import View
from selectfile import SelectionFile

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Mix/Max −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def search_last_indice_before_maxi(list_of_actions: list[Stock], maxi: int=500):
    """ Loops in list_of_actions and adds action's prices.
        Returns last index before price > maxi """

    addition = 0
    for i, a in enumerate(list_of_actions):
        addition += a.f_price

        if addition > maxi:
            return i 

    return 0

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def search_best(list_of_actions, nb_actions_per_combination, combinations, counters):

    best_combination = StocksCombination(stocks=[])
    counter = 0

    for c in itertools_combinations(list_of_actions, nb_actions_per_combination):
        counter += 1

        best_combination = StocksCombination.best_stock(best_combination, StocksCombination(stocks=c))

    combinations.append(best_combination)
    counters.append(counter)


# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Force brute", sf_bodies=['Selectionnez un fichier'])
# list_of_actions = select.select_file()
list_of_actions = select.select_file('essai.csv')

# −−−−−−−−−−−−−−−−−−−--−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- view −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')
my_view = View(header='Force brute threads', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

t0 = time()

# −−−−−−−−−−−−−−−−−−−--−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Min / Max to reduce the list_combinations amount −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
max = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price))
min = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price, reverse=True))

# −−−−−−−−−−−−−−−−−−−--−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Lauching threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
manager = Manager()
combinations = manager.list()
counters = manager.list()
threads = []

for i in range(min, max + 1):
    p = Process(target=search_best, args=(list_of_actions, i, combinations, counters))
    threads.append(p)
    p.start()

for t in threads:
    t.join()

best_combination = StocksCombination.best_stock_in_list(combinations)
counters = sum(counters)

# −−−−−−−−−−−−−−−−−−−--−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append(f'{counters} combinaisons testées en {time() - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(f'{best_combination.sorted_stocks()}')

my_view.stop_loading()
my_view.show()
