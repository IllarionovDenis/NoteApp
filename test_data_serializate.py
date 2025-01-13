import pytest
import json
import datetime
from note import Note


def test_note_serialization():
    # Создание заметки
    note = Note("Test Title", "Test Content", category="Работа")

    # Преобразование заметки в словарь
    note_dict = note.to_dict()

    # Преобразование словаря в JSON
    note_json = json.dumps(note_dict)

    # Проверки
    assert isinstance(note_json, str)
    deserialized_data = json.loads(note_json)

    assert deserialized_data["title"] == "Test Title"
    assert deserialized_data["content"] == "Test Content"
    assert deserialized_data["category"] == "Работа"
    assert "created_at" in deserialized_data
    assert "modified_at" in deserialized_data


def test_note_deserialization():
    # Подготовка данных заметки
    note_data = {
        "title": "Title",
        "content": "Content",
        "category": "Дом",
        "created_at": datetime.datetime.now().isoformat(),
        "modified_at": datetime.datetime.now().isoformat()
    }

    # Преобразование данных в JSON
    note_json = json.dumps(note_data)

    # Десериализация JSON в словарь
    deserialized_data = json.loads(note_json)

    # Создание объекта Note из словаря
    note = Note.from_dict(deserialized_data)

    # Проверки
    assert note.title == "Title"
    assert note.content == "Content"
    assert note.category == "Дом"
    assert note.created_at.isoformat() == note_data["created_at"]
    assert note.modified_at.isoformat() == note_data["modified_at"]


def test_note_modification():
    # Создание заметки
    note = Note("Original Title", "Original Content", category="Финансы")
    original_modified_at = note.modified_at

    # Изменение заголовка и содержимого
    note.title = "Updated Title"
    note.content = "Updated Content"

    # Проверки
    assert note.title == "Updated Title"
    assert note.content == "Updated Content"
    assert note.category == "Финансы"
    assert note.modified_at > original_modified_at


def test_note_category_change():
    # Создание заметки
    note = Note("Test Title", "Test Content", category="Разное")

    # Изменение категории
    note.category = "Здоровье и Спорт"

    # Проверки
    assert note.category == "Здоровье и Спорт"
