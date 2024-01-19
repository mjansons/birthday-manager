"""this is the main settings mode file and from here auto mode can be launched in a seperate thread"""
from data_manager import (
    load_settings,
    switch_auto_mode, 
    update_last_reset_date, 
    save_settings
)
from auto_mode import auto_congratulation_mode
from data_validators import is_auto_mode_on
import threading
import time


class BackFromSettings(Exception):
    pass


def settings_mode(contact_file_path, history_file_path, failed_recipients_path, the_settings_path):
    filepath = the_settings_path
    settings = load_settings(filepath)
    while True:
        # Read settings to get the latest status
        settings = load_settings(filepath)
        time.sleep(1.5)
        print(
            f"\nCurrent Settings:\n\n"
            f"Auto mode ON: {settings['auto_mode_on']}\n"
            f"API is working: {settings['api_is_working']}\n"
            f"Last Reset Date: {settings['last_reset_date']}"
        )
        answer = input(
            "\nSwitch auto mode?\n\n"
            f"1. Yes\n"
            f"2. I'm done, return to Main Menu\n\n"
            f"Option: "
        ).strip()
        if answer == "1":
            switch_auto_mode(settings)
            update_last_reset_date(settings)
            save_settings(filepath, settings)

            # start auto mode if it was off in the settings and now is turned on
            if is_auto_mode_on(filepath):
                auto_thread = threading.Thread(
                    target=auto_congratulation_mode,
                    args=(
                        contact_file_path,
                        history_file_path,
                        failed_recipients_path,
                        the_settings_path,
                    ),
                )
                auto_thread.daemon = True
                auto_thread.start()

        elif answer == "2":
            print("\nAll changes have been saved!")
            raise BackFromSettings
        else:
            print("Enter only '1' or '2'")


