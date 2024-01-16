"""This file contains code to add new contacts"""
from dataclasses import dataclass
import re
import time
from validators import is_valid_birthday, is_valid_email
from data_manager import (
    append_csv,
    read_csv,
    get_duplicates,
    make_list_printable,
    print_person,
)


class BackFromAdding(Exception):
    pass


@dataclass
class Person:
    def __init__(
        self,
        name: str,
        birthday: str,
        email: str,
        about: str = None,
        congratulated: bool = False,
    ) -> None:
        self._uid = None
        self.name = name
        self.birthday = birthday
        self.email = email
        self._about = about
        self._congratulated = False

    def key_value_pairs(self) -> list[dict]:
        return [
            {
                "uid": self.uid,
                "name": self.name,
                "birthday": self.birthday,
                "email": self.email,
                "about": self.about,
                "congratulated": self.congratulated,
            }
        ]
    
    @classmethod
    def format_birthday(cls, birthday) -> str:
        y, m, d = re.split(r"[-./]", birthday)
        formatted_birthday = f"{y}.{m.zfill(2)}.{d.zfill(2)}"
        return formatted_birthday
    
    @classmethod
    def get_data(cls, listdict) -> object:
        while not (name := input("Full name: ").strip()):
            print("Enter a name")

        # check if there are duplicate contacts with the same name in the file, if the file exists.
        if duplicates := get_duplicates(listdict, "name", name):
            formatted_list = make_list_printable(duplicates)
            print_person(formatted_list)
            print(
                "\nThe above contact(s), with the entered name already exist(s), would you like to add another one?\n\n1. Yes\n2. No\n"
            )
            while True:
                option = input("Option: ")
                if option == "1":
                    break
                elif option == "2":
                    raise BackFromAdding
                else:
                    print("Invalid option selected")
                    continue

        # get birthday
        while not (
            birthday := input("Birthday(yyyy/mm/dd): ").strip()
        ) or not is_valid_birthday(birthday):
            print("Enter a valid birthday")
        birthday = cls.format_birthday(birthday)

        # get email
        while not (email := input("Email: ").strip()) or not is_valid_email(email):
            print("Enter a valid email")
            
        # get about
        about = input("About: ").strip()

        return cls(name=name, birthday=birthday, email=email, about=about)

    @property
    def uid(self):
        if self._uid is None:
            self._uid = int(time.time_ns() / 10000)
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def birthday(self) -> str:
        return self._birthday

    @property
    def email(self) -> str:
        return self._email

    @property
    def about(self) -> str:
        return self._about

    @property
    def congratulated(self) -> str:
        return self._congratulated

    @uid.setter
    def uid(self, smth) -> None:
        raise ValueError("Unique ID can't be changed.")

    @name.setter
    def name(self, name: str) -> None:
        if not name:
            raise ValueError("No name added")
        self._name = name

    @birthday.setter
    def birthday(self, birthday: str) -> None:
        if not is_valid_birthday(birthday) or not birthday:
            raise ValueError("Invalid Birthday")
        birthday = Person.format_birthday(birthday)
    
        self._birthday = birthday

    @email.setter
    def email(self, email: str) -> None:
        if not is_valid_email(email) or not email:
            raise ValueError("Invalid email")
        self._email = email

    @about.setter
    def about(self, about) -> None:
        if not about:
            self._about = None
        else:
            self._about = about

    @congratulated.setter
    def congratulated(self, smth) -> None:
        raise ValueError("Congratuation status can't be manually changed.")


def add_contact(filepath):
    while True:
        try:
            listdict = read_csv(filepath)
        except ValueError:
            listdict = []
        contact = Person.get_data(listdict)
        append_csv(filepath, contact.key_value_pairs())
        print("\nSuccess!\n")
        while True:
            print("1. Add another one.\n2. Back to Main Menu\n")
            response = input("Option: ")
            if response == "1":
                break
            elif response == "2":
                raise BackFromAdding
            else:
                print("Invalid option")
                continue


if __name__ == "__main__":
    add_contact("contacts.csv")