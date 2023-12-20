from Classes.Classes_for_secretary import Name, Phone, Birthday, Address, Email


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
            return f"Phone {phone} added successfully."
        else:
            return f"Phone {phone} already exists."

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
        phones_str = (
            "; ".join(p.value for p in self.phones)
            if self.phones
            else "No phones added"
        )
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"email: {email_str}, "
            f"address: {address_str}, "
        )

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return f"{self.name.value}'s birthday is on {self.birthday.value.strftime('%d %B %Y')}"
        return f"No information about {self.name.value}'s date of birth"

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
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
