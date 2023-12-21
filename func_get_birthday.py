from rich.console import Console
from datetime import datetime
from collections import defaultdict

# Initialize the Rich Console for enhanced output
console = Console()

# Function to retrieve upcoming birthdays within a specified number of days
def get_birthdays_in_days(self, days_ahead):
    today = datetime.today().date()
    upcoming_birthdays = defaultdict(list)
    for name, record in self.data.items():
        if record.birthday is not None:
            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            if 0 <= delta_days <= int(days_ahead):
                upcoming_birthdays[name].append((birthday_this_year, delta_days))

    if upcoming_birthdays:
        print(f"Upcoming birthdays in the next {days_ahead} days:")
        for name, birthdays in upcoming_birthdays.items():
            for birthday, delta_days in birthdays:
                console.print(
                    f"{name}'s birthday is on {birthday.strftime('%d %B %Y')}, {delta_days} days from today.",
                    style="green",
                )
    else:
        console.print(
            f"No upcoming birthdays in the next {days_ahead} days.", style="red"
        )
