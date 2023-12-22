import difflib
from rich.console import Console
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
console = Console()
notebook = NoteBook()


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
            console.print("Not enough values (expected 2 parameters)", style="red")
        except IndexError:
            console.print(
                "This contact cannot be added, it exists already", style="red"
            )
        except TypeError:
            console.print(
                "Unknown command or incorrect number of arguments, please try again",
                style="red",
            )

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
       contact.add_phone(phone)
       console.print(f"Phone {phone} was successfully added to {name}", style="green")
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
        console.print(
            f"{name}'s phone numbers: {', '.join(p.value for p in contact.phones)}",
            style="green",
        )
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


def add_email(name, email):
    contact = book.find_contact(name)
    if contact:
        contact.add_email(email)
        console.print(f"{name}'s email added successfully.", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def add_address(*args):
    name, *address_parts = args
    address = " ".join(address_parts)
    contact = book.find_contact(name)
    if contact:
        contact.add_address(address)
        console.print(f"{name}'s address added successfully.", style="green")
    else:
        console.print(f"Contact {name} not found.", style="red")


def save_address_book():
    book.save_to_file(FILENAME_AB)


def load_address_book():
    book.read_from_file(FILENAME_AB)


def help() -> str:
    console.print(
        "[bold magenta]Main commands:[/bold magenta]\n"
        "[bold magenta]load[/bold magenta]  - load the book\n"
        "[bold magenta]save[/bold magenta] - save the book\n"
        "[bold magenta]add[/bold magenta] - add contact and number\n"
        "[bold magenta]find[/bold magenta] - find contact number by name\n"
        "[bold magenta]delete-phone[/bold magenta] - delete contact number\n"
        "[bold magenta]add-phone[/bold magenta] - add phone to contact\n"
        "[bold magenta]change[/bold magenta] - change phone to new phone\n"
        "[bold magenta]all[/bold magenta] - show all contacts in AddressBook\n"
        "[bold magenta]phone[/bold magenta] - show phone by name\n"
        "[bold magenta]add-birthhday[/bold magenta] - add birthday to contact\n"
        "[bold magenta]show birthday[/bold magenta] - show contact birthday\n"
        "[bold magenta]birthday[/bold magenta] - show all birthdays\n"
        "[bold magenta]close[/bold magenta] - close programm\n"
        "[bold magenta]exit[/bold magenta] - close programm\n"
        "[bold magenta]hello[/bold magenta] - say hello\n"
        "[bold magenta]add-address[/bold magenta] - add address to contact\n"
        "[bold magenta]add-email[/bold magenta] - add email to contact\n"
        "[bold magenta]add-note[/bold magenta] - add note to title\n"
        "[bold magenta]change-note[/bold magenta] - change note by title\n"
        "[bold magenta]delete-note[/bold magenta] - delete note by title\n"
        "[bold magenta]find-note[/bold magenta] - find note by title\n"
        "[bold magenta]find-tag[/bold magenta] - find note by tag\n"
        "[bold magenta]add-tag[/bold magenta] - add tag by title\n"
        "[bold magenta]change-tag[/bold magenta] - change tag by title\n"
        "[bold magenta]sort-notes[/bold magenta] - sort note by tags\n"
        "[bold magenta]deadline[/bold magenta] - add deadline to title by date\n"
        "[bold magenta]save-notes[/bold magenta] - save note\n"
        "[bold magenta]load-notes[/bold magenta] - load note\n"
        "[bold magenta]to-do[/bold magenta] - a list of work to be done by that day\n"
    )


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
        console.print(f"Note with title {title} found:\n{note}", style="green")
    else:
        console.print(f"Note with title {title} not found.", style="red")


def add_tag(title, tag):
    notebook.add_tag(title, tag)


def delete_tag(title, tag):
    notebook.delete_tag(title, tag)


def change_tag(tag, new_tag):
    notebook.change_tag(tag, new_tag)


def find_note_by_tag(tag):
    if notebook.find_by_tag(tag):
        console.print(notebook.find_by_tag(tag), style="green")
    else:
        console.print(f"No notes found by tag {tag}", style="red")


def sort_notes_by_tags():
    notebook.sort_notes_by_tags()


def add_deadline(title, date):
    notebook.add_deadline(title, date)


def to_do_list(days):
    notebook.to_do_list(days)


def save_notes():
    notebook.save_to_file(FILENAME_NB)


def load_notes():
    notebook.read_from_file(FILENAME_NB)


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
    "add-address": add_address,
    "add-email": add_email,
    "save": save_address_book,
    "load": load_address_book,
    "help": help,
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
    "save-notes": save_notes,
    "load-notes": load_notes,
}


def suggest_command(user_input):
    closest_match = difflib.get_close_matches(
        user_input, HANDLERS.keys(), n=1, cutoff=0.8
    )
    if closest_match:
        console.print(f"Perhaps you meant '{closest_match[0]}'?", style="green")
    else:
        console.print("Hint not available. Please enter a valid command.", style="red")


@error_handler
def parser_input(user_input):
    cmd, *args = user_input.strip().split(" ")
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        console.print("Unknown command, please try again", style="red")
        suggestion = suggest_command(cmd.lower())
        if suggestion:
            print(suggestion)
        return
    try:
        return handler(*args)
    except TypeError as e:
        console.print(
            f"Incorrect number of arguments, please try again: {e}", style="red"
        )


def main():
    console.print(
        "Welcome mate!!, [bold green]help[/bold green] to show all comands",
        style="blue",
    )
    while True:
        user_input = input("Enter command> ")
        if user_input in ("close", "exit"):
            console.print("Good bye!", style="blue")
            break
        parser_input(user_input)


if __name__ == "__main__":
    main()
