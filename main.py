import psycopg2
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from pdf2image import convert_from_path
import pytesseract
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

# Giriş Paneli
class LoginPanel(QWidget):
    def __init__(self, text, x):
        self.text = text + " Giriş Paneli"
        self.x = x
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Panelin arka plan rengini değiştir
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle(self.text)
        self.move(self.x, 200)
        self.setFixedSize(700, 500)

         
        self.lblTitle = QLabel(self.text, self)
        self.lblTitle.move(220, 80)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")


        self.lblUserName = QLabel('Kullanıcı Adı:', self)
        self.lblUserName.move(170, 180)
        self.myFont.setPointSize(12)
        self.lblUserName.setFont(self.myFont)
        self.lblUserName.setStyleSheet("color : white")
        
        self.txtUserName = QLineEdit(self)
        self.txtUserName.move(300, 180)
        self.txtUserName.resize(200, 30)
        self.txtUserName.setPlaceholderText('Kullanıcı adı girin...')
        self.txtUserName.setStyleSheet("color : black; background-color : white")
        
        self.lblPassword = QLabel('Şifre:', self)
        self.lblPassword.move(240, 280)
        self.myFont.setPointSize(12)
        self.lblPassword.setFont(self.myFont)
        self.lblPassword.setStyleSheet("color : white")
        
        self.txtPassword = QLineEdit(self)
        self.txtPassword.move(300, 280)
        self.txtPassword.resize(200, 30)
        self.txtPassword.setPlaceholderText('Şifre girin...')
        self.txtPassword.setStyleSheet("color : black; background-color : white")
    
    
        self.myFont.setPointSize(11)
        self.btnLogIn = QPushButton(self)
        self.btnLogIn.setText("Sisteme giriş yap")
        self.btnLogIn.setFont(self.myFont)
        self.btnLogIn.setFixedSize(180, 50)
        self.btnLogIn.move(275, 350)
        self.btnLogIn.setStyleSheet("color : black; background-color : white; border-radius: 5px")




# Yönetici Paneli
class AdminPanel(QWidget):
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


# Öğrenci Paneli
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

# Veritabanı bağlantısı
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="yazlab1",
    host="127.0.0.1",
    port="5432"
)

# Transkript okuma fonksiyonu
def read_transcript():
    # convert pdf file
    transcript = convert_from_path('transcript.pdf')

    text = ""
    for c in transcript:
        text += pytesseract.image_to_string(c, lang="tur")
        
    print(text)    
    
    pattern = r"^[A-Z]{3}\d{3}.*"

    # Metni satır satır bölmek
    print(text)

    # Her satırı incelemek
    """for line in lines:
        print(line)
        # Satırın başında üç büyük harf ve üç rakam var mı kontrol et
        if re.match(r"^[A-Z]{3}\d{3}", line):
            print(f"Al: {line}")"""

"""# PyQt uygulamasını başlat
app = QApplication(sys.argv)

loginStudentPanel = LoginPanel("Öğrenci", 1250)
loginTeacherPanel = LoginPanel("Hoca", 700)
loginAdminPanel = LoginPanel("Yönetici", 10)
loginAdminPanel.show()
loginTeacherPanel.show()
loginStudentPanel.show()

def login_student():
    print("Butona basıldı")

def login_teacher():
    print("Butona basıldı")

def login_admin():
    print("Butona basıldı")

loginStudentPanel.btnLogIn.clicked.connect(login_student)
loginTeacherPanel.btnLogIn.clicked.connect(login_teacher)
loginAdminPanel.btnLogIn.clicked.connect(login_admin)

sys.exit(app.exec_())"""

read_transcript()