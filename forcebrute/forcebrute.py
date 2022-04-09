from time import time
from itertools import combinations

from stockmanager import (Item,
                          ItemsCombination)
                          # Combinations_manager)

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
list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')

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
best_combination = ItemsCombination([])

# -- Best combination ? −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append('NORMAL')
for i in range(min, max + 1):

    for c in combinations(list_of_actions, i):
        nb_combinaisons += 1
        new_combination = ItemsCombination(c)

        if not best_combination or new_combination > best_combination:
            best_combination = new_combination

# -- Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'{nb_combinaisons} combinations en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append("\n".join( str(i) for i in best_combination.items))

my_view.show()
