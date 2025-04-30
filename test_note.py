import pytest
import datetime
from note import Note


def test_note_initialization():
    note = Note("Initial Title", "Content")
    modified_at_before = note.modified_at

    note.title = "Updated Title"
    assert note.title == "Updated Title"
    assert note.modified_at > modified_at_before

    # Тест ошибки при пустом заголовке
    with pytest.raises(ValueError):
        note.title = ""


def test_note_content_setter():
    note = Note("Title", "Content", category="Дом")
    modified_at_before = note.modified_at

    note.category = "Работа"
    assert note.category == "Работа"
    assert note.modified_at > modified_at_before


def test_note_to_string():
    note = Note("Title", "Content", category="Люди")
    note_dict = note.to_dict()

    assert note_dict["title"] == "Title"
    assert note_dict["content"] == "Content"
    assert note_dict["category"] == "Люди"
    assert isinstance(note_dict["created_at"], str)
    assert isinstance(note_dict["modified_at"], str)


def test_note_from_dict():
    
    note_data = {
        "title": "Title",
        "content": "Content",
        "category": "Финансы",
        "created_at": datetime.datetime.now().isoformat(),
        "modified_at": datetime.datetime.now().isoformat()
    }
    note = Note.from_dict(note_data)

    assert note.title == "Title"
    assert note.content == "Content"
    assert note.category == "Финансы"
    assert note.created_at.isoformat() == note_data["created_at"]
    assert note.modified_at.isoformat() == note_data["modified_at"]
