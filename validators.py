"""functions that perfom str or int validations"""

from validator_collection import validators, errors
from datetime import datetime
import re


def is_valid_birthday(bday: str) -> bool:
    """returns True if YYYY-MM-DD or YYYY.MM.DD or YYYY/MM/DD, else False"""
    if not bday:
        return False
        # raise ValueError("No birthday added")
    elif not re.search(r"^\d{4}(-|.|/)\d{2}(-|.|/)\d{2}$", bday):
        return False
        # raise ValueError("Invalid Format. Expected: YYYY-MM-DD or YYYY.MM.DD or YYYY/MM/DD")

    y, m, d = re.split(r"[\./-]", bday)
    current_year = datetime.now().year
    if int(y) > current_year:
        return False
        # raise ValueError("Invalid year")
    elif 12 < int(m) or int(m) < 1:
        return False
        # raise ValueError("Invalid month")
    elif 31 < int(d) or int(d) < 1:
        return False
        # raise ValueError("Invalid day")
    return True


def is_valid_email(address: str) -> bool:
    """returns True or False for email"""
    try:
        validators.email(address)
        return True
    except (errors.EmptyValueError, errors.InvalidEmailError):
        return False


def is_birthday_today(person: list[dict]) -> bool:
    """checks if bday is today"""
    birthday = person[0]["birthday"]
    # Birthday string to a datetime object
    birthday_date = datetime.strptime(birthday, "%Y.%m.%d").date()
    today_date = datetime.now().date()
    return (
        birthday_date.day == today_date.day and birthday_date.month == today_date.month
    )


if __name__ == "__main__":
    ...
