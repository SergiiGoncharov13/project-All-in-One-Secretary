from Classes.Record import Record
from Classes.Addressbook import AddressBook
from Classes.Classes_for_secretary import Name
from pathlib import Path

book = AddressBook()


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyError:
            print("This contact doesn't exist, please try again")
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
    "save": save_address_book,
    "load": load_address_book,
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
    except TypeError:
        print("Incorrect number of arguments, please try again")


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
