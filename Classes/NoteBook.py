from collections import UserDict, defaultdict
from datetime import datetime
from Classes.Classes_for_secretary import (
    NoteTitle,
    NoteContent,
    NoteDeadline,
    NoteTag,
)


class NoteRecord:
    def __init__(self, title, content):
        self.title = NoteTitle(title)
        self.content = NoteContent(content)
        self.creation_date = datetime.today().date()
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
            print(f"Note {title} changed")
        else:
            print(f"Note {title} not found. Create new note")

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
            print(f"Tags updated")
        else:
            print(f"Note {title} not found.")

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

    def sort_notes_by_tags(self):
        sorted_by_tags = defaultdict(list)
        for note in self.data.values():
            if note.tags:
                for tag in note.tags:
                    sorted_by_tags[tag.value].append(note.content)
            else:
                sorted_by_tags["Without tags"].append(note.content)
        return dict(sorted_by_tags)
