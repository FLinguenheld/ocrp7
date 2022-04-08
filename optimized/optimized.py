from time import time
from time import sleep


from stockmanager_opti import (Item,
                          ItemsCombination,
                          Glouton,
                          GloutonThread)

from views.view import View
from selectfile import SelectionFile



# MAX_AMOUNT = 6
# MAX_AMOUNT = 5
# MAX_AMOUNT = 15
MAX_AMOUNT = 500

# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Optimisation de l'algorithme", sf_bodies=['Selectionnez un fichier'], sf_multiplier=1)
# list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')
# list_of_actions = select.select_file('dataset1_Python+P7.csv')
list_of_actions = select.select_file('dataset2_Python+P7.csv')

bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')


# -−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glouton random −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t0 = time()
my_view = View(header='Glouton random', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
glouton = Glouton(g_max=MAX_AMOUNT, g_list=list_of_actions)

best_combination = ItemsCombination(max_amount=MAX_AMOUNT)
counter = 0
while counter < 10000:

    counter += 1
    new_combination = glouton.random()

    if new_combination > best_combination:
        best_combination = new_combination
# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

t1 = time()
my_view.stop_loading()

bodies.append(f'{counter} combinaisons traitées en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_items())
my_view.show()


# -−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glouton random Thread −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append(f'−− Threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−')

t0 = time()
my_view = View(header='Glouton random threads', bodies=bodies)
my_view.start_loading(text='Étude en cours ')

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
nb_threads = 4
counters = [x * 0 for x in range(0, nb_threads)]
combinations = [x * 0 for x in range(0, nb_threads)]
threads = []

for i in range(0, nb_threads):
    t = GloutonThread(g_max=MAX_AMOUNT, g_list=list_of_actions, results=combinations, id_thread=i, counter=counters)
    t.start()
    threads.append(t)

sleep(2)
for t in threads:
    t.stop = True

combinations.sort(reverse=True)
best_combination = combinations[0]

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'{len(counters)} threads - {counters}')
bodies.append(f'{sum(counters)} combinaisons traitées en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_items())

my_view.show()
