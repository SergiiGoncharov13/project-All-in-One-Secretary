from Field import Name, Phone, Birthday, Address, Email
from collections import UserDict
import json


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        if phone not in [p.value for p in self.phones]:
            self.phones.append(Phone(phone))

    def edit_phone(self, phone, new_phone):
        self.phones = [p for p in self.phones if p.value != phone]
        self.phones.append(Phone(new_phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def find_phone(self, phone):
        return next((p.value for p in self.phones if p.value == phone), None)

    def __str__(self):
        email_str = str(self.email) if self.email is not None else "Unknown"
        address_str = str(self.address) if self.address is not None else "Unknown"
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones added"
        return (f"Contact name: {self.name.value}, "
                f"phones: {phones_str}, "
                f"email: {email_str}, "
                f"address: {address_str}, ")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return f"{self.name.value}'s birthday is on {self.birthday.value.strftime("%d %B %Y")}"
        return f"No information about {self.name.value}'s date of birth"
    
    def add_email(self,email):
       self.email = Email(email)

    def add_address(self,address):
        self.address = Address(address)

    def to_json(self):
        return {
            "name": str(self.name),
            "phones": [str(phone) for phone in self.phones],
            "birthday": str(self.birthday) if self.birthday else None,
            "email": str(self.email) if self.email else None,
            "address": str(self.address) if self.address else None,
        }

    def from_json(data):
        record = Record(data["name"])
        for phone in data["phones"]:
            record.add_phone(phone)
        if data["birthday"]:
            record.add_birthday(data["birthday"])
        if data["email"]:
            record.add_email(data["email"])
        if data["address"]:
            record.add_address(data["address"])
        return record


class AddressBook(UserDict):
    def add_record(self, record):
        if record not in self.data:
            self.data[record] = Record(record)
        return self.data[record]

    def find_contact(self, name):
        return self.data.get(name)

    def delete_contact(self, name):
        self.data.pop(name, None)

    def birthdays(self,days):
        pass

    def save_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                data = {name: record.to_json() for name, record in self.data.items()}
                json.dump(data, file)
                print("Address book is saved to file")
        except FileNotFoundError:
            print("File not found. Address book isn't saved")
        except PermissionError:
            print("Acces s to file is denied. Address book isn't saved.")
        except Exception as e:
            print(f"Error! Address book isn't saved: {e}")

    def read_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for name, record_data in data.items():
                    self.data[name] = Record.from_json(record_data)
                print("Adress book is loaded from file")
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
        except PermissionError:
            print("Access to file is denied. Creating a new address book.")
        except Exception as e:
            print(f"Error by loadind file. Creating a new address book: {e}.")