"""this is the main settings mode file and from here auto mode can be launched in a seperate thread"""
from datetime import datetime
from data_manager import read_csv, rewrite_csv, edit_contact
from auto_mode import auto_congratulation_mode
import threading
import os
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
        print(f"\nCurrent Settings:\n\nAuto mode ON: {settings['auto_mode_on']}\nAPI is working: {settings['api_is_working']}\nLast Reset Date: {settings['last_reset_date']}")
        answer = input("\nSwitch auto mode?\n\n1. Yes\n2. I'm done, return to Main Menu\nOption: ").strip()
        if answer == "1":
            switch_auto_mode(settings)
            update_last_reset_date(settings)
            save_settings(filepath, settings)

            # start auto mode if it was off in the settings and now is turned on
            if is_auto_mode_on(filepath):
                auto_thread = threading.Thread(target=auto_congratulation_mode,args=(contact_file_path, history_file_path, failed_recipients_path, the_settings_path))
                auto_thread.daemon = True
                auto_thread.start()
                time.sleep(1.33)
            
        elif answer == "2":
            print("\nAll changes have been saved!")
            raise BackFromSettings
        else:
            print("Enter only '1' or '2'")


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
    settings = {line.split("=")[0]: line.split("=")[1].strip() for line in lines if "=" in line}
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


def is_new_year(last_reset_date: str) -> bool:
    today = datetime.now().date()
    last_reset_year = datetime.strptime(last_reset_date, "%Y-%m-%d").date().year
    return today.year > last_reset_year


def is_auto_mode_on(setting_filepath: str) -> bool:
    dictionary = load_settings(setting_filepath)
    result = str(dictionary["auto_mode_on"])
    if result == "True":
        return True
    elif result == "False":
        return False


def check_and_reset_if_new_year(setting_filepath: str, all_contacts_filepath: str) -> None:
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


if __name__ == "__main__":
    settings_mode("settings.txt")
