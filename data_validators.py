"""functions that perfom str or int validations"""

from validator_collection import validators, errors
from datetime import datetime
from data_manager import load_settings
import re


def is_valid_birthday(bday: str) -> bool:
    """returns True if YYYY-MM-DD or YYYY.MM.DD or YYYY/MM/DD, else False"""
    if not bday:
        return False
    elif not re.search(r"^\d{4}(-|\.|/)\d{2}(-|\.|/)\d{2}$", bday):
        return False

    y, m, d = re.split(r"[\./-]", bday)
    current_year = datetime.now().year
    if int(y) > current_year:
        return False
    elif 12 < int(m) or int(m) < 1:
        return False
    elif 31 < int(d) or int(d) < 1:
        return False
    return True


def is_valid_email(address: str) -> bool:
    try:
        validators.email(address)
        return True
    except (errors.EmptyValueError, errors.InvalidEmailError):
        return False


def is_birthday_today(person: list[dict]) -> bool:
    birthday = person[0]["birthday"]
    # Birthday string to a datetime object
    birthday_date = datetime.strptime(birthday, "%Y.%m.%d").date()
    today_date = datetime.now().date()
    return (
        birthday_date.day == today_date.day and birthday_date.month == today_date.month
    )


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
