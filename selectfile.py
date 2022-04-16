from dataclasses import dataclass
from pathlib import Path
from csv import DictReader
from typing import(Optional,
                   Any)

from views.menu import (Menu, FieldMenu)
from stockmanager import (Stock)


@dataclass
class SelectionFile:
    """ Displays a form to select a csv file in ./fichiers/
        Once selected, loops in the file to create Stock objects and fills a list.
        csv file has to have three columns : name, price, profit
        prices and profits are convert in float. Invalidated values are ignored.
        """

    sf_header: str
    sf_bodies: Optional[list[str]]
    sf_path: Path=Path(str(Path.cwd()) + '/fichiers')
    sf_current_choice: Any=""

    def select_file(self, force_to_test: str=''):
        """ Creates displays the form, then fills and returns the list of actions
            You can skip the form by forcing, just fills in the csv file's name """

        if not force_to_test:
            fields = []
            for i, p in enumerate(self.sf_path.iterdir()):
                fields.append(FieldMenu(f_text=p.name, f_value=str(i), f_object=p))

            my_menu = Menu(header=self.sf_header, choices=fields, bodies=['Selectionnez un fichier à analyser'])
            self.sf_current_choice = my_menu.show()
        else:
            self.sf_current_choice = str(self.sf_path / force_to_test)

        # Reading the file --
        list_of_actions = []
        with open(self.sf_current_choice) as file:
            csv_dict = DictReader(file, delimiter=',')

            for r in csv_dict:

                price = float(r['price'])
                profit = float(r['profit'])

                if price > 0 and profit > 0:
                    list_of_actions.append(Stock(f_name=r['name'],
                                                 f_price = price,
                                                 f_profit = profit))

        return list_of_actions
