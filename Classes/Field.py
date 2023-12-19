from datetime import datetime
import re


class Field:
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
        return f'{self._value}'
    
class Name(Field):
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
    pass


class Phone(Field):
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
    pass


class UnrealDateError(ValueError):
    pass


class Birthday(Field):
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
    def __init__(self, value):
        super().__init__(value)



class EmailFormatError(ValueError):
    pass


class Email(Field):
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
    def __init__(self, value):
        super().__init__(value)

class NoteCreationDate(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = datetime.today().date()

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class NoteDeadline(Birthday):
    def __init__(self, value):
        super().__init__(value)

class NoteTag(Field):
    def __init__(self, value):
        super().__init__(value)
    