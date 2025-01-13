import json
from note import Note

class DataSerializer:
    @staticmethod
    def save_to_file(data, filename: str):
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
        return DataSerializer.load_from_file(filename)
