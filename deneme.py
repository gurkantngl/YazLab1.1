import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox

# Örnek veriler
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

class StudentPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Öğrenci Paneli")
        self.setGeometry(100, 100, 600, 400)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(100, 100, 400, 200)  # Tablo boyutu ve konumu
        self.tableWidget.setRowCount(len(lessons))
        self.tableWidget.setColumnCount(len(lessons[0]))
        self.tableWidget.setHorizontalHeaderLabels(["Ders Kodu", "Ders Adı", "Ders Durumu", "Öğretim Dili", "AKTS", "Not"])

        for row, lesson in enumerate(lessons):
            for col, value in enumerate(lesson.values()):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)

        # ComboBox eklemek için yeni bir sütun ekleyin
        comboColumn = 6
        self.tableWidget.setColumnCount(self.tableWidget.columnCount() + 1)
        self.tableWidget.setHorizontalHeaderItem(comboColumn, QTableWidgetItem("Seçenekler"))

        for row in range(self.tableWidget.rowCount()):
            combo = QComboBox()
            combo.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])
            self.tableWidget.setCellWidget(row, comboColumn, combo)

def main():
    app = QApplication(sys.argv)
    window = StudentPanel()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
