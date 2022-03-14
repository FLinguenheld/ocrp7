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

# MAX_AMOUNT = 6
# MAX_AMOUNT = 5
# MAX_AMOUNT = 15
MAX_AMOUNT = 500

# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Optimisation de l'algorithme", sf_bodies=['Selectionnez un fichier'])
list_of_actions = select.select_file()
# list_of_actions = select.select_file('essaivideo.csv')
# list_of_actions = select.select_file('essaisimple.csv')
# list_of_actions = select.select_file('essaiwiki.csv')
# list_of_actions = select.select_file('essai.csv')

bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')

# -- view −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t0 = time()
my_view = View(header='Force brute', bodies=bodies)
# my_view.start_loading(text='Étude en cours ')

# list_of_actions.sort(key=lambda x: x.f_price)
# list_of_actions.sort(key=lambda x: x.f_price, reverse=True)


matrice = [[0 for x in range(MAX_AMOUNT + 1)] for a in range(len(list_of_actions) + 1)]


for line in range(1, len(list_of_actions) +1):

    for column in range(1, MAX_AMOUNT + 1):

        price_current_line = list_of_actions[line-1].f_price
        profit_current_line = list_of_actions[line -1].f_profit

        # L'index est le prix en cours (la colonne) moins le prix de la ligne en cours
        index = column - price_current_line
        if index < 0:
            index = 0

        # Calcule le meilleur profit : ligne en cours plus profit de la case 'index' de la ligne précédente
        temp_profit = profit_current_line + matrice[line-1][index]

        if column >= price_current_line:
            matrice[line][column] = max(matrice[line-1][column], temp_profit)
        else:
            matrice[line][column] = matrice[line-1][column]


prix = MAX_AMOUNT
n = len(list_of_actions)
elements = [] 

while prix >= 0 and n >= 0:

    e = list_of_actions[n-1]
    # print(e)

    print(f"{matrice[n][prix]} == {matrice[n-1][prix-e.f_price] + e.f_profit} −−−−−−− {prix}")

    if matrice[n][prix] == matrice[n-1][prix-e.f_price] + e.f_profit:
        elements.append(e)
        prix -= e.f_price

    n -=1

print(Items_Combination(elements))
for i in elements:
    print(i)



# print(matrice)

# -- Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'traité en {t1 - t0} secondes')
# bodies.append(f'{best_combination}')

# my_view.show()
