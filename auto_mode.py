"""this file executes automode"""
from data_manager import (
    create_csv,
    append_csv,
    read_csv,
    get_todays_celebrators,
    edit_specific_contact,
    rewrite_csv,
    delete_contact,
    append_history_csv,
)
from ai_manager import MessageMaker
from email_manager import send_mail
from ai_manager import WriteManual
from email_manager import WrongEmail

import time


def auto_congratulation_mode(contact_file_path, history_file_path, failed_recipients_path, settings_file_path):
    """This does the same thing as congratulation manager, except it skips user inputs/ verifications"""
    # Loading here to Avoid Circular Dependency on settings file
    from settings import (
    is_auto_mode_on,
    check_and_reset_if_new_year,
    load_settings,
    switch_auto_mode,
    update_last_reset_date,
    save_settings,
    switch_api_working
)
    
    continue_running = True

    while is_auto_mode_on(settings_file_path) and continue_running:
        create_csv(history_file_path)
        check_and_reset_if_new_year(settings_file_path, contact_file_path)
        try:
            contacts = read_csv(contact_file_path)
        except ValueError:
            contacts = []

        todays_celebrators = get_todays_celebrators(contacts, False)

        while len(todays_celebrators) > 0 and continue_running:
            for contact_to_congratulate in todays_celebrators:
                try:
                    global_history = read_csv(history_file_path)
                except ValueError:
                    global_history = []
                
                bot = MessageMaker([contact_to_congratulate], global_history)
                try:
                    # switch "api_working_on", if it was off
                    settings = load_settings(settings_file_path)
                    if settings["api_is_working"] == "False":
                        switch_api_working(settings)
                        save_settings(settings_file_path, settings)
                    message = bot.get_prompt()
                    subject = "Happy Birthday!"
                # if there was an error turn off auto mode
                except WriteManual:
                    settings = load_settings(settings_file_path)
                    switch_auto_mode(settings)
                    switch_api_working(settings)
                    update_last_reset_date(settings)
                    save_settings(settings_file_path, settings)
                    continue_running = False
                    break
                    

                try:
                    send_mail([contact_to_congratulate], message, subject)
                except WrongEmail:
                    append_csv(failed_recipients_path, [contact_to_congratulate])
                    edit_specific_contact(
                        contacts, [contact_to_congratulate], "congratulated", "True"
                    )
                    rewrite_csv(contact_file_path, contacts)
                    todays_celebrators = delete_contact(
                        todays_celebrators, [contact_to_congratulate]
                    )

                else:
                    append_history_csv(
                        history_file_path, [contact_to_congratulate], subject, message
                    )
                    edit_specific_contact(
                        contacts, [contact_to_congratulate], "congratulated", "True"
                    )
                    rewrite_csv(contact_file_path, contacts)
                    todays_celebrators = delete_contact(
                        todays_celebrators, [contact_to_congratulate]
                    )
        # no need to re-check for anyone's birthay constantly
        time.sleep(60)


if __name__ == "__main__":
    ...
