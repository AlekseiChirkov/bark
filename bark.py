import os
from typing import Callable, ClassVar, Union, Dict

import commands


class Option:
    """Interface to choose option from menu"""

    def __init__(self, name: str, command: ClassVar,
                 prep_call: Callable = None):
        """
        Initialize class attrs
        :param name: str -> name showing in menu
        :param command: ClassVar -> command name to execute
        :param prep_call: str -> preparation step before command execution
        """

        self.name = name
        self.command = command
        self.prep_call = prep_call

    def __str__(self):
        return self.name

    def choose(self) -> None:
        """
        Works after variant choice in menu
        :return: None
        """

        data = self.prep_call() if self.prep_call else None
        message = (
            self.command.execute(data) if data else self.command.execute()
        )
        print(message)


def print_options(options: dict) -> None:
    """
    Method prints options to execute
    :param options: dict -> options for execution
    :return: None
    """

    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")


def option_choice_is_valid(choice: str, options: dict) -> bool:
    """
    Method validates option choice
    :param choice: str -> chosen option key
    :param options: dict -> options choices dict
    :return: bool -> choice is valid or not
    """

    return choice.upper() in options.keys()


def get_options_choice(options: dict) -> ClassVar:
    """
    Method returns choice if it exists in options
    :param options: dict -> options choices dict
    :return: ClassVar -> existed option
    """

    choice = input("Choose option from list: ")
    while not option_choice_is_valid(choice, options):
        print("Choice doesn't exist, please select another one from the list.")
        print_options(options)
        choice = input("Choose option from list: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> Union[str, None]:
    """
    Method te get user input for bookmark label
    :param label: str -> bookmark field label
    :param required: bool -> label is required
    :return: str or None -> bookmark name on None
    """

    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_bookmark_data() -> Dict[str, str]:
    """
    Method returns result of user input validation.
    :return: dict -> bookmark validated fields
    """

    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_id_for_deletion() -> str:
    """
    Method returns bookmark ID to delete
    :return: str -> bookmark id
    """

    return get_user_input("Enter a bookmark ID to delete.")


def clear_screen() -> None:
    clear = 'cls' if os.name == 'nt' else 'cls'
    os.system(clear)


def loop() -> None:
    while True:
        clear_screen()
        print_options(OPTIONS)
        chosen_option = get_options_choice(OPTIONS)
        chosen_option.choose()
        _ = input("Please enter the key 'Enter' to go back to menu.")


OPTIONS = {
    "A": Option(
        "Add bookmark", commands.AddBookmarkCommand(),
        prep_call=get_new_bookmark_data
    ),
    "B": Option("Show bookmarks by date", commands.ListBookmarksCommand()),
    "T": Option("Show bookmarks by title", commands.ListBookmarksCommand(
        order_by='title'
    )),
    "D": Option(
        "Delete bookmark", commands.DeleteBookmarkCommand(),
        prep_call=get_bookmark_id_for_deletion
    ),
    "Q": Option("Quit", commands.QuitCommand()),
}

if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()
    loop()
