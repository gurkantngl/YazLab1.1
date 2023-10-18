import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from loginPanel import LoginPanel

class StudentPanel(QWidget):
    def __init__(self):
        
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.arr = []
        
        # Panelin arka plan rengini değiştir
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle('Yönetici Paneli')
        self.move(600, 200)
        self.setFixedSize(800, 600)

         
        self.lblTitle = QLabel('Yönetici Paneli', self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(12)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")

        """ 
            - Her bir ders için kaç farklı hocadan talep oluşturulabilir +
            - Öğrenci ve hoca arasında mesajlaşma karakter sayısı +
            - Bir hoca kaç öğrencinin talebini onaylayabilir +
            - (Kontenjan miktarı bir hocadan ders alabilecek toplam öğrenci sayısına karşılık gelmektedir. Bir hocanın farklı iki dersini alan aynı öğrenciler 2 öğrenci gibi düşünülerek kontenjandan düşülmelidir Her ders için ayrı kontenjan olmamalıdır.)
            - 1.Aşama süresi 
        """
        
        
        
        self.lblRequestNum = QLabel('Bir öğrenci kaç farklı hocadan talep oluşturabilir:', self)
        self.lblRequestNum.move(20, 180)
        self.myFont.setPointSize(9)
        self.lblRequestNum.setFont(self.myFont)
        self.lblRequestNum.setStyleSheet("color : white")
        self.arr.append(self.lblRequestNum)
        
        self.txtRequestNum = QLineEdit(self)
        self.txtRequestNum.move(370, 180)
        self.txtRequestNum.resize(200, 30)
        self.txtRequestNum.setPlaceholderText('Talep sayısı girin...')
        self.txtRequestNum.setStyleSheet("color : black; background-color: white")
        self.arr.append(self.txtRequestNum)
        
        self.lblChar = QLabel('Mesajlaşma karakter sayısı:', self)
        self.lblChar.move(170, 240)
        self.myFont.setPointSize(9)
        self.lblChar.setFont(self.myFont)
        self.lblChar.setStyleSheet("color : white")
        self.arr.append(self.lblChar)
        
        self.txtChar = QLineEdit(self)
        self.txtChar.move(370, 240)
        self.txtChar.resize(200, 30)
        self.txtChar.setPlaceholderText('Karakter sayısı girin...')
        self.txtChar.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChar)
        
        self.lblConfirmNum = QLabel('Bir hoca kaç öğrencinin talebini onaylayabilir:', self)
        self.lblConfirmNum.move(45, 300)
        self.myFont.setPointSize(9)
        self.lblConfirmNum.setFont(self.myFont)
        self.lblConfirmNum.setStyleSheet("color : white")
        self.arr.append(self.lblConfirmNum)
        
        self.txtConfirmNum = QLineEdit(self)
        self.txtConfirmNum.move(370, 300)
        self.txtConfirmNum.resize(200, 30)
        self.txtConfirmNum.setPlaceholderText('Öğrenci sayısı girin...')
        self.txtConfirmNum.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtConfirmNum)
        
        self.lblTime = QLabel('1. Aşama süresi:', self)
        self.lblTime.move(250, 360)
        self.myFont.setPointSize(9)
        self.lblTime.setFont(self.myFont)
        self.lblTime.setStyleSheet("color : white")
        self.arr.append(self.lblTime)
        
        self.txtTime = QLineEdit(self)
        self.txtTime.move(370, 360)
        self.txtTime.resize(200, 30)
        self.txtTime.setPlaceholderText('Süre girin...')
        self.txtTime.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtTime)
        
        
        
        self.myFont.setPointSize(11)
        self.btnStart = QPushButton(self)
        self.btnStart.setText("1. Aşamayı başlat")
        self.btnStart.setFont(self.myFont)
        self.btnStart.clicked.connect(self.start)
        self.btnStart.setFixedSize(180, 50)
        self.btnStart.move(275, 440)
        self.btnStart.setStyleSheet("color : black; background-color : white; border-radius: 5px")
        self.arr.append(self.btnStart)
        
        
    def start(self):
        for c in self.arr:
            c.setVisible(False)
            
def loginStudent():
    login = LoginPanel("Öğrenci", 1250)
    login.show()
        
def main():
    app = QApplication(sys.argv)
    window = StudentPanel()
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
