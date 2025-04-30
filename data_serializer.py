import json
from note import Note

class DataSerializer:
    @staticmethod
    def save_to_file(data, filename: str):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([note.to_dict() for note in data], file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from_file(filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return [Note.from_dict(item) for item in json.load(file)]
        except FileNotFoundError:
            print("Файл не найден. Будет создан новый.")
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Файл будет очищен.")
            return []

    @staticmethod
    def save(data, filename="notes_data.json"):
        DataSerializer.save_to_file(data, filename)

    @staticmethod
    def load(filename="notes_data.json"):
        return DataSerializer.load_from_file(filename)