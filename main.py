import sys
from PySide6.QtWidgets import QApplication
from ui import FinanceApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec())