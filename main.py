"""This is the main menu"""
from data_manager import (
    wipe_file,
    create_csv,
    read_csv,
    add_days_until_birthday,
    turning_years,
    get_todays_celebrators,
    make_list_printable,
    print_person,
)
from settings import (
    settings_mode,
    create_settings_file,
    check_and_reset_if_new_year,
    BackFromSettings,
    is_auto_mode_on,
)
from congratulation_manager import congratulation_mode, BackFromCongratulations
from adding import add_contact, BackFromAdding
from edit_contacts import view_or_edit, BackFromEdit
from auto_mode import auto_congratulation_mode
import sys
import time
import threading

print("\n\nHELLO!\n")


def user_mode(
    settings_file: str,
    contacts_file: str,
    history_file: str,
    failed_recipients_file: str,
) -> None:
    while True:
        # create files if not yet created
        create_settings_file(settings_file)
        create_csv(contacts_file)

        # reset congratulation status, if new year
        check_and_reset_if_new_year(settings_file, contacts_file)

        # start auto mode if it's on in the settings
        if is_auto_mode_on(settings_file):
            auto_thread = threading.Thread(
                target=auto_congratulation_mode,
                args=(
                    contacts_file,
                    history_file,
                    failed_recipients_file,
                    settings_file,
                ),
            )
            auto_thread.start()

        try:
            contacts = read_csv(contacts_file)
            todays_celebrators = get_todays_celebrators(contacts, True)
            time.sleep(1.5)
            display_birthdays_today(todays_celebrators)
            print()
            display_upcoming_birthdays(contacts)

            while not (
                answer := input(
                    "Main Menu:\n\n"
                    "1. Congratulate Contact(s)\n"
                    "2. Add Contact(s)\n"
                    "3. View/ Edit/ Remove Contacts(s)\n"
                    "4. View History\n"
                    "5. View Failed Senders\n"
                    "6. Settings\n"
                    "7. Wipe all files\n"
                    "8. Exit\n\n"
                    "Option: "
                ).strip()
            ) or answer not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                print("Enter only '1', '2', '3', '4', '5', '6', '7', or '8'")

            if answer == "1":
                congratulation_mode(
                    contacts_file, history_file, failed_recipients_file, settings_file
                )
            elif answer == "2":
                add_contact(contacts_file)
            elif answer == "3":
                view_or_edit(contacts_file, failed_recipients_file)
            elif answer == "4":
                display_history(history_file)
            elif answer == "5":
                display_failed_senders(failed_recipients_file)
            elif answer == "6":
                settings_mode(
                    contacts_file, history_file, failed_recipients_file, settings_file
                )
            elif answer == "7":
                wipe_all_files(history_file, failed_recipients_file, contacts_file)
            elif answer == "8":
                sys.exit("Adios!")

        except (
            BackFromAdding,
            BackFromCongratulations,
            BackFromEdit,
            BackFromSettings,
        ):
            continue


def wipe_all_files(
    history_filepath: str, failed_senders_filepath: str, contacts: list[dict]
):
    while not (
        answer := input("Are you sure?:\n\n" "1. Yes\n" "2. No\n\n" "Option: ").strip()
    ) or answer not in ["1", "2"]:
        print("Enter only '1', '2'")

    if answer == "1":
        wipe_file(history_filepath)
        wipe_file(failed_senders_filepath)
        wipe_file(contacts)
        print("\nAll data from all files has been deleted!")

    else:
        pass


def display_history(history_filepath: str) -> None:
    try:
        people = read_csv(history_filepath)
    except ValueError:
        print("No emails have been sent yet!")
    else:
        print("\nHistory:")
        if people:
            for person in people:
                person["message"] = person["message"].replace("(new-line)", "\n")
            printable = make_list_printable(people)
            print_person(printable)
        else:
            print("No emails have been sent yet!")


def display_failed_senders(failed_senders_filepath: str) -> None:
    try:
        people = read_csv(failed_senders_filepath)
    except ValueError:
        print("No failed senders yet!")
    else:
        printable = make_list_printable(people)
        if not printable:
            print("\nNo failed senders yet!")
        else:
            print_person(printable)


def display_birthdays_today(todays_celebrators: list[dict]) -> None:
    """Prints today's celebrators if there are any + how old they are getting"""
    if todays_celebrators:
        printable_celebrators = "\n".join(
            f"{person.get('name', 'Somebody')} is turning {turning_years([person])} years old today. "
            f"{'Remember to congratulate!' if person.get('congratulated', 'False') == 'False' else 'Congratulations have been sent!'}"
            for person in todays_celebrators
        )
        print("\nTODAY:")
        print(printable_celebrators)


def display_upcoming_birthdays(contacts: list[dict]) -> None:
    people = contacts
    if people:
        add_days_until_birthday(people)
        upcoming_list = [
            person for person in people if person.get("days_until_birthday", 0) != 0
        ][:3]
        printable_upcoming_list = "\n".join(
            f"{person.get('name', 'Somebody')} will be turning {turning_years([person])} years old in {person['days_until_birthday']} day(s)."
            for person in upcoming_list
        )
        if upcoming_list:
            print("UPCOMING:")
            print(printable_upcoming_list, "\n")


if __name__ == "__main__":
    user_mode("settings.txt", "contacts.csv", "history.csv", "failed_recipients.csv")
