from collections import defaultdict, OrderedDict
from datetime import datetime


def to_do_list(notebook, days):
    """Generates and prints a to-do list from notes for the upcoming specified days."""
    to_do_list = defaultdict(list)
    today = datetime.today().date()
    for note_record in notebook.data.values():
        if note_record.deadline is not None:
            delta_days = (note_record.deadline.value - today).days
            if 0 <= delta_days < int(days):
                deadline_date = str(note_record.deadline)
                to_do_list[deadline_date].append(note_record.content)
    if to_do_list:
        sorted_to_do_list = OrderedDict(sorted(to_do_list.items()))
        for date, notes in sorted_to_do_list.items():
            notes_str = '; '.join(str(note) for note in notes)
            print(f"{date}: {notes_str}")
    else:
        print(f"There aren't any tasks in next {days} days")
