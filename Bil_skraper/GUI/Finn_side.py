"""
Hoved siden på 
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Example")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Item 1", "Item 2", "Item 3"])
        layout.addWidget(self.dropdown)

        for i in range(5):
            button = QPushButton(f"Button {i + 1}")
            layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_win = MainWindow()
    main_win.show()

    sys.exit(app.exec())
