from rich.console import Console
from collections import UserDict, defaultdict
from datetime import datetime
from to_do_func import to_do_list
import json
from Classes.Classes_for_secretary import (
    NoteTitle,
    NoteContent,
    NoteDeadline,
    NoteCreationDate,
    NoteTag,
)


console = Console()


class NoteRecord:
    def __init__(self, title, content):
        self.title = NoteTitle(title)
        self.content = NoteContent(content)
        self.creation_date = NoteCreationDate(datetime.today().date())
        self.tags = []
        self.deadline = None

    def add_tag(self, tag):
        if tag not in [t.value for t in self.tags]:
            self.tags.append(NoteTag(tag))

    def remove_tag(self, tag):
        self.tags = [t for t in self.tags if t.value != tag]

    def __str__(self):
        tags_str = "; ".join(t.value for t in self.tags) if self.tags else "No tags"
        deadline_str = (
            str(self.deadline) if self.deadline is not None else "Date is not defined"
        )
        return (
            f"Title: {self.title.value}, "
            f"Tags: {tags_str}, "
            f"Note: {self.content.value}, "
            f"Date of creation: {str(self.creation_date)}, "
            f"Date of deadline: {deadline_str}"
        )

    def add_deadline(self, deadline):
        self.deadline = NoteDeadline(deadline)

    def to_json(self):
        return {
            "title": self.title.value,
            "tags": [tag.value for tag in self.tags],
            "note": self.content.value,
            "date_of_creation": str(self.creation_date),
            "deadline": str(self.deadline) if self.deadline else None,
        }

    def from_json(data):
        record = NoteRecord(data["title"], data["note"])
        for tag in data["tags"]:
            record.add_tag(tag)
        record.creation_date = datetime.strptime(
            data["date_of_creation"], "%d.%m.%Y"
        ).date()
        if data["deadline"]:
            record.add_deadline(data["deadline"])
        return record


class NoteBook(UserDict):
    def add_note(self, title, note):
        if title not in self.data:
            self.data[title] = NoteRecord(title, note)
            print(f"Note {title} added succesfully")
        else:
            print(f"Note with title {title} already exist. Choose another title")

    def change_note(self, title, note):
        if title in self.data:
            self.data[title].content = note
            console.print(f"Note {title} changed", style="green")
        else:
            console.print(f"Note {title} not found. Create new note", style="red")

    def add_tag(self, title, tag):
        if title in self.data:
            self.data[title].add_tag(tag)
            print(f"Tag {tag} added to note {title}")
        else:
            print(f"Note with title {title} not found.")

    def delete_tag(self, title, tag):
        if title in self.data:
            self.data[title].remove_tag(tag)
            print(f"Tag {tag} deleted from note {title}")
        else:
            print(f"Note with title {title} not found.")

    def change_tag(self, title, tag, new_tag):
        if title in self.data():
            self.data[title].remove_tag(tag)
            self.data[title].add_tag(new_tag)
            console.print(f"Tags updated", style="green")
        else:
            console.print(f"Note {title} not found.", style="red")

    def find_by_title(self, title):
        return self.data.get(title)

    def find_by_tag(self, tag):
        return [
            note for note in self.data.values() if tag in [t.value for t in note.tags]
        ]

    def delete_note(self, title):
        if title in self.data:
            self.data.pop(title)
            print(f"Note {title} deleted successfully.")
        else:
            print(f"Note {title} not found.")

    def add_deadline(self, title, date):
        if title in self.data:
            self.data[title].add_deadline(date)
            print(f"Deadline for note {title} added successfully.")
        else:
            print(f"Note with title {title} not found.")
    
    def to_do_list(self,days):
        to_do_list(self,days)

    def sort_notes_by_tags(self):
        sorted_by_tags = defaultdict(list)
        for note in self.data.values():
            if note.tags:
                for tag in note.tags:
                    sorted_by_tags[tag.value].append(note.content.value)
            else:
                sorted_by_tags["Without tags"].append(note.content.value)
        for tag, notes in sorted_by_tags.items():
            print(f"{tag}: {'; '.join(notes)}")
       
    
    def save_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                data = {title: note.to_json() for title, note in self.data.items()}
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
                for title, note_data in data.items():
                    self.data[title] = NoteRecord.from_json(note_data)
                print("Adress book is loaded from file")
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
        except PermissionError:
            print("Access to file is denied. Creating a new address book.")
        except Exception as e:
            print(f"Error by loadind file. Creating a new address book: {e}.")
