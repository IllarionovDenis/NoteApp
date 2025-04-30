from note import Note

class NoteCategory:
    def __init__(self, name: str):
        self._name = name  # Название категории
        self.notes = []  # Список заметок в категории

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Название категории не может быть пустым.")
        self._name = value

    def add_note(self, note: Note):
        if not isinstance(note, Note):
            raise ValueError("Можно добавлять только объекты типа Note.")
        self.notes.append(note)

    def remove_note_by_title(self, title: str):
        self.notes = [note for note in self.notes if note.title != title]

    def get_notes(self):
        return self.notes
