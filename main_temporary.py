from Classes.Addressbook import AddressBook, Record
from Classes.Classes_for_secretary import Name

book = AddressBook()

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact doesn't exist, please try again"
        except ValueError as exception:
            return str(exception)
        except IndexError:
            return "This contact cannot be added, it exists already"
        except TypeError:
            return "Unknown command or incorrect number of arguments, please try again"
    return inner

def hello(*_):
    return "How can I help you?"

def exit(*_):
    return "Good bye!"

def add_contact(name):
    record = Record(name)
    book.add_record(record)
    return f"Contact {name} added successfully."

def change_contact(name, phone, new_phone):
    book.change_contact(name, phone, new_phone)
    return f"{name}'s phone number changed successfully."

def show_all(*_):
    return str(book)

def show_phone(name):
    contact = book.find_contact(name)
    if contact:
        return f"{name}'s phone numbers: {', '.join(contact.phones)}"
    else:
        return f"Contact {name} not found."

def add_birthday(name, birthday):
    contact = book.find_contact(name)
    if contact:
        contact.add_birthday(birthday)
        return f"{name}'s birthday added successfully."
    else:
        return f"Contact {name} not found."

def show_birthday(name):
    contact = book.find_contact(name)
    if contact:
        return contact.show_birthday()
    else:
        return f"Contact {name} not found."

def save_address_book(filename):
    book.save_to_file(filename)
    return "Address book saved successfully."

def load_address_book(filename):
    book.read_from_file(filename)
    return "Address book loaded successfully."

HANDLERS = {
    "hello": hello,
    "close": exit,
    "exit": exit,
    "add": add_contact,
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
    cmd, *args = user_input.strip().split(' ')
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        return "Unknown command, please try again"
    
    try:
        return handler(*args)
    except TypeError:
        return "Incorrect number of arguments, please try again"

def main():
    while True:
        user_input = input("Enter command> ")
        if user_input in ("close", "exit"):
            print("Good bye!")
            break
        result = parser_input(user_input)
        print(result)

if __name__ == "__main__":
    main()
