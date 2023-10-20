import psycopg2
import fitz
import re
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QWidget,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QComboBox
)
from PyQt5.QtGui import QFont

# Giriş Paneli
class LoginPanel(QWidget):
    def __init__(self, text, x, txtUserName):
        self.textUser = txtUserName
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

        self.lblUserName = QLabel(self.textUser + ": ", self)
        self.lblUserName.move(150, 180)
        self.myFont.setPointSize(10)
        self.lblUserName.setFont(self.myFont)
        self.lblUserName.setStyleSheet("color : white")

        self.txtUserName = QLineEdit(self)
        self.txtUserName.move(300, 180)
        self.txtUserName.resize(200, 30)
        self.txtUserName.setPlaceholderText(self.textUser + " girin...")
        self.txtUserName.setStyleSheet("color : black; background-color : white")

        self.lblPassword = QLabel("Şifre:", self)
        self.lblPassword.move(240, 280)
        self.myFont.setPointSize(12)
        self.lblPassword.setFont(self.myFont)
        self.lblPassword.setStyleSheet("color : white")

        self.txtPassword = QLineEdit(self)
        self.txtPassword.move(300, 280)
        self.txtPassword.resize(200, 30)
        self.txtPassword.setPlaceholderText("Şifre girin...")
        self.txtPassword.setStyleSheet("color : black; background-color : white")

        self.myFont.setPointSize(11)
        self.btnLogIn = QPushButton(self)
        self.btnLogIn.setText("Sisteme giriş yap")
        self.btnLogIn.setFont(self.myFont)
        self.btnLogIn.setFixedSize(180, 50)
        self.btnLogIn.move(275, 350)
        self.btnLogIn.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        
        self.lblIncorrect = QLabel("Hatalı Giriş!", self)
        self.lblIncorrect.move(310, 410)
        self.lblIncorrect.setFont(self.myFont)
        self.lblIncorrect.setStyleSheet("color : white")
        self.lblIncorrect.setVisible(False)
        
        

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
        self.setWindowTitle("Yönetici Paneli")
        self.move(600, 200)
        self.setFixedSize(800, 600)

        self.lblTitle = QLabel("Yönetici Paneli", self)
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

        self.lblRequestNum = QLabel(
            "Bir öğrenci kaç farklı hocadan talep oluşturabilir:", self
        )
        self.lblRequestNum.move(20, 180)
        self.myFont.setPointSize(9)
        self.lblRequestNum.setFont(self.myFont)
        self.lblRequestNum.setStyleSheet("color : white")
        self.arr.append(self.lblRequestNum)

        self.txtRequestNum = QLineEdit(self)
        self.txtRequestNum.move(370, 180)
        self.txtRequestNum.resize(200, 30)
        self.txtRequestNum.setPlaceholderText("Talep sayısı girin...")
        self.txtRequestNum.setStyleSheet("color : black; background-color: white")
        self.arr.append(self.txtRequestNum)

        self.lblChar = QLabel("Mesajlaşma karakter sayısı:", self)
        self.lblChar.move(170, 240)
        self.myFont.setPointSize(9)
        self.lblChar.setFont(self.myFont)
        self.lblChar.setStyleSheet("color : white")
        self.arr.append(self.lblChar)

        self.txtChar = QLineEdit(self)
        self.txtChar.move(370, 240)
        self.txtChar.resize(200, 30)
        self.txtChar.setPlaceholderText("Karakter sayısı girin...")
        self.txtChar.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChar)

        self.lblConfirmNum = QLabel(
            "Bir hoca kaç öğrencinin talebini onaylayabilir:", self
        )
        self.lblConfirmNum.move(45, 300)
        self.myFont.setPointSize(9)
        self.lblConfirmNum.setFont(self.myFont)
        self.lblConfirmNum.setStyleSheet("color : white")
        self.arr.append(self.lblConfirmNum)

        self.txtConfirmNum = QLineEdit(self)
        self.txtConfirmNum.move(370, 300)
        self.txtConfirmNum.resize(200, 30)
        self.txtConfirmNum.setPlaceholderText("Öğrenci sayısı girin...")
        self.txtConfirmNum.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtConfirmNum)

        self.lblTime = QLabel("1. Aşama süresi:", self)
        self.lblTime.move(250, 360)
        self.myFont.setPointSize(9)
        self.lblTime.setFont(self.myFont)
        self.lblTime.setStyleSheet("color : white")
        self.arr.append(self.lblTime)

        self.txtTime = QLineEdit(self)
        self.txtTime.move(370, 360)
        self.txtTime.resize(200, 30)
        self.txtTime.setPlaceholderText("Süre girin...")
        self.txtTime.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtTime)

        self.myFont.setPointSize(11)
        self.btnStart = QPushButton(self)
        self.btnStart.setText("1. Aşamayı başlat")
        self.btnStart.setFont(self.myFont)
        #self.btnStart.clicked.connect(self.start)
        self.btnStart.setFixedSize(180, 50)
        self.btnStart.move(275, 440)
        self.btnStart.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
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
        self.setWindowTitle("Öğrenci Paneli")
        self.move(600, 200)
        self.setFixedSize(1280, 720)

        self.lblTitle = QLabel("Öğrenci Paneli", self)
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
        self.btn_load_pdf.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_load_pdf.clicked.connect(self.load_pdf)

        self.myFont.setPointSize(11)
        self.btn_sec = QPushButton(self)
        self.btn_sec.setText("Seçim Yap")
        self.btn_sec.setFont(self.myFont)
        self.btn_sec.setFixedSize(180, 50)
        self.btn_sec.move(200, 50)
        self.btn_sec.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
            )
        self.btn_sec.setVisible(False)
        
        
        # Ders Seçim Tablosu
        self.lessonTable = QTableWidget(self)
        self.lessonTable.move(10, 120)
        self.lessonTable.setFixedSize(800, 500)
        self.lessonTable.setVisible(False)

    # Yerel dosyalardan pdf dosyası seçme
    def load_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        pdf_file, _ = QFileDialog.getOpenFileName(
            self,
            "PDF Dosyasını Seç",
            "",
            "PDF Dosyaları (*.pdf);;Tüm Dosyalar (*)",
            options=options,
        )

        self.btn_load_pdf.close()
        self.btn_sec.setVisible(True)
        self.myFont.setPointSize(11)
        self.btn_toggle_table = QPushButton(self)
        self.btn_toggle_table.setText("Transkript Göster")
        self.btn_toggle_table.setFont(self.myFont)
        self.btn_toggle_table.setFixedSize(180, 50)
        self.btn_toggle_table.move(10, 50)
        self.btn_toggle_table.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
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
        lines = text.split("\n")

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


        self.transcript_panel = Transcript(lessons)
        self.transcript_panel.show()

        self.lessons_teacher = {
            "Veri Madenciliğine Giriş": ["Sevinç İlhan Omurca"],
            "İşletim Sistemleri": ["Suhap Şahin", "Hikmetcan Özcan"],
            "Yazılım Laboratovarı - I": ["Meltem Kurt Pehlivanoğlu", "Furkan Göz", "Onur Gök"],
            "İşaret ve Sistemler" : ["Adnan Kavak"]
        }

        max_element_count = 0
        
        for lesson, teachers in self.lessons_teacher.items():
            if len(teachers) > max_element_count:
                max_element_count = len(teachers)
        
        
        self.lessonTable.setStyleSheet("color : black; background-color : white")
        self.lessonTable.setRowCount(len(self.lessons_teacher))
        self.lessonTable.setColumnCount(max_element_count+1)
        
        labels = ["Ders Adı"]
        for i in range(max_element_count):
            labels.append("Öğretmenler")
            
        self.lessonTable.setHorizontalHeaderLabels(labels)
        
        row = 0
        for lesson, teachers in self.lessons_teacher.items():
            lesson_item = QTableWidgetItem(lesson)
            self.lessonTable.setItem(row, 0, lesson_item)

            for col, teacher in enumerate(teachers, 1):
                teacher_combobox = QComboBox()
                teacher_combobox.addItems(teachers)
                self.lessonTable.setCellWidget(row, col, teacher_combobox)

            row += 1


        self.lessonTable.setVisible(True)
        
        
    # Transkript panelini gösterip gizleme
    def toggle_table(self):
        self.table_visible = not self.table_visible
        self.transcript_panel.setVisible(self.table_visible)


