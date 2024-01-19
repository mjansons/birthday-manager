import os
import pytest
from datetime import datetime
from data_validators import is_valid_birthday, is_valid_email, is_birthday_today, is_new_year, is_auto_mode_on

from data_manager import (  # Replace 'your_module_name' with the actual name of your module
    create_csv,
    wipe_file,
    read_csv,
    rewrite_csv,
    append_csv,
    append_history_csv,
    edit_contact,
    edit_specific_contact,
    delete_contact,
    get_duplicates,
    search_by_keyword,
    make_list_printable,
    print_person,
    add_days_until_birthday,
    turning_years,
    get_todays_celebrators,
    create_settings_file,
    load_settings,
    save_settings,
    switch_auto_mode,
    switch_api_working,
    update_last_reset_date,
    check_and_reset_if_new_year,
)

@pytest.fixture
def setup_csv(tmp_path):
    filepath = tmp_path / "test.csv"
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)

def test_create_csv(setup_csv):
    create_csv(setup_csv)
    assert os.path.exists(setup_csv)

def test_wipe_file(setup_csv):
    create_csv(setup_csv)
    wipe_file(setup_csv)
    assert os.path.exists(setup_csv) and os.stat(setup_csv).st_size == 0

def test_read_csv(setup_csv):
    create_csv(setup_csv)
    data = read_csv(setup_csv)
    assert isinstance(data, list)

def test_rewrite_csv(setup_csv):
    create_csv(setup_csv)
    data = [{"uid": '1', "name": "John"}, {"uid": '2', "name": "Jane"}]
    rewrite_csv(setup_csv, data)
    read_data = read_csv(setup_csv)
    assert read_data == data

def test_append_csv(setup_csv):
    data = [{"uid": '1', "name": "John"}] 
    append_csv(setup_csv, data)
    read_data = read_csv(setup_csv)
    assert read_data == data

def test_append_history_csv(setup_csv):
    data = [{"uid": 1, "name": "John", "email": "john@example.com"}]
    append_history_csv(setup_csv, data, "Test Subject", "Test Message")
    read_data = read_csv(setup_csv)
    assert read_data[0]["subject"] == "Test Subject"
    assert read_data[0]["message"] == "Test Message"

def test_edit_contact():
    contacts = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
    ]
    edited_contacts = edit_contact(contacts, "email", "newemail@example.com")
    assert all(person["email"] == "newemail@example.com" for person in edited_contacts)

def test_edit_specific_contact():
    full_list = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
    ]
    my_contact = [{"uid": 1, "name": "John", "email": "john@example.com"}]
    edited_list = edit_specific_contact(full_list, my_contact, "email", "newemail@example.com")
    assert edited_list[0]["email"] == "newemail@example.com"

def test_delete_contact():
    all_contacts = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
        {"uid": 3, "name": "Jim", "email": "jim@example.com"},
    ]
    removable_contact_list = [{"uid": 2, "name": "Jane", "email": "jane@example.com"}]
    remaining_contacts = delete_contact(all_contacts, removable_contact_list)
    assert all(person not in remaining_contacts for person in removable_contact_list)

def test_get_duplicates():
    listdict = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
        {"uid": 3, "name": "John", "email": "john.doe@example.com"},
    ]
    duplicates = get_duplicates(listdict, "name", "John")
    assert len(duplicates) == 2

def test_search_by_keyword():
    listdict = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
        {"uid": 3, "name": "Jim", "email": "jim@example.com"},
    ]
    search_keys = ["name", "email"]
    keyword = "john"
    matches = search_by_keyword(listdict, search_keys, keyword)


def test_make_list_printable():
    the_list = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
    ]
    printable_list = make_list_printable(the_list)
    assert isinstance(printable_list, list)

def test_print_person(capfd):
    the_list = [
        {"uid": 1, "name": "John", "email": "john@example.com"},
        {"uid": 2, "name": "Jane", "email": "jane@example.com"},
    ]
    print_person(the_list)
    captured = capfd.readouterr()
    assert "John" in captured.out
    assert "Jane" in captured.out


def test_get_todays_celebrators():
    contacts = [
        {"uid": 1, "name": "John", "birthday": "1990.01.01", "congratulated": "False"},
        {"uid": 2, "name": "Jane", "birthday": "1995.05.05", "congratulated": "True"},
    ]
    celebrators = get_todays_celebrators(contacts, congr=True)

    today = datetime.now().date()
    for celebrator in celebrators:
        birthday_date = datetime.strptime(celebrator["birthday"], "%Y.%m.%d").date()
        assert is_birthday_today(celebrator, today) and celebrator["congratulated"] == "True"


def test_create_settings_file(setup_csv):
    create_settings_file(setup_csv)
    assert os.path.exists(setup_csv)

def test_load_settings(setup_csv):
    create_settings_file(setup_csv)
    settings = load_settings(setup_csv)
    assert isinstance(settings, dict)

def test_save_settings(setup_csv):
    settings = {"auto_mode_on": "True", "api_is_working": "False"}
    save_settings(setup_csv, settings)
    loaded_settings = load_settings(setup_csv)
    assert loaded_settings == {"auto_mode_on": "True", "api_is_working": "False"}


def test_update_last_reset_date(setup_csv):
    settings = {"last_reset_date": "2023-01-01"}
    update_last_reset_date(settings)
    assert "last_reset_date" in settings
    assert settings["last_reset_date"] == datetime.now().date().strftime("%Y-%m-%d")

def test_check_and_reset_if_new_year(setup_csv):
    settings = {"last_reset_date": "2023-01-01"}
    check_and_reset_if_new_year(setup_csv, setup_csv)
    loaded_settings = load_settings(setup_csv)
    assert "last_reset_date" in loaded_settings
    assert loaded_settings["last_reset_date"] == datetime.now().date().strftime("%Y-%m-%d")


def test_is_valid_birthday():
    # Valid birthdays
    assert is_valid_birthday("1990-01-01") == True
    assert is_valid_birthday("1990.01.01") == True
    assert is_valid_birthday("1990/01/01") == True

    # Invalid birthdays
    assert is_valid_birthday("invalid") == False
    assert is_valid_birthday("") == False
    assert is_valid_birthday("2023-13-01") == False
    assert is_valid_birthday("2023-01-32") == False

def test_is_valid_email():
    # Valid emails
    assert is_valid_email("user@example.com") == True
    assert is_valid_email("user.name@example.co.uk") == True

    # Invalid emails
    assert is_valid_email("invalid") == False
    assert is_valid_email("user@com") == False
    assert is_valid_email("") == False

def test_is_birthday_today():
    # Birthday today
    person_today = [{"birthday": datetime.now().strftime("%Y.%m.%d")}]
    assert is_birthday_today(person_today) == True

    # Birthday not today
    person_not_today = [{"birthday": "1990.01.01"}]
    assert is_birthday_today(person_not_today) == False
