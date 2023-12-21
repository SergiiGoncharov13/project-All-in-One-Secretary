from rich.console import Console
from collections import UserDict, defaultdict
from datetime import datetime
from Classes.Classes_for_secretary import (
    NoteTitle,
    NoteContent,
    NoteDeadline,
    NoteTag,
)

console = Console()

class NoteRecord:
    """
    Represents a record in the notebook.
    """

    def __init__(self, title, content):
        self.title = NoteTitle(title)
        self.content = NoteContent(content)
        self.creation_date = datetime.today().date()
        self.tags = []
        self.deadline = None

    def add_tag(self, tag):
        """
        Add a tag to the note.
        """
        if tag not in [t.value for t in self.tags]:
            self.tags.append(NoteTag(tag))

    def remove_tag(self, tag):
        """
        Remove a tag from the note.
        """
        self.tags = [t for t in self.tags if t.value != tag]

    def __str__(self):
        """
        String representation of the note.
        """
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
        """
        Add a deadline to the note.
        """
        self.deadline = NoteDeadline(deadline)

    def to_json(self):
        """
        Convert the note to JSON format.
        """
        return {
            "title": self.title.value,
            "tags": [tag.value for tag in self.tags],
            "note": self.content.value,
            "date_of_creation": str(self.creation_date),
            "deadline": str(self.deadline) if self.deadline else None,
        }

    @classmethod
    def from_json(cls, data):
        """
        Create a NoteRecord instance from JSON data.
        """
        record = cls(data["title"], data["note"])
        for tag in data["tags"]:
            record.add_tag(tag)
        record.creation_date = datetime.strptime(
            data["date_of_creation"], "%d.%m.%Y"
        ).date()
        if data["deadline"]:
            record.add_deadline(data["deadline"])
        return record

class NoteBook(UserDict):
    """
    Represents a collection of notes.
    """

    def add_note(self, title, note):
        """
        Add a note to the notebook.
        """
        if title not in self.data:
            self.data[title] = NoteRecord(title, note)
            print(f"Note {title} added successfully")
        else:
            print(f"Note with title {title} already exists. Choose another title")

    def change_note(self, title, note):
        """
        Change the content of a note in the notebook.
        """
        if title in self.data:
            self.data[title].content = note
            console.print(f"Note {title} changed", style="green")
        else:
            console.print(f"Note {title} not found. Create a new note", style="red")

    def add_tag(self, title, tag):
        """
        Add a tag to a note in the notebook.
        """
        if title in self.data:
            self.data[title].add_tag(tag)
            print(f"Tag {tag} added to note {title}")
        else:
            print(f"Note with title {title} not found.")

    def delete_tag(self, title, tag):
        """
        Delete a tag from a note in the notebook.
        """
        if title in self.data:
            self.data[title].remove_tag(tag)
            print(f"Tag {tag} deleted from note {title}")
        else:
            print(f"Note with title {title} not found.")

    def change_tag(self, title, tag, new_tag):
        """
        Change a tag on a note in the notebook.
        """
        if title in self.data:
            self.data[title].remove_tag(tag)
            self.data[title].add_tag(new_tag)
            console.print(f"Tags updated", style="green")
        else:
            console.print(f"Note {title} not found.", style="red")

    def find_by_title(self, title):
        """
        Find a note in the notebook by its title.
        """
        return self.data.get(title)

    def find_by_tag(self, tag):
        """
        Find notes in the notebook by a tag.
        """
        return [
            note for note in self.data.values() if tag in [t.value for t in note.tags]
        ]

    def delete_note(self, title):
        """
        Delete a note from the notebook.
        """
        if title in self.data:
            self.data.pop(title)
            print(f"Note {title} deleted successfully.")
        else:
            print(f"Note {title} not found.")

    def add_deadline(self, title, date):
        """
        Add a deadline to a note in the notebook.
        """
        if title in self.data:
            self.data[title].add_deadline(date)
            print(f"Deadline for note {title} added successfully.")
        else:
            print(f"Note with title {title} not found.")

    def sort_notes_by_tags(self):
        """
        Sort notes in the notebook by tags.
        """
        sorted_by_tags = defaultdict(list)
        for note in self.data.values():
            if note.tags:
                for tag in note.tags:
                    sorted_by_tags[tag.value].append(note.content)
            else:
                sorted_by_tags["Without tags"].append(note.content)
        return dict(sorted_by_tags)
