import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton

class PDFSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Seçici')
        self.setGeometry(100, 100, 300, 100)

        select_button = QPushButton('PDF Seç', self)
        select_button.clicked.connect(self.showDialog)

    def showDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        fileName, _ = QFileDialog.getOpenFileName(self, 'PDF Dosyasını Seç', '', 'PDF Dosyaları (*.pdf);;Tüm Dosyalar (*)', options=options)

        if fileName:
            with open(fileName, 'rb') as file:
                pdf_data = file.read()
            # Şimdi pdf_data içinde PDF dosyasının verisini tutabilirsiniz.
            print('PDF Verisi Alındı.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFSelector()
    ex.show()
    sys.exit(app.exec_())
