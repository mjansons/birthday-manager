"""All file manipulation functions are here"""
import os
import csv
import re
from datetime import datetime
from validators import is_birthday_today


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


def append_csv(filepath: str, data: list[dict]) -> None:
    file_is_empty = False
    if os.path.exists(filepath):
        file_is_empty = open(filepath).readline() == ""

    with open(filepath, "a", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file_is_empty or not os.path.exists(filepath):
            writer.writeheader()
        writer.writerows(data)


def append_history_csv(filepath: str, data: list[dict], subject: str, message: str) -> None:
    the_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = message.replace("\n", "(new-line)")

    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["uid", "name", "email", "date_sent", "subject", "message"])
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


def make_list_printable(the_list) -> list:
    format_person = lambda p: f"{'\n'.join([f'{k}: {v}' for k, v in p.items()])}"
    strings = [format_person(person) for person in the_list]
    return strings


def print_person(file: list) -> None:
    """print list items in a numbered sequence"""
    print()
    for index, person in enumerate(file):
        print(f"Nr. {index + 1}")
        print(person, "\n")


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

    if (today_date.month, today_date.day) < (birthday_date.month, birthday_date.day):
        # Birthday is yet to come this year
        return today_date.year - birthday_date.year
    else:
        # Birthday has already occurred this year
        return today_date.year - birthday_date.year + 1


def get_todays_celebrators(contacts: list[dict], congr: bool = True) -> list[dict]:
    """return today's celebrators"""
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


if __name__ == "__main__":
    list_of_dicts = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Alice", "age": 25, "city": "San Francisco"},
        {"name": "Bob", "age": 35, "city": "Los Angeles"},
    ]

    edit_contact(list_of_dicts, "name", "Peter")
    print(list_of_dicts)
