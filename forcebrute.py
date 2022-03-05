from time import time
from itertools import combinations


from stockmanager import (Item,
                          Items_Combination,
                          Combinations_manager)

from views.view import View
from selectfile import SelectionFile

a = 0
if a => a:
    print(1)

if a == a:
    print(2)

# ==========>
# --------->


select = SelectionFile(sf_header="Force brute", sf_bodies=['Selectionnez un fichier'])
# list_of_actions = select.select_file()
list_of_actions = select.select_file(True)

bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')

list_of_actions.sort(key=lambda k: k.f_price)

# for i, a in enumerate(list_of_actions):


# Create combinations then keep only the best --
t0 = time()
number_of_combinations = 0

my_view = View(header='Force brute', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

my_comb_manager = Combinations_manager(number_of_results=1)
best_combination = None
for i in range(1, len(list_of_actions) + 1):
# for i in range(9, 1):

    for c in combinations(list_of_actions, i):
        number_of_combinations += 1
        new_combination = Items_Combination(c)

        if not best_combination or new_combination > best_combination:
            best_combination = new_combination
t1 = time()
my_view.stop_loading()


bodies.append(f'{number_of_combinations} combinations en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
# bodies.append("\n".join( str(i) for i in best_combination.items))

my_view.show()
