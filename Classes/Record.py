from Classes.Classes_for_secretary import Name, Phone, Birthday, Address, Email

class Record:
    """
    Represents a contact record with information such as name, phones, birthday, email, and address.
    """

    def __init__(self, name):
        """
        Initialize a new contact record with the given name.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        """
        Add a phone number to the contact record.
        """
        if phone not in [p.value for p in self.phones]:
            self.phones.append(Phone(phone))
            return f"Phone {phone} added successfully to {self.name.value}."
        else:
            return f"Phone {phone} already exists."

    def edit_phone(self, phone, new_phone):
        """
        Edit a phone number in the contact record.
        """
        self.phones = [p for p in self.phones if p.value != phone]
        self.phones.append(Phone(new_phone))

    def remove_phone(self, phone):
        """
        Remove a phone number from the contact record.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def find_phone(self, phone):
        """
        Find a phone number in the contact record.
        """
        return next((p.value for p in self.phones if p.value == phone), None)

    def __str__(self):
        """
        String representation of the contact record.
        """
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
        """
        Add a birthday to the contact record.
        """
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        """
        Display the birthday information of the contact.
        """
        if self.birthday:
            return f"{self.name.value}'s birthday is on {self.birthday.value.strftime('%d %B %Y')}"
        return f"No information about {self.name.value}'s date of birth"

    def add_email(self, email):
        """
        Add an email address to the contact record.
        """
        self.email = Email(email)

    def add_address(self, address):
        """
        Add an address to the contact record.
        """
        self.address = Address(address)

    def to_json(self):
        """
        Convert the contact record to JSON format.
        """
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": str(self.birthday) if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": str(self.address) if self.address else None,
        }

    @classmethod
    def from_json(cls, data):
        """
        Create a Record instance from JSON data.
        """
        record = cls(data["name"])
        for phone in data["phones"]:
            record.add_phone(phone)
        if data["birthday"]:
            record.add_birthday(data["birthday"])
        if data["email"]:
            record.add_email(data["email"])
        if data["address"]:
            record.add_address(data["address"])
        return record
