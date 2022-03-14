import threading
from time import sleep
from time import time
from itertools import combinations

from typing import(Any)

from stockmanager import (Item,
                          Items_Combination,
                          Combinations_manager)

from views.view import View
from selectfile import SelectionFile



# -- Mix/Max −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def search_last_indice_before_maxi(list_of_actions: list[Item], maxi: int=500):
    """ Loops in list_of_actions and adds action's prices.
        Returns last index before price > maxi """

    addition = 0
    for i, a in enumerate(list_of_actions):
        addition += a.f_price

        if addition > maxi:
            return i 

    return 0


# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Force brute", sf_bodies=['Selectionnez un fichier'])
# list_of_actions = select.select_file()
list_of_actions = select.select_file('essai.csv')

bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')

# -- view −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t0 = time()
my_view = View(header='Force brute', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

# -- Min / Max to reduce the combinations amount −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
max = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price))
min = search_last_indice_before_maxi(sorted(list_of_actions, key=lambda k: k.f_price, reverse=True))


nb_combinaisons = 0
best_of_the_best = []
best_combination = None

# -- Best combination ? −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# bodies.append('NORMAL')
# print(min)
# print(max)
# for i in range(min, max + 1):

#     for c in combinations(list_of_actions, i):
#         nb_combinaisons += 1
#         new_combination = Items_Combination(c)

#         if not best_combination or new_combination > best_combination:
#             best_combination = new_combination


# -- Best combination with threads ? −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append('THREAD')
# for i in range(max, min -1, -1):

#     cb = Combinations_manager(list_of_actions=list_of_actions, r=i, best_of_the_best=best_of_the_best)
#     cb.start()

l1 = list(range(min, max+1))
l2 = []
while l1:
    l2.append(l1.pop(int(len(l1)/2)))

for i in l2:
    cb = Combinations_manager(list_of_actions=list_of_actions, r=i, best_of_the_best=best_of_the_best)
    cb.start()


while threading.active_count() != 2:
    sleep(0.05)
    # print(threading.active_count())

best_of_the_best.sort(reverse=True)
best_combination = best_of_the_best[0]


# -- Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'{nb_combinaisons} combinations en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append("\n".join( str(i) for i in best_combination.items))

my_view.show()
