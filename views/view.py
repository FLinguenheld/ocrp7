from threading import Thread
import time
import os

from .frame import (Justification, Frame)


class View:
    """ Base to display a view in terminal. It will be formated with border (See Frame class)
        Use show() display bodies and _ask methods to close the frame """

    def __init__(self, header: str, bodies: list[str]):

        self.continue_exec = 0

        self.frame = Frame()
        self.title = header.upper()
        self.bodies = bodies
        self.loading = _Loading(view_instance=self)

    def show(self, ended: bool=True):
        """ Clear the terminal, print header and all bodies. Close the frame if ended=True """

        # Clear screen
        os.system("cls" if os.__name__ == "nt" else "clear")

        # Header
        self.frame.print_top()
        self.frame.print_text(self.title, Justification.CENTER)
        self.frame.print_line()
        self.frame.print_blank_line()

        # Bodies
        for b in self.bodies:
            self.frame.print_text(b, Justification.LEFT)
            self.frame.print_blank_line()

        if ended:
            self.frame.print_bottom()

    # Questions −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _ask_question(self, text: str):
        """ Finish the frame with a prompt. Return user's value without any check """

        self.frame.print_line()
        self.frame.print_text(text, Justification.LEFT)
        self.frame.print_bottom()

        # Print input then replace the cursor
        return input(f"\u001B[2A\u001B[{len(text) + self.frame.tab + 2}C> ")

    def _ask_confirmation(self, text: str="Confirmer ? (O/N)"):
        """ Finish the frame with a confirmation, return a bool """

        while True:
            match self._ask_question(text).upper():
                case "O":
                    return True
                case "N":
                    return False

    def key_to_continue(self):
        self._ask_question('Appuyez sur entrer pour continuer')

    # Loading −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def start_loading(self, text: str=""):
        """ Refresh the screen, display the bodies, close the frame then replace the cursor """

        self.show(ended=False)
        self.frame.print_line()
        self.frame.print_blank_line()
        self.frame.print_bottom()
        print("\033[3A")

        self.loading.text = text
        self.continue_exec = 1
        self.loading.start()

    def update_loading_text(self, txt: str):
        self.loading.text = txt

    def update_loading(self, percentage: int):
        self.loading.percentage = percentage

    def stop_loading(self):
        """ Stop the loading thread """
        self.loading.continue_exec = 0


class _Loading(Thread):
    """ Allows to display a loading in a thread
        Use start() to launch the thread. It will reprint the penultimate line with self.text and dots.
        Turn self.continue_exec to 0 to to stop """

    def __init__(self, view_instance):
        Thread.__init__(self)

        self.continue_exec = 0
        self.view_instance = view_instance  # To use the same frame object with view
        self.text = ""
        self.percentage = 0

    def run(self):
        self.continue_exec = 1
        while self.continue_exec == 1:

            self.view_instance.frame.print_progress(self.text, self.percentage)
            time.sleep(0.3)
