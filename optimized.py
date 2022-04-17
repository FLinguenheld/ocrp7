from multiprocessing import (Process, Manager)
from time import time
from time import sleep

from stockmanager import (Stock, StocksCombination)
from glutton import Glutton
from views.view import View
from views.form import (Form, FieldForm)
from selectfile import SelectionFile


MAX_AMOUNT = 500


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Glutton random Thread per time −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def glutton_thread_time(list_actions: list[Stock], time_in_seconds: int, combinations, counters):
    """ Glutton algorithm by time for threads. See class Glutton for more details.
        This function allows to use glutton with threads.
        Give two manager.list to 'combinations'and 'counters'
        These lists will be shared and filled by all threads.
        Once all threads finished, just sort or sum manager.lists """

    glutton = Glutton(g_max=MAX_AMOUNT, g_list=list_actions)
    r = glutton.random_by_time(time_in_seconds=time_in_seconds)

    combinations.append(r[0])
    counters.append(r[1])


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− File selection −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
select = SelectionFile(sf_header="Glutton random", sf_bodies=['Selectionnez un fichier'])
list_of_actions = select.select_file()
# list_of_actions = select.select_file('essai.csv')
# list_of_actions = select.select_file('essai_28_actions.csv')
# list_of_actions = select.select_file('dataset1_Python+P7.csv')
# list_of_actions = select.select_file('dataset2_Python+P7.csv')

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Form threads and time −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
settings=[FieldForm(f_name="Temps de traitement en secondes", f_type=int),
          FieldForm(f_name="Nombre de threads", f_type=int)]

form_settings = Form(header="Options glouton", fields=settings)
form_settings.show()

time_in_seconds = settings[0].f_value
nb_threads = settings[1].f_value


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− View −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
bodies = list()
bodies.append(f'Fichier : {select.sf_current_choice}\n'
              f'{len(list_of_actions)} actions\n'
              f'{nb_threads} threads pendant {time_in_seconds} secondes')

my_view = View(header='Glutton random', bodies=bodies)
my_view.start_loading(text='En cours')
t0 = time()

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Lauching threads −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−-−−−−−−−−−−−−−−−−−−−−−
manager = Manager()
combinations = manager.list()
counters = manager.list()
threads = []

for i in range(0, nb_threads):
    p = Process(target=glutton_thread_time, args=(list_of_actions, time_in_seconds, combinations, counters))
    threads.append(p)
    p.start()

# Progression
while time() - t0 < time_in_seconds:
    sleep(0.5)
    my_view.update_loading(round(100 * (time() - t0) / time_in_seconds))

for t in threads:
    t.join()

best_combination = StocksCombination.best_stock_in_list(combinations)
counter = sum(counters)

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# −− Displays results −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
bodies.append(f'{counter} combinaisons traitées en {time() - t0} secondes')
bodies.append(f'{best_combination}')
bodies.append(best_combination.sorted_stocks())

my_view.stop_loading()
my_view.show()
