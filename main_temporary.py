from Classes.Addressbook import AddressBook

book = AddressBook()

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Цей контакт не існує, будь ласка, спробуйте ще раз"
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return "Цей контакт не може бути доданий, він вже існує"
        except TypeError:
            return "Невідома команда, будь ласка, спробуйте ще раз"
    return inner

def hello(_):
    return "How can I help you?"
    
def exit(_):
    return "Goodbye!"

def add_contact(name):
    book.add_record(name)
    return f"Контакт {name} успішно додано."

def change_contact(name, phone, new_phone):
    book.change_contact(name, phone, new_phone)
    return f"Номер телефону {name} успішно змінено."

def show_all(_):
    return str(book)

def show_phone(name):
    contact = book.find_contact(name)
    if contact:
        return f"Номери телефону {name}: {', '.join(contact.phones)}"
    else:
        return f"Контакт {name} не знайдено."

def add_birthday(name, birthday):
    contact = book.find_contact(name)
    if contact:
        contact.add_birthday(birthday)
        return f"День народження {name} успішно додано."
    else:
        return f"Контакт {name} не знайдено."

def show_birthday(name):
    contact = book.find_contact(name)
    if contact:
        return contact.show_birthday()
    else:
        return f"Контакт {name} не знайдено."

def save_address_book(filename):
    book.save_to_file(filename)
    return "Адресна книга успішно збережена."

def load_address_book(filename):
    book.read_from_file(filename)
    return "Адресна книга успішно завантажена."

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
        if args:
            cmd = f"{cmd} {args[0]}"
            args = args[1:]
        handler = HANDLERS[cmd.lower(), "Unknown command"]
    return handler, args



def main():
    while True:
        user_input = input("Enter command> ")
        if user_input in ("close", "exit"):
            print("Good bye!")
            break
        handler, *args = parser_input(user_input)
        result = handler(*args)
        if not result:
            print("Good bye!")
            break
        print(result)


if __name__ == "__main__":
    main()
