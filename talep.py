import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QFont

class DersTablosu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ders Tablosu")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Ders adları listesi
        self.ders_adlari = ["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih"]

        
        
        # Tablo oluştur
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(2)
        self.tablo.setRowCount(len(self.ders_adlari))
        self.tablo.setColumnWidth(1, 210)
        
        # Tablo başlıklarının yazı fontunu oluşturun ve ayarlayın
        font = QFont()
        font.setBold(True)  # Kalın font
        font.setPointSize(8)  # Font boyutu

        # Tabloya başlık etiketlerini eklerken bu fontu kullanın
        self.tablo.setHorizontalHeaderLabels(["Ders Adları", "Talep Edilebilecek Hoca Sayısı"])
        header = self.tablo.horizontalHeader()
        for i in range(self.tablo.columnCount()):
            header.setFont(font)
        
        for row, ders_adi in enumerate(self.ders_adlari):
            self.tablo.setItem(row, 0, QTableWidgetItem(ders_adi))
            self.tablo.setItem(row, 1, QTableWidgetItem("1"))

            # Birinci sütun değiştirilemez
            self.tablo.item(row, 0).setFlags(QtCore.Qt.ItemIsEnabled)

        self.layout.addWidget(self.tablo)

        # Kaydet butonu
        self.kaydet_buton = QPushButton("Kaydet")
        self.kaydet_buton.clicked.connect(self.kaydet)
        self.layout.addWidget(self.kaydet_buton)

        self.central_widget.setLayout(self.layout)

    def kaydet(self):
        ders_hoca_dict = {}
        for row in range(len(self.ders_adlari)):
            ders_adi = self.tablo.item(row, 0).text()
            talep_hoca_sayisi = int(self.tablo.item(row, 1).text())
            ders_hoca_dict[ders_adi] = talep_hoca_sayisi

        print(ders_hoca_dict)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DersTablosu()
    window.show()
    sys.exit(app.exec_())
