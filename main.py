"""This is the main menu"""

from data_manager import read_csv, add_days_until_birthday, turning_years, get_todays_celebrators

def main():
    contacts = read_csv("contacts.csv")
    todays_celebrators = get_todays_celebrators(contacts, True)
    display_birthdays_today(todays_celebrators)
    print()
    display_upcoming_birthdays(contacts)


def display_birthdays_today(todays_celebrators: list[dict]) -> None:
    """Prints today's celebrators if there are any + how old they are getting"""
    if todays_celebrators:
        printable_celebrators = "\n".join(
            f"{person.get('name', 'Somebody')} is turning {turning_years([person])} years old today. "
            f"{'Remember to congratulate!' if person.get('congratulated', 'False') == 'False' else 'Congratulations have been sent!'}"
            for person in todays_celebrators)
        print("\n    TODAY:")
        print(printable_celebrators)



def display_upcoming_birthdays(contacts: list[dict]) -> None:
    people = contacts 
    if people:
        add_days_until_birthday(people)
        upcoming_list = [person for person in people if person.get('days_until_birthday', 0) != 0][:3]
        printable_upcoming_list = "\n".join(
            f"{person.get('name', 'Somebody')} will be turning {turning_years([person])} years old in {person["days_until_birthday"]} day(s)." for person in upcoming_list)
        print("    UPCOMING:")
        print(printable_upcoming_list)

# top 3 upcoming birthdays


# add_days_until_birthday()



# person = [{"uid": "1704663936754301","name": "Gints","birthday": "1993.05.12", "email": "gints@gmail.com", "about": "smth", "congratulated": "False"},]
# print(turning_years(person))



if __name__ == "__main__":
    main()


    