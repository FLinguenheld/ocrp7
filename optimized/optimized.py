from multiprocessing import (Process,
                             Manager)


from time import time
from time import sleep
from math import ceil


from stockmanager_opti import (Item,
                          ItemsCombination,
                          Glouton)

from views.view import View
from selectfile import SelectionFile

MAX_AMOUNT = 500
nb_loops = 100000
nb_threads = 8
time_in_seconds = 10


# -- File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Optimisation de l'algorithme", sf_bodies=['Selectionnez un fichier'], sf_multiplier=1)
# list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')
list_of_actions = select.select_file('dataset1_Python+P7.csv')
# list_of_actions = select.select_file('dataset2_Python+P7.csv')


bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}')

# -−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glouton random normal −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t0 = time()
my_view = View(header='Glouton random', bodies=bodies)
my_view.start_loading(text='Étude en cours ')


glouton = Glouton(g_max=MAX_AMOUNT, g_list=list_of_actions)
best_combination = glouton.random_by_tries(nb_loops)

t1 = time()
my_view.stop_loading()

bodies.append(f'{nb_loops} combinaisons traitées en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_items())
my_view.show()


# -−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glouton random Thread −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def glouton_thread(list_actions, nb_loops, combinations):
    glouton = Glouton(g_max=MAX_AMOUNT, g_list=list_actions)
    combinations.append(glouton.random_by_tries(nb_loops))


bodies.append(f'−− Threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−')

t0 = time()
my_view = View(header='Glouton random', bodies=bodies)
my_view.start_loading(text='Étude threads en cours ')

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
nb_loops_per_thread = nb_loops
# nb_loops_per_thread = int(nb_tries / nb_threads)

manager = Manager()
combinations = manager.list()
threads = []

for i in range(0, nb_threads):
    p = Process(target=glouton_thread, args=(list_of_actions, nb_loops_per_thread, combinations))
    threads.append(p)
    p.start()

for t in threads:
    t.join()

best_combination = max(combinations)

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'{nb_threads} threads : {nb_loops_per_thread * nb_threads} combinaisons traitées en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_items())
my_view.show()


# -−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# -- Glouton random Thread per time −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def glouton_thread_time(list_actions, time_in_seconds, combinations, counters):
    glouton = Glouton(g_max=MAX_AMOUNT, g_list=list_actions)
    r = glouton.random_by_time(time_in_seconds=time_in_seconds)

    combinations.append(r[0])
    counters.append(r[1])


bodies.append(f'−− Threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−')

t0 = time()
my_view = View(header='Glouton random', bodies=bodies)
my_view.start_loading(text='Étude threads en cours ')

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
manager = Manager()
combinations = manager.list()
counters = manager.list()
threads = []

for i in range(0, nb_threads):
    p = Process(target=glouton_thread_time, args=(list_of_actions, time_in_seconds, combinations, counters))
    threads.append(p)
    p.start()

for t in threads:
    t.join()

best_combination = max(combinations)
counter = sum(counters)

# --−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
t1 = time()
my_view.stop_loading()

bodies.append(f'{nb_threads} threads pendant {time_in_seconds} secondes\n{counter} combinaisons traitées en {t1 - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_items())
my_view.show()

