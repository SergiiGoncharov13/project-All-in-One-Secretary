from All_in_One_Secretary.Classes.Record import Record
from rich.console import Console
from collections import UserDict
import json
from All_in_One_Secretary.func_get_birthday import get_birthdays_in_days

console = Console()


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        return self.data[record.name.value]

    def find_contact(self, name):
        return self.data.get(name)

    def delete_contact(self, name):
        self.data.pop(name, None)

    def birthdays(self, days):
        get_birthdays_in_days(self, days)

    def change_contact(self, name, phone, new_phone):
        if name in self.data:
            self.data[name].edit_phone(phone, new_phone)
        else:
            console.print(f"Contact {name} not found", style="red")

    def save_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                data = {name: record.to_json() for name, record in self.data.items()}
                json.dump(data, file)
                console.print("Address book is saved to file", style="green")
        except FileNotFoundError:
            console.print("File not found. Address book isn't saved", style="red")
        except PermissionError:
            console.print(
                "Access to file is denied. Address book isn't saved.", style="red"
            )
        except Exception as e:
            console.print(f"Error! Address book isn't saved: {e}", style="red")

    def read_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for name, record_data in data.items():
                    self.data[name] = Record.from_json(record_data)
                console.print("Adress book is loaded from file", style="green")
        except FileNotFoundError:
            console.print("File not found. Creating a new address book.", style="red")
        except PermissionError:
            console.print(
                "Access to file is denied. Creating a new address book.", style="red"
            )
        except Exception as e:
            console.print(
                f"Error by loadind file. Creating a new address book: {e}.", style="red"
            )
