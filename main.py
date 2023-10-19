import psycopg2
import fitz
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QWidget, QLineEdit, QPushButton, QFileDialog, QTableWidget, QVBoxLayout, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QFont

# Giriş Paneli
class LoginPanel(QWidget):
    def __init__(self, text, x):
        self.text = text + " Giriş Paneli"
        self.x = x
        super().__init__()
        self.initUI()

    def initUI(self):
        
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
        self.table_visible = True

    def initUI(self):
        self.arr = []
        
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle('Öğrenci Paneli')
        self.move(600, 200)
        self.setFixedSize(1280, 720)

         
        self.lblTitle = QLabel('Öğrenci Paneli', self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(12)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        
        self.myFont.setPointSize(11)
        self.btn_load_pdf = QPushButton(self)
        self.btn_load_pdf.setText("Transkript Yükle")
        self.btn_load_pdf.setFont(self.myFont)
        self.btn_load_pdf.setFixedSize(180, 50)
        self.btn_load_pdf.move(10, 50)
        self.btn_load_pdf.setStyleSheet("color : black; background-color : white; border-radius: 5px")
        self.btn_load_pdf.clicked.connect(self.load_pdf)
        
        
    #Yerel dosyalardan pdf dosyası seçme    
    def load_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        pdf_file, _ = QFileDialog.getOpenFileName(self, 'PDF Dosyasını Seç', '', 'PDF Dosyaları (*.pdf);;Tüm Dosyalar (*)', options=options)

        self.btn_load_pdf.close()
        self.myFont.setPointSize(11)
        self.btn_toggle_table = QPushButton(self)
        self.btn_toggle_table.setText("Transkript Göster")
        self.btn_toggle_table.setFont(self.myFont)
        self.btn_toggle_table.setFixedSize(180, 50)
        self.btn_toggle_table.move(10, 50)
        self.btn_toggle_table.setStyleSheet("color : black; background-color : white; border-radius: 5px")
        self.btn_toggle_table.clicked.connect(self.toggle_table)
        self.btn_toggle_table.setVisible(True)
        self.read_transcript(pdf_file)

    
    
    # Transkript okuma fonksiyonu
    def read_transcript(self, pdf_file):

        doc = fitz.open(pdf_file)

        text = ""
        
        # pdf dosyasını sayfa sayfa dolaşıp texte çevirir
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        # text i satırlara böler
        lines = text.split('\n')
        
        # Üç büyük harf ve üç rakam (Ders Kodu) ile başlayan satırları ayıklar
        ders_kodlari = re.findall(r"^[A-Z]{3}\d{3}$", text, re.MULTILINE)

        lessons = []

        # textte ders kodunu bulduğu ders ile ilgili bilgileri ayıklar
        for kod in ders_kodlari:
            try:
                indeks = lines.index(kod)
                if indeks < len(lines) - 1:
                    ders_kodu = lines[indeks]
                    ders_adi = lines[indeks + 1]
                    ders_statusu = lines[indeks + 3]
                    ogretim_dili = lines[indeks + 4]
                    akts = int(lines[indeks + 8])
                    notu = lines[indeks + 10]
                    lessons.append(
                        {
                            "ders_kodu": ders_kodu,
                            "ders_adi": ders_adi,
                            "ders_statusu": ders_statusu,
                            "ogretim_dili": ogretim_dili,
                            "AKTS": akts,
                            "not": notu,
                        }
                    )
            except ValueError:
                pass
        
        self.transcript_panel = transcript(lessons)
        self.transcript_panel.show()
    
    def toggle_table(self):
        self.table_visible = not self.table_visible
        self.transcript_panel.setVisible(self.table_visible)
    
class transcript(QWidget):
    def __init__(self, lessons):
        super().__init__()
        
        self.lessons = lessons
        self.setWindowTitle("Transkript")
        self.setGeometry(100, 100, 600, 400)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(100, 100, 400, 200)
        self.tableWidget.setRowCount(len(self.lessons))
        self.tableWidget.setColumnCount(len(lessons[0]))
        self.tableWidget.setHorizontalHeaderLabels(["Ders Kodu", "Ders Adı", "Ders Durumu", "Öğretim Dili", "AKTS", "Not"])
        
    
        for row, lesson in enumerate(self.lessons):
            for col, value in enumerate(lesson.values()):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)
        
# Veritabanı bağlantısı
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="yazlab1",
    host="127.0.0.1",
    port="5432"
)


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


app = QApplication(sys.argv)


student_panel = StudentPanel()
student_panel.show()


sys.exit(app.exec_())