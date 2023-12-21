from datetime import datetime
import re

class Field:
    """
    A generic class representing a field with a value.
    """

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f"{self._value}"

class Name(Field):
    """
    Represents a name field.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError("Name is a required field.")

class InvalidNumberError(ValueError):
    """
    Custom exception for invalid phone number format.
    """

    pass

class Phone(Field):
    """
    Represents a phone number field.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.fullmatch(r"\d{10}", value):
            self.__value = value
        else:
            raise InvalidNumberError("Invalid number format.")

class DateFormatError(ValueError):
    """
    Custom exception for invalid date format.
    """

    pass

class UnrealDateError(ValueError):
    """
    Custom exception for an unreal date (e.g., February 30).
    """

    pass

class Birthday(Field):
    """
    Represents a birthday field.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.fullmatch(r"\d{2}.\d{2}.\d{4}", value):
            try:
                value = datetime.strptime(value, "%d.%m.%Y").date()
                self.__value = value
            except ValueError:
                raise UnrealDateError()
        else:
            raise DateFormatError()

    def __str__(self):
        return self.value.strftime("%d.%m.%Y") if self.value else None

class Address(Field):
    """
    Represents an address field.
    """

    def __init__(self, value):
        super().__init__(value)

class EmailFormatError(ValueError):
    """
    Custom exception for invalid email format.
    """

    pass

class Email(Field):
    """
    Represents an email field.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]{2,}", value):
            self.__value = value
        else:
            raise EmailFormatError("Invalid email format")

class NoteTitle(Field):
    """
    Represents a note title field.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError("Title is a required field.")

class NoteContent(Field):
    """
    Represents a note content field.
    """

    def __init__(self, value):
        super().__init__(value)

class NoteCreationDate(Field):
    """
    Represents the creation date of a note.
    """

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class NoteDeadline(Birthday):
    """
    Represents the deadline of a note.
    """

    def __init__(self, value):
        super().__init__(value)

class NoteTag(Field):
    """
    Represents a tag associated with a note.
    """

    def __init__(self, value):
        super().__init__(value)
