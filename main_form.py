import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel,
    QComboBox, QListWidget, QDialog, QDialogButtonBox, QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor 
from note import Note
from data_serializer import DataSerializer

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Название программы
        app_name_label = QLabel("NoteApp", self)
        app_name_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(app_name_label)

        # Имя автора
        author_label = QLabel("Автор: Илларионов Д.", self)
        author_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(author_label)

        # Почта
        email_label = QLabel('<a href="mailto:dencsch@mail.ru">Почта: dencsch@mail.ru</a>', self)
        email_label.setOpenExternalLinks(True)
        email_label.setStyleSheet("font-size: 12pt; color: blue;")
        layout.addWidget(email_label)

        # GitHub
        github_label = QLabel('<a href="https://github.com/IllarionovDenis/NoteApp">GitHub: https://github.com/IllarionovDenis/NoteApp</a>', self)
        github_label.setOpenExternalLinks(True)
        github_label.setStyleSheet("font-size: 12pt; color: blue;")
        layout.addWidget(github_label)

        # Кнопка закрытия
        close_button = QDialogButtonBox(QDialogButtonBox.Ok)
        close_button.accepted.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)


class NoteEditorDialog(QDialog):
    def __init__(self, note=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактор заметок" if note else "Создать заметку")
        self.note = note

        layout = QVBoxLayout()

        # Поле для ввода заголовка
        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText("Введите заголовок")
        layout.addWidget(QLabel("Заголовок:"))
        layout.addWidget(self.title_edit)

        # Поле для ввода содержимого
        self.content_edit = QTextEdit(self)
        self.content_edit.setPlaceholderText("Введите содержимое (минимум 5 символов)")

        layout.addWidget(QLabel("Содержимое:"))
        layout.addWidget(self.content_edit)

        # Выпадающий список для выбора категории
        self.category_combo = QComboBox(self)
        self.category_combo.addItems(["Все", "Работа", "Дом", "Здоровье и Спорт", "Люди", "Документы", "Финансы", "Разное"])
        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.category_combo)

        # Отображение даты создания заметки
        self.date_label = QLabel(self)
        layout.addWidget(QLabel("Дата создания:"))
        layout.addWidget(self.date_label)

        # Кнопки сохранения и отмены
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        # Если передана заметка, заполняем поля
        if self.note:
            self.title_edit.setText(note.title)
            self.content_edit.setText(note.content)
            self.category_combo.setCurrentText(note.category)
            self.date_label.setText(note.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            self.date_label.setText("Создаётся сейчас")

    def validate_input(self):
        valid = True
        palette = self.title_edit.palette()

        # Проверка заголовка
        if not self.title_edit.text().strip():
            valid = False
            palette.setColor(QPalette.Base, QColor("red"))
        elif len(self.title_edit.text().strip()) > 20:
            valid = False
            palette.setColor(QPalette.Base, QColor("red"))
        else:
            palette.setColor(QPalette.Base, QColor("green"))
        self.title_edit.setPalette(palette)

        # Проверка содержимого
        content_palette = self.content_edit.palette()
        if len(self.content_edit.toPlainText().strip()) < 5:
            valid = False
            content_palette.setColor(QPalette.Base, QColor("red"))
        else:
            content_palette.setColor(QPalette.Base, QColor("green"))
        self.content_edit.setPalette(content_palette)

        return valid

    def accept(self):
        if not self.validate_input():
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return
        super().accept()

    def get_note_data(self):
        return {
            "title": self.title_edit.text(),
            "content": self.content_edit.toPlainText(),
            "category": self.category_combo.currentText(),
        }


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoteApp")
        self.resize(900, 600)  # Увеличен размер окна
        self.layout = QVBoxLayout(self)
        self.notes = []
        self.load_notes()

        # Список заметок
        self.note_list = QListWidget(self)
        self.note_list.itemClicked.connect(self.show_note_content)
        self.note_list.itemDoubleClicked.connect(self.edit_note)
        self.layout.addWidget(self.note_list)


        # Выпадающий список сортировки
        self.sort_combo = QComboBox(self)
        self.sort_combo.addItems(["Сортировка: По имени", "Сортировка: По дате"])
        self.sort_combo.currentIndexChanged.connect(self.sort_notes)
        self.layout.addWidget(self.sort_combo)

        # Выпадающий список категорий
        self.category_combo = QComboBox(self)
        self.category_combo.addItems(["Все", "Работа", "Дом", "Здоровье и Спорт", "Люди", "Документы", "Финансы", "Разное"])
        self.category_combo.currentIndexChanged.connect(self.filter_by_category)
        self.layout.addWidget(self.category_combo)

        # Поле поиска
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Поиск по заголовкам...")
        self.search_bar.textChanged.connect(self.filter_notes)
        self.layout.addWidget(self.search_bar)

        # Фрейм с подробной информацией о заметке
        self.content_frame = QFrame(self)
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_layout = QVBoxLayout(self.content_frame)

        self.content_title_label = QLabel("Заголовок: (не выбран)")
        self.content_layout.addWidget(self.content_title_label)

        self.content_body_label = QLabel("Содержимое: (не выбрано)")
        self.content_layout.addWidget(self.content_body_label)

        self.content_category_label = QLabel("Категория: (не выбрано)")
        self.content_layout.addWidget(self.content_category_label)

        self.content_created_label = QLabel("Дата создания: (не выбрано)")
        self.content_layout.addWidget(self.content_created_label)

        self.content_modified_label = QLabel("Дата модификации: (не выбрано)")
        self.content_layout.addWidget(self.content_modified_label)

        self.layout.addWidget(self.content_frame)

        # Панель кнопок
        button_layout = QHBoxLayout()
        add_button = QPushButton("Создать заметку", self)
        add_button.clicked.connect(self.add_note)
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Удалить выбранную заметку", self)
        delete_button.clicked.connect(self.delete_note)
        button_layout.addWidget(delete_button)

        about_button = QPushButton("О программе", self)  # Кнопка "Автор"
        about_button.clicked.connect(self.show_about_dialog)
        button_layout.addWidget(about_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
        self.refresh_note_list()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()


    def load_notes(self):
        try:
            self.notes = DataSerializer.load()
        except Exception as e:
            self.notes = []

    def save_notes(self):
        DataSerializer.save(self.notes)

    def refresh_note_list(self):
        self.note_list.clear()
        for note in self.notes:
            self.note_list.addItem(f"{note.title} ({note.category}) - {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def add_note(self):
        dialog = NoteEditorDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_note_data()
            note = Note(title=data["title"], content=data["content"], category=data["category"])
            self.notes.append(note)
            self.save_notes()
            self.refresh_note_list()

    def edit_note(self, item):
        index = self.note_list.row(item)
        note = self.notes[index]
        dialog = NoteEditorDialog(note=note, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_note_data()
            note.title = data["title"]
            note.content = data["content"]
            note.category = data["category"]
            self.save_notes()
            self.refresh_note_list()

    def delete_note(self):
        current_item = self.note_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для удаления.")
            return

        index = self.note_list.row(current_item)
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить заметку '{self.notes[index].title}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.notes[index]
            self.save_notes()
            self.refresh_note_list()

    def filter_notes(self):
        query = self.search_bar.text().lower()
        self.note_list.clear()
        for note in self.notes:
            if query in note.title.lower():
                self.note_list.addItem(f"{note.title} ({note.category}) - {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def filter_by_category(self):
        selected_category = self.category_combo.currentText()
        self.note_list.clear()
        for note in self.notes:
            if selected_category == "Все" or note.category == selected_category:
                self.note_list.addItem(f"{note.title} ({note.category}) - {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def sort_notes(self):
        if self.sort_combo.currentText() == "Сортировка: По имени":
            self.notes.sort(key=lambda note: note.title)
        elif self.sort_combo.currentText() == "Сортировка: По дате":
            self.notes.sort(key=lambda note: note.created_at)
        self.refresh_note_list()

    def show_note_content(self, item):
        index = self.note_list.row(item)
        note = self.notes[index]
        self.content_title_label.setText(f"Заголовок: {note.title}")
        self.content_body_label.setText(f"Содержимое: {note.content}")
        self.content_category_label.setText(f"Категория: {note.category}")
        self.content_created_label.setText(f"Дата создания: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if note.modified_at != note.created_at:
            self.content_modified_label.setText(f"Дата модификации: {note.modified_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.content_modified_label.setText("Дата модификации: Не изменено")
