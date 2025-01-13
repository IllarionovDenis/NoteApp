from PyQt5.QtWidgets import QApplication
from main_form import MainForm

if __name__ == "__main__":
    app = QApplication([])

    window = MainForm()

    window.show()

    app.exec_()