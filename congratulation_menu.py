"""this file manages congratulation sending"""

from data_manager import (
    create_csv,
    append_csv,
    read_csv,
    get_todays_celebrators,
    make_list_printable,
    print_person,
    edit_specific_contact,
    rewrite_csv,
    delete_contact,
    append_history_csv,
    load_settings,
    switch_api_working,
    save_settings
)
from edit_menu import ask_which_contact_to_manipulate
from ai_manager import MessageMaker
from email_manager import send_mail
from ai_manager import WriteManual
from email_manager import WrongEmail


class BackFromCongratulations(Exception):
    pass


def regular_congratulation_mode(contact_file_path, history_file_path, failed_senders, settings_filepath):
    """the main function for congratulations"""
    create_csv(history_file_path)
    try:
        contacts = read_csv(contact_file_path)
    except ValueError:
        contacts = []

    todays_celebrators = get_todays_celebrators(contacts, False)

    while len(todays_celebrators) > 0:
        # select who to congratulate if there is more than 1
        if len(todays_celebrators) > 1:
            preview = make_list_printable(todays_celebrators)
            print("\nPeople to be congratulated today:")
            print_person(preview)
            contact_to_congratulate = ask_which_contact_to_manipulate(
                todays_celebrators
            )
        else:
            preview = make_list_printable(todays_celebrators)
            print("\nPeople to be congratulated today:")
            print_person(preview)
            contact_to_congratulate = todays_celebrators

        # decide on AI or Manual congratulation mode
        answer = decide_how_to_write_message()

        # AI
        if answer == "1":
            # generate congratulation message
            try:
                global_history = read_csv(history_file_path)
            except ValueError:
                global_history = []
            bot = MessageMaker(contact_to_congratulate, global_history)
            try:
                message = bot.get_prompt()
            except WriteManual as e:
                print(e)
                print("Entering manual mode...")
                subject, message = write_myself(contact_to_congratulate)
                break

            # update settings in case API wasn't working before
            settings = load_settings(settings_filepath)
            if settings["api_is_working"] == "False":
                switch_api_working(settings)
            save_settings(settings_filepath, settings)

            # preview
            print("\nThis is how your email will look:")
            print(f"\nTo: {contact_to_congratulate[0]['email']}")
            print("Subject: Happy Birthday!")
            print(message, "\n")

            # confirmation
            while True:
                answer = ask_ai_message_confirmation()
                # Ready to send
                if answer == "1":
                    subject = "Happy Birthday!"
                    break

                # ask AI to regenerate
                elif answer == "2":
                    corrections = input("\nSuggestions for improvement: ")
                    message = bot.re_prompt(corrections)

                    # preview
                    print(f"\nTo: {contact_to_congratulate[0]['email']}")
                    print("Subject: Happy Birthday!")
                    print(message, "\n")
                    continue

                # Write myself
                elif answer == "3":
                    print()
                    subject, message = write_myself(contact_to_congratulate)
                    break

                elif answer == "4":
                    raise BackFromCongratulations

        # custom
        elif answer == "2":
            subject, message = write_myself(contact_to_congratulate)
        try:
            send_mail(contact_to_congratulate, message, subject)
            print("\nSuccess!\n")
        except WrongEmail as e:
            print(e)
            append_csv(failed_senders, contact_to_congratulate)
            edit_specific_contact(
                contacts, contact_to_congratulate, "congratulated", "True"
            )
            rewrite_csv(contact_file_path, contacts)
            todays_celebrators = delete_contact(
                todays_celebrators, contact_to_congratulate
            )

        else:
            append_history_csv(
                history_file_path, contact_to_congratulate, subject, message
            )
            edit_specific_contact(
                contacts, contact_to_congratulate, "congratulated", "True"
            )
            rewrite_csv(contact_file_path, contacts)
            todays_celebrators = delete_contact(
                todays_celebrators, contact_to_congratulate
            )

    print("Nobody needs to be congratulated, come back another day!")
    raise BackFromCongratulations


def write_myself(contact_to_congratulate: list[dict]) -> tuple[str, str]:
    """function that prompts user to conduct his/her own congratulation message"""
    while True:
        subject = input("Subject: ")
        lines = []
        print("Body (type 'DONE' on a new line to finish):")
        while True:
            line = input()
            if line.strip().upper() == "DONE":
                break
            lines.append(line)
        message = "\n".join(lines)

        # preview
        print("\nThis is how your email will look:")
        print(f"\nTo: {contact_to_congratulate[0]['email']}")
        print(f"Subject: {subject}")
        print(f"{message}\n")

        answer = ask_reg_message_confirmation()
        # yes
        if answer == "1":
            break
        # try again
        if answer == "2":
            print()
            continue
        # Exit
        if answer == "3":
            raise BackFromCongratulations

    return subject, message


def ask_ai_message_confirmation() -> str:
    while not (
        answer := input(
            "Ready to send?\n\n"
            "1. Yes\n"
            "2. No, generate another option\n"
            "3. I want to write myself\n"
            "4. Exit to main menu\n\n"
            "Option: "
        )
        .strip()
        .casefold()
    ) or answer not in ["1", "2", "3", "4"]:
        print("Enter only '1' or '2', or '3', or '4'")
    return answer


def ask_reg_message_confirmation() -> str:
    while not (
        answer := input(
            "Ready to send?\n\n"
            "1. Yes\n"
            "2. No, I want to try again\n"
            "3. Exit to main menu\n\n"
            "Option: "
        )
        .strip()
        .casefold()
    ) or answer not in ["1", "2", "3"]:
        print("Enter only '1' or '2', or '3'")
    return answer


def decide_how_to_write_message() -> str:
    while not (
        answer := input(
            "\nDo you want AI to generate a message for you?\n\n"
            "1. Yes\n"
            "2. No\n\n"
            "Option: "
        )
        .strip()
        .casefold()
    ) or answer not in ["1", "2"]:
        print("Enter only '1' or '2'")
    return answer
