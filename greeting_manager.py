from data_manager import create_csv, read_csv, get_todays_celebrators, make_list_printable, print_person, edit_specific_contact, rewrite_csv, delete_contact, append_history_csv
from edit_contacts import ask_which_contact_to_manipulate
from ai_manager import MessageMaker
from email_manager import send_mail

class BackToMain(Exception):
    pass

def main(contact_file_path, history_file_path):
    # need to remember to only offer this feature if there is anyone to be congratulated!!!!!!!!
    # this check should probably happen in the main file

    create_csv(history_file_path)
    contacts = read_csv(contact_file_path)
    todays_celebrators = get_todays_celebrators(contacts, False)
    
    while len(todays_celebrators) > 0:

        # select who to congratulate if there is more than 1
        if len(todays_celebrators) > 1:
            preview = make_list_printable(todays_celebrators)
            print("\nPeople to be congratulated today:")
            print_person(preview)
            contact_to_congratulate = ask_which_contact_to_manipulate(todays_celebrators)
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
            global_history = read_csv(history_file_path)
            bot = MessageMaker(contact_to_congratulate, global_history)
            message = bot.get_prompt()

            # preview
            print("\nThis is how your email will look:")
            print(f"\nTo: {contact_to_congratulate[0]["email"]}")
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
                    print(f"\nTo: {contact_to_congratulate[0]["email"]}")
                    print("Subject: Happy Birthday!")
                    print(message, "\n")
                    continue

                # Write myself
                elif answer == "3":
                    print()
                    subject, message = write_myself(contact_to_congratulate)
                    break

                elif answer == "4":
                    raise BackToMain
    
        # custom    
        elif answer == "2":
            subject, message = write_myself(contact_to_congratulate)

        send_mail(contact_to_congratulate, message, subject)
        append_history_csv(history_file_path, contact_to_congratulate, subject, message)
        edit_specific_contact(contacts, contact_to_congratulate, "congratulated", "True")
        rewrite_csv(contact_file_path, contacts)
        todays_celebrators = delete_contact(todays_celebrators, contact_to_congratulate)


def write_myself(contact_to_congratulate: list[dict]) -> tuple[str, str]:
    while True:
        subject = input("Subject: ")
        lines = []
        print("Body (type 'DONE' on a new line to finish):")
        while True:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            lines.append(line)
        message = '\n'.join(lines)
        
        # preview
        print("\nThis is how your email will look:")
        print(f"\nTo: {contact_to_congratulate[0]["email"]}")
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
            raise BackToMain

    return subject, message


def ask_ai_message_confirmation():
    while not (
        answer := input(
            "Ready to send?\n\n"
            "1. Yes\n"
            "2. No, generate another option\n"
            "3. I want to write myself\n"
            "4. Exit to main menu\n"
            "Answer: "
        ).strip().casefold()
) or answer not in ["1", "2", "3", "4"]:
        print("Enter only '1' or '2', or '3', or '4'")
    return answer


def ask_reg_message_confirmation():
    while not (
    answer := input(
        "Ready to send?\n\n"
        "1. Yes\n"
        "2. No, I want to try again\n"
        "3. Exit to main menu\n"
        "Answer: "
    ).strip().casefold()
) or answer not in ["1", "2", "3"]:
        print("Enter only '1' or '2', or '3'")
    return answer


def decide_how_to_write_message() -> str:
    while not (
        answer := input(
            "\nDo you want AI to generate a message for you?\n"
            "1. Yes\n"
            "2. No\nAnswer: "
        ).strip().casefold()
    ) or answer not in ["1", "2"]:
        print("Enter only '1' or '2'")
    return answer



        # if ai then promt ai while 
            # generate message
            # add to temporary history # this is done in the class
            # then ask for confirmation, 
                # if yes
                    # edit temporary history
                    # send it
                    # update history
                    # update contacts with congratulated == "True"
                    # restart
                # if no 
                    # ask ai to regenerate
                # if exit
                    # return to main

        # if custom, then just ask to type it while answer is no
            # then ask for confirmation, 
                # if yes
                    # send it
                    # update history
                    # update contacts with congratulated == "True"
                    # restart
                # if no 
                    # can retype
                # If Exit 
                    # return to main
        





# I had an idea to make congratulator a class?
    # what would it store then?
    # what would be it's methods?
    # why?

# in case I want a different method for congratulating?
        # maybe I can just get by with dependency injections with functions?
# then need to select one

# then need a method for doing it



if __name__ == "__main__":
    main("contacts.csv", "history.csv")








# people = [
#     {"uid": "1704663936754301","name": "Gints","birthday": "1993.05.12", "email": "gints@gmail.com", "about": "smth", "congratulated": "False"},
#     {"uid": "1703432132435901","name": "Juris","birthday": "1992.03.12", "email": "bd@gmail.com", "about": "smth", "congratulated": "False"},
#     {"uid": "1704663243212301","name": "Andris","birthday": "1993.08.03", "email": "ar@gmail.com", "about": "smth", "congratulated": "False"}
#     ]

# person = [{"uid": "1704663936754301","name": "Gints","birthday": "1993.05.12", "email": "gints@gmail.com", "about": "smth", "congratulated": "False"},]