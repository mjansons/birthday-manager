"""this file manages view/ edit/ delete contacts mode"""
from data_manager import (
    read_csv,
    rewrite_csv,
    search_by_keyword,
    make_list_printable,
    print_person,
    edit_contact,
    delete_contact,
)
from data_validators import is_valid_birthday, is_valid_email
import re


class BackFromEdit(Exception):
    pass


class SearchAgain(Exception):
    pass


def view_or_edit(filepath: str, failed_sender_path: str) -> None:
    """This is the main loop for this mode"""

    while not (
        answer := input(
            "What do you want to do?\n\n"
            "1. View All Contacts\n"
            "2. Edit/Delete a Contact\n"
            "3. Return to Main Menu\n\n"
            "Option: "
        ).strip()
    ) or answer not in ["1", "2", "3"]:
        print("Enter only '1', '2', or '3'")

    # print all contacts
    if answer == "1":
        try:
            contacts = read_csv(filepath)
        except ValueError:
            print("You don't have any contacts!\n")
        else:
            printable_contacts = make_list_printable(contacts)
            print_person(printable_contacts)
            print("Look up!")
        raise BackFromEdit

    # run edit mode
    elif answer == "2":
        try:
            contacts = read_csv(filepath)
        except ValueError:
            print("You don't have any contacts!\n")
        else:
            run_edit_mode(filepath, contacts, failed_sender_path)
        raise BackFromEdit

    else:
        raise BackFromEdit


def run_edit_mode(filepath: str, contacts: list[dict], failed_sender_path: str) -> None:
    """This is the main function that offers user to edit a single contact"""
    while True:
        try:
            # get keyword and perform a search
            keyword = get_keyword(2)
            search_results = search_by_keyword(
                contacts, ["uid", "name", "email", "birthday", "about"], keyword
            )

            # if there are any results
            if search_results:
                # print them
                printable_list = make_list_printable(search_results)
                print_person(printable_list)

                # offer to edit
                offer_to_continue_to_edit()
                if len(search_results) > 1:
                    contact_to_edit = ask_which_contact_to_manipulate(search_results)
                else:
                    contact_to_edit = search_results

                # ask what to edit and then perform the edit
                while True:
                    print(
                        "\nWhat would you like to do?\n\n"
                        "1. Edit name\n"
                        "2. Edit birthday\n"
                        "3. Edit email\n"
                        "4. Edit about\n"
                        "5. Delete Contact\n"
                        "6. I'm done, return to Main Menu"
                    )
                    response = input("Option: ").strip()
                    # name
                    if response == "1":
                        edit_name(contact_to_edit)
                        continue
                    # if edit birthday
                    elif response == "2":
                        edit_birthday(contact_to_edit)
                        continue
                    # if edit email
                    elif response == "3":
                        edit_email(contact_to_edit, failed_sender_path)
                        continue
                    # if edit about
                    elif response == "4":
                        edit_about(contact_to_edit)
                        continue
                    # if delete contact
                    elif response == "5":
                        delete_person(filepath, contacts, contact_to_edit)
                        continue
                    # if exit
                    elif response == "6":
                        finish(filepath, contacts, contact_to_edit)
                    # in case option not in range of 1-6
                    else:
                        print("Invalid option selected")
                        continue

            # if there are no search results:
            else:
                print(
                    "\nNo contact matches your search term.\n"
                    "Do you want to try again?\n\n"
                    "1. Yes\n"
                    "2. No, return to Main Menu"
                )
                while True:
                    response = input("Option: ")
                    if response == "1":
                        raise SearchAgain
                    elif response == "2":
                        raise BackFromEdit
                    else:
                        print("Invalid option")
                        continue
        except SearchAgain:
            continue


def get_keyword(min_characters: int) -> str:
    """Prompt the user for a keyword"""
    while (keyword := str(input("Search for contact to edit: ").strip())) and len(
        keyword
    ) < min_characters:
        print("\nEnter at least 2 characters.")
    return keyword


def offer_to_continue_to_edit() -> None:
    """Ask the user what to do after the search"""
    print(
        "Found what you were looking for?\n\n"
        "1. Yes, let's continue\n"
        "2. Try another search term\n"
        "3. Return to Main Menu"
    )
    while True:
        response = input("Option: ").strip()
        if response == "1":
            break
        elif response == "2":
            print()
            raise SearchAgain
        elif response == "3":
            raise BackFromEdit
        else:
            print("Invalid option")
            continue


def ask_which_contact_to_manipulate(search_results: list[dict]) -> list[dict]:
    """ask which contact to tamper with if there is more than 1"""
    print("\nSelect the order number of the contact")
    while True:
        try:
            response = int(input("Nr.: ").strip())
            if response not in range(1, len(search_results) + 1):
                print("Invalid number selected")
                continue
            else:
                break
        except ValueError:
            print("Invalid number selected")
            continue
    contact_to_edit = [search_results[response - 1]]
    return contact_to_edit


def edit_name(contact_to_edit: list[dict]) -> None:
    while not (name := input("New name: ").strip()):
        print("Enter a name")
    edit_contact(contact_to_edit, "name", name)
    print("\nSuccess!")


def edit_birthday(contact_to_edit: list[dict]) -> None:
    while not (
        birthday := input("New birthday(yyyy/mm/dd): ").strip()
    ) or not is_valid_birthday(birthday):
        print("Enter a valid birthday")

    y, m, d = re.split(r"[-./]", birthday)
    formatted_birthday = f"{y}.{m.zfill(2)}.{d.zfill(2)}"

    edit_contact(contact_to_edit, "birthday", formatted_birthday)
    print("\nSuccess!")


def edit_email(
    contact_to_edit: list[dict], failed_senders_path: str = "optional_parameter.csv"
) -> None:
    while not (email := input("New email: ").strip()) or not is_valid_email(email):
        print("Enter a valid email")
    edit_contact(contact_to_edit, "email", email)

    # logic in case the user was in failed sender list before
    try:
        failed_list = read_csv(failed_senders_path)
        for contact in failed_list:
            if contact["uid"] == contact_to_edit[0]["uid"]:
                edit_contact(contact_to_edit, "congratulated", "False")
                delete_contact(failed_list, contact_to_edit)
                rewrite_csv(failed_senders_path, failed_list)
    except ValueError:
        pass

        # need to remove him now from failed sender list if he's there
    print("\nSuccess!")


def edit_about(contact_to_edit: list[dict]) -> None:
    about = input("New about: ").strip()
    edit_contact(contact_to_edit, "about", about)
    print("\nSuccess!")


def delete_person(
    filepath: str, contacts: list[dict], contact_to_edit: list[dict]
) -> None:
    while not (
        answer := input("\nAre you sure?\n1. Yes\n2. No\n\nOption: ").strip().casefold()
    ) or answer not in ["1", "2"]:
        print(f"Enter only '1' or '2'")
    if answer == "1":
        contacts = delete_contact(contacts, contact_to_edit)
        rewrite_csv(filepath, contacts)
        print("\nSuccess!")
        raise BackFromEdit


def finish(filepath: str, contacts: list[dict], contact_to_edit: list[dict]) -> None:
    rewrite_csv(filepath, contacts)
    print("\nFinal version:")
    edited_contact = make_list_printable(contact_to_edit)
    print_person(edited_contact)
    print("All changes have been saved!\n")
    raise BackFromEdit
