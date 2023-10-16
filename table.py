import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt  # Qt ifadesini ekleyin

class DataTable(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle('Veri Tablosu')
        self.setGeometry(100, 100, 600, 400)

        # Veri tablosunu oluştur
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(50, 50, 500, 300)
        
        # Veriyi tabloya ekle
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                item.setFlags(item.flags() ^  Qt.ItemIsEditable)  # Düzenleme yeteneğini devre dışı bırak
                self.tableWidget.setItem(row_idx, col_idx, item)

def main(data):
    app = QApplication(sys.argv)
    window = DataTable(data)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Örnek bir veri listesi (2D array)
    data = [
        ['Ad', 'Soyad', 'Yaş'],
        ['John', 'Doe', 30],
        ['Jane', 'Smith', 25],
        ['Bob', 'Johnson', 40]
    ]

    main(data)
