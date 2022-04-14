from multiprocessing import (Process, Manager)
from time import time
from time import sleep

from stockmanager import (Stock, StocksCombination)
from glutton import Glutton
from views.view import View
from selectfile import SelectionFile


MAX_AMOUNT = 500
# NB_LOOPS = 10000
NB_THREADS = 8
TIME_IN_SECONDS = 3

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Optimisation de l'algorithme", sf_bodies=['Selectionnez un fichier'])
# list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')
# list_of_actions = select.select_file('essai_24_actions.csv')
# list_of_actions = select.select_file('essai_25_actions.csv')
# list_of_actions = select.select_file('dataset1_Python+P7.csv')
list_of_actions = select.select_file('dataset2_Python+P7.csv')


# glouton = Glutton(g_max=MAX_AMOUNT, g_list=list_of_actions)
# best_combination = glouton.random_by_tries(NB_LOOPS)

# print(best_combination)


# −−−−−−−−−−−−−−−−−−−--−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- view −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}\n' \
              f'{len(list_of_actions)} actions\n' \
              f'{NB_THREADS} threads pendant {TIME_IN_SECONDS} secondes')


# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glutton random Thread per time −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def glutton_thread_time(list_actions, time_in_seconds, combinations, counters):
    glutton = Glutton(g_max=MAX_AMOUNT, g_list=list_actions)
    r = glutton.random_by_time(time_in_seconds=time_in_seconds)

    combinations.append(r[0])
    counters.append(r[1])

t0 = time()
my_view = View(header='Glutton random', bodies=bodies)
my_view.start_loading(text=f'En cours : {NB_THREADS} threads / {TIME_IN_SECONDS} s')

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Lauching threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
manager = Manager()
combinations = manager.list()
counters = manager.list()
threads = []

for i in range(0, NB_THREADS):
    p = Process(target=glutton_thread_time, args=(list_of_actions, TIME_IN_SECONDS, combinations, counters))
    threads.append(p)
    p.start()

# Progression
while time() - t0 < TIME_IN_SECONDS:
    sleep(0.5)
    my_view.update_loading(round(100 * (time() - t0) / TIME_IN_SECONDS))

for t in threads:
    t.join()

best_combination = StocksCombination.best_stock_in_list(combinations)
counter = sum(counters)

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append(f'{counter} combinaisons traitées en {time() - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_stocks())

my_view.stop_loading()
my_view.show()