# Hoca Paneli
class TeacherPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.table_visible = True

    def initUI(self):
        self.arr = []

        self.setStyleSheet("background-color: rgb(140, 0, 0);")

        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Hoca Paneli")
        self.move(600, 200)
        self.setFixedSize(1280, 720)

        self.lblTitle = QLabel("Hoca Paneli", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(12)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")



    
    
    
    

class Transcript(QWidget):
    def __init__(self, lessons):
        super().__init__()
        self.lessons = lessons

        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Transkript")
        self.move(100, 100)
        self.setFixedSize(825, 525)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 10, 800, 500)
        self.tableWidget.setRowCount(len(self.lessons))
        self.tableWidget.setColumnCount(len(lessons[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["Ders Kodu", "Ders Adı", "Ders Durumu", "Öğretim Dili", "AKTS", "Not"]
        )
        self.tableWidget.setStyleSheet("color : black; background-color : white")

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
    port="5432",
)


# PyQt uygulamasını başlat
app = QApplication(sys.argv)

loginStudentPanel = LoginPanel("Öğrenci", 1250, "Öğrenci Numarası")
loginTeacherPanel = LoginPanel("Hoca", 700, "Sicil Numarası")
loginAdminPanel = LoginPanel("Yönetici", 10, "Kullanıcı Adı")

loginStudentPanel.show()
loginTeacherPanel.show()
loginAdminPanel.show()


student_panel = StudentPanel()
teacher_panel = TeacherPanel()
admin_panel = AdminPanel()

def login_check(panel, table, txtUserName):
    userName = panel.txtUserName.text()
    password = panel.txtPassword.text()
    
    cur = conn.cursor()
    query = f"SELECT * FROM {table} WHERE {txtUserName} = '{userName}' AND şifre = '{password}'"
    cur.execute(query)
    
    results = cur.fetchall()
    
    
    return results


def login_student():
    results = login_check(loginStudentPanel,"ogrenci", "ogrenci_no")
    if len(results):
        student_panel.show()
        loginStudentPanel.setVisible(False)
    
    else:
        loginStudentPanel.lblIncorrect.setVisible(True)
        
        loginStudentPanel.txtUserName.setText("")
        loginStudentPanel.txtPassword.setText("")


def login_teacher():
    results = login_check(loginTeacherPanel, "hoca", "sicil_numarası")
    if len(results):
        teacher_panel.show()
        loginTeacherPanel.setVisible(False)
    
    else:
        loginTeacherPanel.lblIncorrect.setVisible(True)
        
        loginTeacherPanel.txtUserName.setText("")
        loginTeacherPanel.txtPassword.setText("")


def login_admin():
    results = login_check(loginAdminPanel, "yonetici", "kullanıcı_adı")
    if len(results):
        admin_panel.show()
        loginAdminPanel.setVisible(False)
    
    else:
        loginAdminPanel.lblIncorrect.setVisible(True)
        
        loginAdminPanel.txtUserName.setText("")
        loginAdminPanel.txtPassword.setText("")



loginStudentPanel.btnLogIn.clicked.connect(login_student)
loginTeacherPanel.btnLogIn.clicked.connect(login_teacher)
loginAdminPanel.btnLogIn.clicked.connect(login_admin)

sys.exit(app.exec_())



