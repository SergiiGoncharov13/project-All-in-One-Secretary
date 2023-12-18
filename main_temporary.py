

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact doesnt exist, please try again"
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return "This contact cannot be added, it exists already"
        except TypeError:
            return "Unknown command, please try again"
    return inner


def hello(_):
    return "How can I help you?"
    
def exit(_):
    return "Good bye!"


HANDLERS = {
    "hello": hello,
    "close": exit,
    "exit": exit,
    # "add": add_contact,
    # "change": change_contact,
    # "all": show_all,
    # "phone": show_phone,
    # "add-birthday": add_birthday,
    # "show-birthday": show_birthday,
    # "save": save_address_book,
    # "load": load_address_book
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
