from typing import (Optional,
                    List,
                    Any)

from dataclasses import dataclass
from .view import View


@dataclass
class FieldMenu:
    """ Container to easily build a menu in Menu class """

    f_text: Optional[str]=""
    f_value: Optional[str]=None
    f_object: Optional[Any]=None

    def __str__(self):
        if self.f_value is not None:
            return f"{self.f_value} : {self.f_text}"
        else:
            return f"{self.f_text}"


class Menu(View):
    """ Based on View, allow to display bodies and a list of choices.
        Forces user to choice in the list """

    def __init__(self, header: str, choices: List[FieldMenu], bodies: List[str]=[]):

        self.choices = choices
        new_bodies = list(bodies)
        new_bodies += ["\n".join(str(t) for t in choices)]

        super().__init__(header=header, bodies=new_bodies)

    def show(self):
        """ Displays the form, waits and checks the user's awnser.
            Loops if choice doesn't exist and return :
                - the object of selected value
                - the value if objet is None """

        while True:
            try:
                # Show without closing the frame
                super().show(ended=False)

                # Ask question and check choice
                choice = self._ask_question("Selection")

                for elem in self.choices:
                    if elem.f_value == choice:
                        return elem.f_object if elem.f_object is not None else choice

            except KeyboardInterrupt:
                break
