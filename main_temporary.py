from Classes.Record import Record
from Classes.Addressbook import AddressBook
from Classes.NoteBook import NoteBook
from Classes.Classes_for_secretary import (
    DateFormatError,
    UnrealDateError,
    InvalidNumberError,
)

from pathlib import Path

book = AddressBook()
notebook = NoteBook()


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyError:
            print("This contact doesn't exist, please try again")
        except DateFormatError:
            return "Please use correct date format DD.MM.YYYY."
        except UnrealDateError:
            return "Please wrire correct date"
        except InvalidNumberError:
            return "Phone number must be 10 digits"
        except ValueError as exception:
            print(exception)
        except IndexError:
            print("This contact cannot be added, it exists already")
        except TypeError:
            print("Unknown command or incorrect number of arguments, please try again")

    return inner


def hello(*_):
    print("How can I help you?")


def exit(*_):
    print("Good bye!")


def add_contact(name, phone):
    record = Record(name)
    book.add_record(record)
    record.add_phone(phone)
    print(f"Contact {name} added successfully.")


def find_contact(name):
    contact = book.find_contact(name)
    if contact:
        print(f"Contact {name} found:\n{contact}")
    else:
        print(f"Contact {name} not found.")


def delete_phone(name, phone):
    contact = book.find_contact(name)
    if contact:
        contact.remove_phone(phone)
        print(f"{name}'s phone {phone} deleted")
    else:
        print(f"Contact {name} not found.")


def add_phone(name, phone):
    contact = book.find_contact(name)
    if contact:
        print(contact.add_phone(phone))
    else:
        print(f"Contact {name} not found.")


def change_contact(name, phone, new_phone):
    book.change_contact(name, phone, new_phone)
    print(f"{name}'s phone number changed successfully.")


def show_all(*_):
    if book.data:
        for contact in book.data.values():
            print(contact)
    else:
        print("Contact list is empty")


def show_phone(name):
    contact = book.find_contact(name)
    if contact:
        print(f"{name}'s phone numbers: {', '.join(p.value for p in contact.phones)}")
    else:
        print(f"Contact {name} not found.")


def add_birthday(name, birthday):
    contact = book.find_contact(name)
    if contact:
        contact.add_birthday(birthday)
        print(f"{name}'s birthday added successfully.")
    else:
        print(f"Contact {name} not found.")


def show_birthday(name):
    contact = book.find_contact(name)
    if contact:
        print(contact.show_birthday())
    else:
        return f"Contact {name} not found."


def birthdays(days):
    book.birthdays(days)


def save_address_book():
    book.save_to_file(FILENAME_AB)


def load_address_book():
    book.read_from_file(FILENAME_AB)


def add_note(*args):
    title, *note_parts = args
    note = " ".join(note_parts)
    note = notebook.add_note(title, note)


def change_note(title, note):
    notebook.change_note(title, note)


def delete_note(title):
    notebook.delete_note(title)


def find_note_by_title(title):
    note = notebook.find_by_title(title)
    if note:
        print(f"Note with title {title} found:\n{note}")
    else:
        print(f"Note with title {title} not found.")


def add_tag(title, tag):
    notebook.add_tag(title, tag)


def delete_tag(title, tag):
    notebook.delete_tag(title, tag)


def change_tag(tag, new_tag):
    notebook.change_tag(tag, new_tag)


def find_note_by_tag(tag):
    if notebook.find_by_tag(tag):
        print(notebook.find_by_tag(tag))
    else:
        print(f"No notes found by tag {tag}")


def sort_notes_by_tags():
    print(notebook.sort_notes_by_tags())


def add_deadline(title, date):
    notebook.add_deadline(title, date)


def to_do_list(days):
    print(to_do_list(days))


FILENAME_AB = Path(__file__).parent / "AddressBook.json"
FILENAME_NB = Path(__file__).parent / "NoteBook.json"
HANDLERS = {
    "hello": hello,
    "close": exit,
    "exit": exit,
    "add": add_contact,
    "find": find_contact,
    "delete-phone": delete_phone,
    "add-phone": add_phone,
    "change": change_contact,
    "all": show_all,
    "phone": show_phone,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "save": save_address_book,
    "load": load_address_book,
    "add-note": add_note,
    "change-note": change_note,
    "delete-note": delete_note,
    "find-note": find_note_by_title,
    "find-tag": find_note_by_tag,
    "add-tag": add_tag,
    "delete-tag": delete_tag,
    "change-tag": change_tag,
    "sort-notes": sort_notes_by_tags,
    "deadline": add_deadline,
    "to-do": to_do_list,
}


@error_handler
def parser_input(user_input):
    cmd, *args = user_input.strip().split(" ")
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        print("Unknown command, please try again")
    try:
        return handler(*args)
    except TypeError as e:
        print(f"Incorrect number of arguments, please try again: {e}")


def main():
    print("Welcome mate!!")
    while True:
        user_input = input("Enter command> ")
        if user_input in ("close", "exit"):
            print("Good bye!")
            break
        parser_input(user_input)


if __name__ == "__main__":
    main()
