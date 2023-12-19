from Classes.Classes_for_secretary import Birthday
from datetime import datetime
from collections import defaultdict   



def get_birthdays_in_days(self, days_ahead):
    today = datetime.today().date()
    upcoming_birthdays = defaultdict(list)

    for records in self.data.values():
        for record in records:
            if record.birthday:
                name = record.name.value
                birthday = datetime.strptime(record.birthday.value, Birthday.DATE_FORMAT).date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= days_ahead:
                    upcoming_birthdays[name].append((birthday_this_year, delta_days))

        if upcoming_birthdays:
            print(f"Upcoming birthdays in the next {days_ahead} days:")
            for name, birthdays in upcoming_birthdays.items():
                for birthday, delta_days in birthdays:
                    print(f"{name}'s birthday is on {birthday.strftime('%Y-%m-%d')}, {delta_days} days from today.")
        else:
            print(f"No upcoming birthdays in the next {days_ahead} days.")
           