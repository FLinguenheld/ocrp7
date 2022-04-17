from copy import deepcopy
from typing import (Any,
                    Optional,
                    List)
from dataclasses import dataclass
from .view import View


@dataclass
class FieldForm():
    """ Container to easily build a form in Menu class """
    f_name: str
    f_type: Any
    f_desc: Optional[str]=""
    f_value: Optional[Any]=None

    def __str__(self):
        return f"{self.f_name}" if self.f_value is None else f"{self.f_name} : {self.f_value}"

    def question_text(self):
        return f"{self.f_name} {self.f_desc}"

    def convert(self, value):
        return self.f_type(value)


class FieldFormList(FieldForm):
    """ Container to easily build a form in Menu class """
    def __init__(self, f_name: str,
                       f_type: Any,
                       f_choices: List[Any],
                       f_desc: Optional[str]="",
                       f_value: Optional[Any]=None):

        self.f_choices = f_choices
        super().__init__(f_name=f_name, f_desc=f_desc, f_type=f_type, f_value=f_value)

    def question_text(self):
        return f"{self.f_name} {self.f_desc} - {'/'.join(str(t) for t in self.f_choices)}"

    def convert(self, value):
        val = super().convert(value)

        if val in self.f_choices:
            return val
        else:
            raise ValueError


class Form(View):
    """ Based on View, allows to display bodies and all fields.
        Ask user to fill each field and ask a confirmation """

    def __init__(self, header: str, fields: List[FieldForm], bodies: List[str]=[]):
        self.fields = fields
        self.bodies_base = bodies

        super().__init__(header=header, bodies=bodies)

    def _update_bodies(self):
        """ Build the bodies with saved bodies, add the Form and overwrite it then refresh screen """

        new_bodies = deepcopy(list(self.bodies_base))
        new_bodies += ["\n".join(str(f) for f in self.fields)]
        self.bodies = new_bodies

        super().show(ended=False)

    def show(self):
        """ Show the form and ask to user field by field to fill it """

        while True:                 # Wait confirmation

            for field in self.fields:

                while True:         # Wait valid value
                    try:
                        self._update_bodies()
                        field.f_value = field.convert(self._ask_question(field.question_text()))
                        break

                    except KeyboardInterrupt:
                        break
                    except ValueError:
                        continue

            self._update_bodies()
            if self._ask_confirmation():
                break
