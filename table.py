import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

# Örnek veri
lessons = [
    {
        "ders_kodu": "101",
        "ders_adi": "Matematik",
        "ders_statusu": "Aktif",
        "ogretim_dili": "Türkçe",
        "AKTS": "4",
        "not": "A"
    },
    {
        "ders_kodu": "202",
        "ders_adi": "Fizik",
        "ders_statusu": "Pasif",
        "ogretim_dili": "İngilizce",
        "AKTS": "5",
        "not": "B"
    },
]

class TableExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ders Tablosu")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(lessons))
        self.tableWidget.setColumnCount(len(lessons[0]))
        self.tableWidget.setHorizontalHeaderLabels(["Ders Kodu", "Ders Adı", "Ders Durumu", "Öğretim Dili", "AKTS", "Not"])

        for row, lesson in enumerate(lessons):
            for col, value in enumerate(lesson.values()):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.central_widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = TableExample()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
