from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from datetime import datetime
import db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import utils

# Кастомный класс для элементов таблицы с правильной сортировкой
class CustomTreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        col = self.treeWidget().sortColumn()  # Текущий столбец сортировки
        if col == 3:  # Столбец "Сумма"
            try:
                # Преобразуем текст "Суммы" в float, убирая пробелы и заменяя запятую на точку
                self_value = float(self.text(3).replace(" ", "").replace(",", "."))
                other_value = float(other.text(3).replace(" ", "").replace(",", "."))
                return self_value < other_value
            except ValueError:
                # Если преобразование не удалось, сравниваем как строки
                return self.text(3) < other.text(3)
        else:
            # Для остальных столбцов сравниваем как строки (в нижнем регистре)
            return self.text(col).lower() < other.text(col).lower()

class AppViews:
    def __init__(self, app):
        self.app = app

    def update_balance(self, balance_label, transaction_type):
        new_balance = utils.format_balance(db.get_balance())
        balance_label.setText(f"Баланс: {new_balance} ₽")

    def show_add_transaction(self, content_widget):
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_widget.setStyleSheet("background-color: #2E2E2E;")

        type_label = QLabel("Тип:")
        type_label.setStyleSheet("color: white; font-size: 18px;")
        form_layout.addWidget(type_label)
        type_combo = QComboBox()
        type_combo.addItems(["Доход", "Расход"])
        type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3E3E3E;
                color: white;
                padding: 8px;
                font-size: 16px;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                width: 20px;
                border: none;
                background: #5E5E5E;
                border-radius: 5px;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        form_layout.addWidget(type_combo)

        amount_label = QLabel("Сумма:")
        amount_label.setStyleSheet("color: white; font-size: 18px;")
        form_layout.addWidget(amount_label)
        amount_entry = QLineEdit()
        amount_entry.setPlaceholderText("Введите сумму")
        amount_entry.setStyleSheet("background-color: #3E3E3E; color: white; padding: 8px; font-size: 16px; border-radius: 5px;")
        form_layout.addWidget(amount_entry)

        date_label = QLabel("Дата:")
        date_label.setStyleSheet("color: white; font-size: 18px;")
        form_layout.addWidget(date_label)
        date_entry = QLineEdit()
        date_entry.setText(datetime.now().strftime("%Y-%m-%d"))
        date_entry.setStyleSheet("background-color: #3E3E3E; color: white; padding: 8px; font-size: 16px; border-radius: 5px;")
        form_layout.addWidget(date_entry)

        category_label = QLabel("Категория:")
        category_label.setStyleSheet("color: white; font-size: 18px;")
        form_layout.addWidget(category_label)
        category_combo = QComboBox()
        category_combo.addItems(db.get_categories())
        category_combo.setStyleSheet("""
            QComboBox {
                background-color: #3E3E3E;
                color: white;
                padding: 8px;
                font-size: 16px;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                width: 20px;
                border: none;
                background: #5E5E5E;
                border-radius: 5px;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        form_layout.addWidget(category_combo)

        desc_label = QLabel("Описание:")
        desc_label.setStyleSheet("color: white; font-size: 18px;")
        form_layout.addWidget(desc_label)
        desc_entry = QLineEdit()
        desc_entry.setPlaceholderText("Введите описание")
        desc_entry.setStyleSheet("background-color: #3E3E3E; color: white; padding: 8px; font-size: 16px; border-radius: 5px;")
        form_layout.addWidget(desc_entry)

        error_label = QLabel("")
        error_label.setStyleSheet("color: red; font-size: 16px;")
        form_layout.addWidget(error_label)

        def save_transaction():
            try:
                amount_text = amount_entry.text().strip()
                if not amount_text:
                    raise ValueError("Сумма не указана")
                amount = round(float(amount_text), 2)
                date = date_entry.text().strip()
                if not date:
                    raise ValueError("Дата не указана")
                datetime.strptime(date, "%Y-%m-%d")  # Проверка формата даты
                transaction_type = type_combo.currentText()
                db.add_transaction(transaction_type, amount, date, category_combo.currentText(), desc_entry.text())
                self.app.last_transaction_type = transaction_type
                self.app.update_balance()
                error_label.setText("Транзакция добавлена")
                error_label.setStyleSheet("color: green; font-size: 16px;")
                amount_entry.clear()
                desc_entry.clear()
            except ValueError as e:
                error_label.setText(f"Ошибка: {str(e)}")
                error_label.setStyleSheet("color: red; font-size: 16px;")

        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet("background-color: #3E3E3E; color: white; border-radius: 12px; padding: 15px; font-size: 18px;")
        save_button.clicked.connect(save_transaction)
        form_layout.addWidget(save_button)

        form_layout.addStretch()
        content_widget.layout().addWidget(form_widget)

    def show_charts(self, content_widget):
        data = db.get_expense_data()
        if data:
            categories, amounts = zip(*data)
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors,
                   textprops={'fontsize': 14, 'color': 'white'})
            ax.set_title("Расходы по категориям", color="white", fontsize=18)
            fig.patch.set_facecolor("#2E2E2E")
            ax.set_facecolor("#2E2E2E")
            canvas = FigureCanvas(fig)
            content_widget.layout().addWidget(canvas)
        else:
            label = QLabel("Нет данных для графика")
            label.setStyleSheet("color: red; font-size: 16px;")
            content_widget.layout().addWidget(label)

    def show_history(self, content_widget):
        tree_widget = QTreeWidget()
        tree_widget.setStyleSheet("""
            QTreeWidget { background-color: #2E2E2E; color: white; font-size: 16px; }
            QTreeWidget::item:selected { background-color: #3E3E3E; }
            QHeaderView::section { background-color: #1E1E1E; color: white; font-size: 16px; padding: 5px; }
        """)
        tree_widget.setHeaderLabels(["Дата", "Тип", "Категория", "Сумма", "Описание"])
        tree_widget.header().setStyleSheet("QHeaderView::section { background-color: #1E1E1E; color: white; font-size: 16px; padding: 5px; }")
        tree_widget.setColumnWidth(0, 120)
        tree_widget.setColumnWidth(1, 100)
        tree_widget.setColumnWidth(2, 120)
        tree_widget.setColumnWidth(3, 120)
        tree_widget.setColumnWidth(4, 240)

        tree_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tree_widget.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: #2E2E2E;
                width: 14px;
                border-radius: 7px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #5E5E5E;
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #2E2E2E;
            }
        """)

        history = sorted(db.get_history(), key=lambda x: x[0], reverse=True)
        for row in history:
            item = CustomTreeWidgetItem([row[0], row[1], row[2], utils.format_balance(row[3]), row[4]])
            tree_widget.addTopLevelItem(item)

        tree_widget.setSortingEnabled(True)
        tree_widget.sortItems(0, Qt.DescendingOrder)

        content_widget.layout().addWidget(tree_widget)