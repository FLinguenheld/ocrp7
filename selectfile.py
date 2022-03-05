from dataclasses import dataclass
from pathlib import Path
from csv import DictReader

from typing import(Any,
                   Optional,
                   List)

from views.menu import (Menu,
                        FieldMenu)

from stockmanager import (Item)


@dataclass
class SelectionFile:

    sf_header: str
    sf_bodies: Optional[list[str]]
    sf_path: Path=Path(str(Path.cwd()) + '/fichiers')
    sf_current_choice: Optional[str]=""


    def select_file(self, force_to_test: bool=False):

        if not force_to_test:

            fields = []
            for i, p in enumerate(self.sf_path.iterdir()):
                fields.append(FieldMenu(f_text=p.name, f_value=str(i), f_object=p))

            my_menu = Menu(header=self.sf_header, choices=fields, bodies=['Selectionnez un fichier à analyser'])
            self.sf_current_choice = my_menu.show()
        else:
            self.sf_current_choice = str(self.sf_path / 'essai.csv')

        # Read the file --
        list_of_actions = []
        with open(self.sf_current_choice) as file:
            csv_dict = DictReader(file, delimiter=',')

            for r in csv_dict:
                list_of_actions.append(Item(f_name=r['Name'], f_price=int(r['Price']), f_profit=int(r['Profit'])))

            return list_of_actions
