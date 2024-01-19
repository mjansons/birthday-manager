"""All file manipulation functions are here, searches and formatting for printing"""

import os
import csv
import re
from datetime import datetime


def create_csv(filepath: str) -> None:
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8"):
            pass


def wipe_file(filepath: str) -> None:
    with open(filepath, "w", newline="", encoding="utf-8"):
        pass


def read_csv(filepath: str) -> list[dict]:
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    else:
        raise ValueError("The file does not exist.")


def rewrite_csv(filepath: str, data: list[dict]) -> None:
    if data:
        fieldnames = data[0].keys()
        with open(filepath, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    if not data:
        with open(filepath, "w", newline="") as file:
            writer = csv.DictWriter(file)
            writer.writerows(data)


def append_csv(filepath: str, data: list[dict]) -> None:
    file_is_empty = not os.path.exists(filepath) or open(filepath).readline() == ""

    with open(filepath, "a", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file_is_empty:
            writer.writeheader()
        writer.writerows(data)


def append_history_csv(filepath: str, data: list[dict], subject: str, message: str) -> None:
    the_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = message.replace("\n", "(new-line)")

    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["uid", "name", "email", "date_sent", "subject", "message"]
        )
        # only create headers if the file is empty.
        if os.path.getsize(filepath) == 0:
            writer.writeheader()
        writer.writerow(
            {
                "uid": data[0]["uid"],
                "name": data[0]["name"],
                "email": data[0]["email"],
                "date_sent": the_time,
                "subject": subject,
                "message": message,
            }
        )


def edit_contact(contacts: list[dict], key: str, new_value: str) -> list[dict]:
    """update key for all contacts in the list provided list"""
    for person in contacts:
        person[key] = new_value
    return contacts


def edit_specific_contact(full_list: list[dict], my_contact: list[dict], key: str, new_value: str) -> list[dict]:
    """update key for a selected contact in the list"""
    for person in full_list:
        if person["uid"] == my_contact[0]["uid"]:
            person[key] = new_value
    return full_list


def delete_contact(all_contacts: list[dict], removable_contact_list: list[dict]) -> list[dict]:
    removable_contacts_uids = [contact["uid"] for contact in removable_contact_list]
    return [d for d in all_contacts if d["uid"] not in removable_contacts_uids]

# searching in list related functions
def get_duplicates(listdict: list[dict], key: str, value: str) -> list[str]:
    """search contacts using one dict key vs exact match"""
    duplicates = [person for person in listdict if person.get(key) == value]

    return duplicates


def search_by_keyword(listdict: list[dict], search_keys: list[str], keyword: str) -> list[str]:
    """search contacts using many dict keys with regex"""

    escaped_keyword = re.escape(keyword)

    pattern = re.compile(rf".*?{escaped_keyword}.*?", re.IGNORECASE)
    matches = []
    for person in listdict:
        for key in search_keys:
            if pattern.match(str(person.get(key))):
                matches.append(person)
                break
    return matches


# formatting list for printing functions
def make_list_printable(the_list) -> list:
    format_person = lambda p: "\n".join([f"{k}: {v}" for k, v in p.items()])
    strings = [format_person(person) for person in the_list]
    return strings


def print_person(file: list) -> None:
    """print list items in a numbered sequence"""
    print()
    for index, person in enumerate(file):
        print(f"Nr. {index + 1}")
        print(person, "\n")

# birthdate related functions
def add_days_until_birthday(contacts: list[dict]) -> list[dict]:
    """returns a new sorted list with days until birthday"""

    today_date = datetime.now().date()

    for person in contacts:
        birthday = person["birthday"]
        birthday_date = datetime.strptime(birthday, "%Y.%m.%d").date()
        birthday_this_year = datetime(
            today_date.year, birthday_date.month, birthday_date.day
        ).date()

        # Check if the birthday has already occurred this year
        if today_date > birthday_this_year:
            next_year_birthday_date = datetime(
                today_date.year + 1, birthday_date.month, birthday_date.day
            ).date()
        else:
            next_year_birthday_date = birthday_this_year

        # Calculate the number of days until the next birthday
        days_until_birthday = (next_year_birthday_date - today_date).days

        # Add a new key-value pair to each person
        person["days_until_birthday"] = days_until_birthday

    # Sort the people by the number of days until their next birthday
    contacts.sort(key=lambda person: person["days_until_birthday"])

    return contacts


def turning_years(person: list[dict]) -> int:
    birthday = person[0]["birthday"]
    birthday_date = datetime.strptime(birthday, "%Y.%m.%d").date()
    today_date = datetime.now().date()
    return today_date.year - birthday_date.year


def get_todays_celebrators(contacts: list[dict], congr: bool = True) -> list[dict]:
    from data_validators import is_birthday_today
    # include everyone
    if congr == True:
        todays_celebrators = [
            person for person in contacts if is_birthday_today([person])
        ]
    # exclude the ones who have been congratulated already
    elif congr == False:
        todays_celebrators = [
            person
            for person in contacts
            if is_birthday_today([person]) and person["congratulated"] == "False"
        ]
    return todays_celebrators

# more settings related functions that deal with txt files
def create_settings_file(filepath: str) -> None:
    if not os.path.exists(filepath):
        default_settings = {
            "auto_mode_on": False,
            "api_is_working": True,
            "last_reset_date": datetime.now().date().strftime("%Y-%m-%d"),
        }
        with open(filepath, "w") as file:
            for key, value in default_settings.items():
                file.write(f"{key}={value}\n")


def load_settings(filepath: str) -> dict:
    if not os.path.exists(filepath):
        create_settings_file(filepath)
    with open(filepath, "r") as file:
        lines = file.readlines()
    settings = {
        line.split("=")[0]: line.split("=")[1].strip() for line in lines if "=" in line
    }
    return settings


def save_settings(filepath: str, settings: dict) -> None:
    with open(filepath, "w") as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")


def switch_auto_mode(settings: dict) -> None:
    if settings["auto_mode_on"] == "False":
        settings["auto_mode_on"] = True
    elif settings["auto_mode_on"] == "True":
        settings["auto_mode_on"] = False
    return settings


def switch_api_working(settings: dict) -> dict:
    if settings["api_is_working"] == "False":
        settings["api_is_working"] = True
    elif settings["api_is_working"] == "True":
        settings["api_is_working"] = False
    return settings


def update_last_reset_date(settings: dict) -> None:
    today = datetime.now().date()
    settings["last_reset_date"] = today.strftime("%Y-%m-%d")


def check_and_reset_if_new_year(setting_filepath: str, all_contacts_filepath: str) -> None:
    from data_validators import is_new_year
    settings = load_settings(setting_filepath)
    if is_new_year(settings["last_reset_date"]):
        try:
            all_contacts = read_csv(all_contacts_filepath)
            new_list = edit_contact(all_contacts, "congratulated", "False")
            rewrite_csv(all_contacts_filepath, new_list)
        except ValueError:
            pass

        update_last_reset_date(settings)
        save_settings(setting_filepath, settings)