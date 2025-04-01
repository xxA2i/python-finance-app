from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
import db
import views
import utils

class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личные финансы")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: #2E2E2E;")

        # Инициализация базы данных
        db.init_db()

        # Главный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Боковая панель
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2E2E2E;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(QLabel("Меню", alignment=Qt.AlignCenter, styleSheet="font-size: 24px; color: white;"))

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet("background-color: #3E3E3E; color: white; border-radius: 12px; padding: 15px; font-size: 18px;")
        self.add_button.clicked.connect(self.show_add_transaction)
        sidebar_layout.addWidget(self.add_button)

        self.chart_button = QPushButton("Графики")
        self.chart_button.setStyleSheet("background-color: #3E3E3E; color: white; border-radius: 12px; padding: 15px; font-size: 18px;")
        self.chart_button.clicked.connect(self.show_charts)
        sidebar_layout.addWidget(self.chart_button)

        self.history_button = QPushButton("История")
        self.history_button.setStyleSheet("background-color: #3E3E3E; color: white; border-radius: 12px; padding: 15px; font-size: 18px;")
        self.history_button.clicked.connect(self.show_history)
        sidebar_layout.addWidget(self.history_button)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Главная область
        self.main_frame = QWidget()
        self.main_frame.setStyleSheet("background-color: #2E2E2E; border-radius: 12px;")
        main_layout.addWidget(self.main_frame)
        self.main_layout = QVBoxLayout(self.main_frame)
        self.balance_label = QLabel(f"Баланс: {utils.format_balance(db.get_balance())} ₽", alignment=Qt.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 32px; color: white;")
        self.main_layout.addWidget(self.balance_label)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.views = views.AppViews(self)
        self.show_add_transaction()
        self.last_transaction_type = None

    def update_balance(self):
        self.views.update_balance(self.balance_label, self.last_transaction_type)

    def show_add_transaction(self):
        self.clear_content()
        self.views.show_add_transaction(self.content_widget)

    def show_charts(self):
        self.clear_content()
        self.views.show_charts(self.content_widget)

    def show_history(self):
        self.clear_content()
        self.views.show_history(self.content_widget)

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()