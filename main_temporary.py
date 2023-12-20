from rich.console import Console
from Classes.Record import Record
from Classes.Addressbook import AddressBook
from Classes.Classes_for_secretary import DateFormatError,UnrealDateError,InvalidNumberError

from pathlib import Path

book = AddressBook()
console = Console()


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyError:
            console.print("This contact doesn't exist, please try again", style="red")
        except DateFormatError:
            console.print("Please use correct date format DD.MM.YYYY.", style="red")
        except UnrealDateError:
            console.print("Please wrire correct date", style="red")
        except InvalidNumberError:
            console.print("Phone number must be 10 digits", style="red")
        except ValueError:
            console.print("Exception", style="red")
        except IndexError:
            console.print("This contact cannot be added, it exists already", style="red")
        except TypeError:
            console.print("Unknown command or incorrect number of arguments, please try again", style="red")

    return inner


def hello(*_):
    console.print("How can I help you?", style="blue")


def exit(*_):
    console.print("Good bye!", style="blue")


def add_contact(name, phone):
    record = Record(name)
    book.add_record(record)
    record.add_phone(phone)
    console.print(f"Contact {name} added successfully.", style="green")


def find_contact(name):
    contact = book.find_contact(name)
    if contact:
        console.print(f"Contact {name} found:\n{contact}", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def delete_phone(name, phone):
    contact = book.find_contact(name)
    if contact:
        contact.remove_phone(phone)
        console.print(f"{name}'s phone {phone} deleted", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def add_phone(name, phone):
    contact = book.find_contact(name)
    if contact:
        console.print(f"contact.add_phone(phone)", style="green" )
    else:
        console.print(f"Contact {name} not found.", style="red")


def change_contact(name, phone, new_phone):
    book.change_contact(name, phone, new_phone)
    console.print(f"{name}'s phone number changed successfully.", style="green")


def show_all(*_):
    if book.data:
        for contact in book.data.values():
            console.print(f"{contact}", style="green")
    else:
        console.print("Contact list is empty", style="red")


def show_phone(name):
    contact = book.find_contact(name)
    if contact:
        console.print(f"{name}'s phone numbers: {', '.join(p.value for p in contact.phones)}", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def add_birthday(name, birthday):
    contact = book.find_contact(name)
    if contact:
        contact.add_birthday(birthday)
        console.print(f"{name}'s birthday added successfully.", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def show_birthday(name):
    contact = book.find_contact(name)
    if contact:
        console.print(contact.show_birthday(), style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")
    
def birthdays(days):
    book.birthdays(days)

def save_address_book():
    book.save_to_file(FILENAME_AB)


def load_address_book():
    book.read_from_file(FILENAME_AB)


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
}


@error_handler
def parser_input(user_input):
    cmd, *args = user_input.strip().split(" ")
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        console.print("Unknown command, please try again", style="red")
    try:
        return handler(*args)
    except TypeError:
        console.print("Incorrect number of arguments, please try again", style="red")


def main():
    console.print("Welcome mate!!", style="blue")
    while True:
        user_input = input("Enter command> ")
        if user_input in ("close", "exit"):
            console.print("Good bye!", style="blue")
            break
        parser_input(user_input)


if __name__ == "__main__":
    main()
