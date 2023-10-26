import psycopg2
import fitz
import re
import sys
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import (
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
from PyQt6.QtGui import QFont
import threading

import student_panel

from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QPalette, QColor
# Giriş Paneli

from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon

import sys
from PyQt6.QtWidgets import QApplication, QWidget,QMainWindow, QLabel, QPushButton, QVBoxLayout,QTabWidget, QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog,QHBoxLayout

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
        
    def setlblTitleText(self, text):
            self.lblTitle.setText(text)    

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
        self.setFixedSize(1280, 700)

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


        self.myFont.setPointSize(9)
        self.btntalep_hoca = QPushButton(self)
        self.btntalep_hoca.clicked.connect(self.talep_sayilari_onay)
        self.btntalep_hoca.setText("Talep Sayılarını Onayla")
        self.btntalep_hoca.setFont(self.myFont)
        self.btntalep_hoca.setFixedSize(180, 50)
        self.btntalep_hoca.move(925, 10)
        self.btntalep_hoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        
        

        cur = conn.cursor()
        query = "SELECT ders_adı FROM açılanDersler"
        cur.execute(query)
        
        veriler = cur.fetchall()
        cur.close()
        self.dersler = [veri[0] for veri in veriler]
        print(self.dersler)

        # Her bir ders için talep edilebilecek hoca sayısı
        self.talep_hoca_tablosu = QTableWidget(self)
        self.talep_hoca_tablosu.move(825, 100)
        self.talep_hoca_tablosu.setFixedSize(450, 350)
        self.talep_hoca_tablosu.setVisible(True)
        self.talep_hoca_tablosu.setStyleSheet("color : black; background-color : white")
        self.talep_hoca_tablosu.setColumnCount(2)
        self.talep_hoca_tablosu.setRowCount(len(self.dersler))
        # 1 indexli sütunun genişliği 210
        self.talep_hoca_tablosu.setColumnWidth(0, 220)
        self.talep_hoca_tablosu.setColumnWidth(1, 210)
        
        
        # Tablo başlıklarının yazı fontunu ayarlama
        font = QFont()
        font.setBold(True)
        font.setPointSize(8)
        
        self.talep_hoca_tablosu.setHorizontalHeaderLabels(["Ders Adları", "Talep Edilebilecek Hoca Sayısı"])
        header = self.talep_hoca_tablosu.horizontalHeader()
        for i in range(self.talep_hoca_tablosu.columnCount()):
            header.setFont(font)
            
        for row, ders_adi in enumerate(self.dersler):
            self.talep_hoca_tablosu.setItem(row, 0, QTableWidgetItem(ders_adi))
            self.talep_hoca_tablosu.setItem(row, 1, QTableWidgetItem("1"))
            
            # Ders adı değiştirilemez
            self.talep_hoca_tablosu.item(row, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        
        self.talep_hoca_tablosu.setVisible(True)
        

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

    def setlblTitleText(self, text):
            self.lblTitle.setText(text)

    
    def talep_sayilari_onay(self):

        for row, ders_adi in enumerate(self.dersler):
            text = self.talep_hoca_tablosu.item(row, 1).text()
            cur = conn.cursor()
            query = "UPDATE \"açılanDersler\" SET talep_edilebilecek_hoca_sayısı = %s WHERE ders_adı = %s"
            cur.execute(query, (str(text), str(ders_adi)))
            cur.close()
                    
        self.talep_hoca_tablosu.close()
        self.btntalep_hoca.close()
        

# Öğrenci Paneli
class StudentPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.table_visible = True
        
        

    def initUI(self):
        self.arr = []

        self.setStyleSheet("background-color: rgb(10, 84, 50);")

        self.setWindowTitle("KOU Öğrenci")
        self.setGeometry(100, 100, 1200, 600)
        
        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.courses_tab = QWidget()
        self.courses_layout = QVBoxLayout(self.courses_tab)
        self.course_list = QListWidget()
        self.btn_load_pdf = QPushButton("Transkript Yükle")
        self.btn_load_pdf.setStyleSheet("color: white; font-weight: bold; background-color: rgb(6, 51, 29);")
        self.btn_load_pdf.clicked.connect(self.load_pdf)
        self.courses_layout.addWidget(self.btn_load_pdf)
        self.courses_layout.addWidget(self.course_list)
        self.central_widget.addTab(self.courses_tab, "Aldığım Dersler")

        self.btn_load_pdf.clicked.connect(self.load_pdf)
       
        self.professors_tab = QWidget()
        self.professors_layout = QVBoxLayout(self.professors_tab)
        self.professor_list = QListWidget()
        self.btn_sec= QPushButton("DERS SEÇ")
        self.btn_sec.setStyleSheet("color: white; font-weight: bold; background-color: rgb(6, 51, 29);")
       # self.btn_sec.setStyleSheet("background-color: rgb(6, 51, 29);")
        self.professors_layout.addWidget(self.btn_sec)
        self.professors_layout.addWidget(self.professor_list)
        self.central_widget.addTab(self.professors_tab, "Ders Alabileceğim Hocalar")
        
        
        # DERS TALEBİ İÇİN
        self.request_tab = QWidget()
        self.request_layout = QVBoxLayout(self.request_tab)
        self.request_list = QListWidget()
        self.request_btn = QPushButton("TALEP OLUŞTUR")
        self.request_btn.setStyleSheet("color: white; font-weight: bold; background-color: rgb(6, 51, 29)")
        self.request_layout.addWidget(self.request_btn)
        self.request_layout.addWidget(self.request_list)
        self.central_widget.addTab(self.request_tab, "Ders Talebi Oluştur")

        #self.request_input = QLineEdit()
        #self.request_layout.addWidget(self.request_input)

        def create_request():
            request_text = self.request_input.text()
            if request_text:
                # Talep oluştur işlemini burada gerçekleştirin
                self.request_list.addItem(request_text)
                # İşte burada bu talebi veritabanına veya başka bir yere kaydetmek isterseniz student_panel.talep_olustur işlevini çağırabilirsiniz.
                # Örnek olarak: student_panel.talep_olustur(210202103, request_text)

                # Kullanıcının girdiği metni temizle
                self.request_input.clear()

        self.request_btn.clicked.connect(create_request)

        self.delete_req_btn = QPushButton("Talebi Sil")
        self.request_layout.addWidget(self.delete_req_btn)

        # MESAJLAŞMA SEKMESİ
        self.message_tab = QWidget()
        self.message_layout = QVBoxLayout()
        self.message_list = QListWidget()

        self.message_btn = QPushButton("Mesaj gönder")
        self.message_btn.setIcon(QIcon("/Users/aslinurtopcu/Desktop/send.png"))  # İkon dosyanızın yolunu belirtin
        self.message_btn.setStyleSheet("color: white; font-weight: bold; background-color: rgb(6, 51, 29)")

        self.send_message_btn = QPushButton("Mesaj Yolla")
        self.message_input = QLineEdit()  # Metin girişi için QLineEdit

        # Akademisyen seçimi için bir açılır menü ekleyin
        self.academician_combo = QComboBox()
        academician_list = ["Akademisyen 1", "Akademisyen 2", "Akademisyen 3"]  # Akademisyenlerin listesi
        self.academician_combo.addItems(academician_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.message_btn)
        button_layout.addWidget(self.academician_combo)  # Akademisyen seçimini ekleyin
        button_layout.addWidget(self.send_message_btn)

        self.message_tab.setLayout(self.message_layout)
        self.message_layout.addWidget(self.message_input)
        self.message_layout.addLayout(button_layout)
        self.message_layout.addWidget(self.message_list)
        self.central_widget.addTab(self.message_tab, "Mesaj Gönder")

        def send_message():
            message_text = self.message_input.text()
            selected_academician = self.academician_combo.currentText()  # Seçilen akademisyeni alın
            if message_text:
            # İşte burada bu mesajı veritabanına veya başka bir yere kaydetmek isterseniz student_panel.mesaj_gonder işlevini çağırabilirsiniz.
            # Öğrenci numarası ve seçilen akademisyeni kullanarak mesaj gönderme işlemi yapabilirsiniz.
                student_panel.mesaj_gonder(ogrenci_no, selected_academician, message_text)

                self.message_list.addItem(f"Gönderilen ({selected_academician}): {message_text}")  # Gönderilen mesajları görüntüle
                self.message_input.clear()

        self.message_btn.clicked.connect(send_message)

        self.show_message_btn = QPushButton("Mesajları Göster")
        button_layout.addWidget(self.show_message_btn)

        def show_messages():
            # İşte burada gelen mesajları görüntülemek isterseniz student_panel.mesajlari_getir işlevini çağırabilirsiniz.
            messages = student_panel.mesajlari_getir(ogrenci_no)
            for message in messages:
                self.message_list.addItem("Gelen: " + message)

        self.show_message_btn.clicked.connect(show_messages)



        
        
        """self.btn_load_pdf = QPushButton(self)
        self.btn_load_pdf.setText("Transkript Yükle")
        self.btn_load_pdf.setFont(self.myFont)
        self.btn_load_pdf.setFixedSize(180, 50)
        self.btn_load_pdf.move(10, 50)
        self.btn_load_pdf.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px" 
        )"""
        
        
        """self.myFont.setPointSize(11)
        self.btn_sec = QPushButton(self)
        self.btn_sec.setText("Seçim Yap")
        self.btn_sec.setFont(self.myFont)
        self.btn_sec.setFixedSize(180, 50)
        self.btn_sec.move(200, 50)
        self.btn_sec.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
            )"""
        self.btn_sec.setVisible(False)
        
        
        # Ders Seçim Tablosu
        self.lessonTable = QTableWidget(self)
        self.lessonTable.move(10, 120)
        self.lessonTable.setFixedSize(800, 500)
        self.lessonTable.setVisible(False)

    # Yerel dosyalardan pdf dosyası seçme
    def load_pdf(self):
        dosya_diyalog = QFileDialog()
        dosya_yolu, _ = dosya_diyalog.getOpenFileName()
        if dosya_yolu:
            print(f"Seçilen dosya: {dosya_yolu}")
            pdf_file, _ = QFileDialog.getOpenFileName(parent=None, caption="Select a PDF file", directory='', filter="PDF Files (*.pdf)")

        self.btn_load_pdf.close()
        self.btn_sec.setVisible(True)
       # self.myFont.setPointSize(11)
        self.btn_toggle_table = QPushButton(self)
        self.btn_toggle_table.setText("Transkript Göster")
        #self.btn_toggle_table.setFont(18)
        self.btn_toggle_table.setFixedSize(180, 50)
        self.btn_toggle_table.move(10, 50)
        self.btn_toggle_table.setStyleSheet("color : black; background-color : white; border-radius: 5px")
        self.btn_toggle_table.clicked.connect(self.toggle_table)
        self.btn_toggle_table.setVisible(True)
        self.read_transcript(pdf_file)


        self.btn_load_pdf.close()
        self.btn_sec.setVisible(True)
        #self.myFont.setPointSize(11)
        self.btn_toggle_table = QPushButton(self)
        self.btn_toggle_table.setText("Transkript Göster")
       # self.btn_toggle_table.setFont(self.myFont)
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

    def setlblTitleText(self, text):
        self.lblTitle.setText(text)
        


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


    def setlblTitleText(self, text):
        self.lblTitle.setText(text)
    
    
    
    

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
        
        
#ÖĞRENCİ GİRİŞİ İÇİN *******************************************************************************************************

class StudentLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show
        self.setWindowTitle("Öğrenci Girişi")
        self.setGeometry(100, 100, 1200, 600)
        self.init_ui()

    def init_ui(self):
        background_image = QPixmap("/Users/aslinurtopcu/Desktop/wallpapers/simon.jpg")
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(background_label)

        frame = QWidget()
        frame.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        frame.setFixedSize(400, 300)

        self.setCentralWidget(frame)

        self.student_no_label = QLabel("Öğrenci Numarası:", frame)
        self.student_no_input = QLineEdit(frame)
        self.password_label = QLabel("Şifre:", frame)
        self.password_input = QLineEdit(frame)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Giriş", frame)
        self.login_btn.setIcon(QIcon("/Users/aslinurtopcu/Desktop/StuIkon.png"))

        self.login_btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.student_no_label)
        layout.addWidget(self.student_no_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        frame.setLayout(layout)

    def login(self):
        student_no = self.student_no_input.text()
        password = self.password_input.text()

        if self.validate_student_credentials(student_no, password):
            print("Öğrenci girişi başarılı")
            self.open_student_panel()
        else:
            print("Başarısız öğrenci girişi")
            self.show_error_message("Giriş başarısız!")

    def validate_student_credentials(self, student_no, password):
        conn = psycopg2.connect(
            database="postgres",
            user="aslinurtopcu",
            password="sifre",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT ogrenci_no, sifre FROM ogrenci WHERE ogrenci_no = %s AND sifre = %s", (student_no, password))
        result = cursor.fetchone()

        conn.close()

        return result is not None

    def open_student_panel(self):
        self.hide()
        self.student_panel = StudentPanel()
        self.student_panel.show()

    def show_error_message(self, message):
        pass



# Veritabanı bağlantısı***************************************
conn = psycopg2.connect(

    database="postgres",
    user="aslinurtopcu",
    password="çilek",
    host="localhost",
    port="5432",
)
conn.autocommit = True

cursor = conn.cursor()


        
#UYGULAMA GİRİŞ EKRANI****************************** 

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(100, 100, 1200, 600)

    
        layout = QVBoxLayout(self)
        background_image_path = "/Users/aslinurtopcu/Desktop/wallpapers/kocaeliUni.jpeg"
        background_image = QPixmap(background_image_path)
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        layout.addWidget(background_label)

        self.lblTitle = QLabel("KOCAELİ ÜNİVERSİTESİ DERS KAYIT SİSTEMİNE HOŞ GELDİNİZ", self)
        self.lblTitle.setStyleSheet("font-size: 30px; color: white; text-align: center;")
        layout.addWidget(self.lblTitle)

        self.btnStudent = QPushButton("Öğrenci Girişi", self)
        self.btnStudent.setStyleSheet("font-size: 20px;")
        self.btnStudent.clicked.connect(self.openStudentPanel)
        layout.addWidget(self.btnStudent)

        self.btnTeacher = QPushButton("Hoca Girişi", self)
        self.btnTeacher.setStyleSheet("font-size: 20px;")
        self.btnTeacher.clicked.connect(self.openTeacherPanel)
        layout.addWidget(self.btnTeacher)

        self.btnAdmin = QPushButton("Yönetici Girişi", self)
        self.btnAdmin.setStyleSheet("font-size: 20px;")
        self.btnAdmin.clicked.connect(self.openAdminPanel)
        layout.addWidget(self.btnAdmin)

    def openStudentPanel(self):
        print("Öğrenci Paneline Yönlendiriliyor")
        self.student_login_window = StudentLoginWindow()  # Öğrenci girişi ekranı penceresini oluştur
        self.student_login_window.show()  # Pencereyi görüntüle
        

    def openTeacherPanel(self):
        print("Hoca Paneline Yönlendiriliyor")
        self.teacher_panel = TeacherPanel()
        self.teacher_panel.show()

    def openAdminPanel(self):
        print("Yönetici Paneline Yönlendiriliyor")
        self.admin_panel = AdminPanel()
        self.admin_panel.show()

if __name__ == "__main__":
    app = QApplication([])
    loginScreen = LoginScreen()
    loginScreen.show()
    app.exec()



#PyQt uygulamasını başlat*************************************
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
    cur.close()
    
    return results


def login_student():
    results = login_check(loginStudentPanel,"ogrenci", "ogrenci_no")
    student_name = "Öğrenci Paneli - " + results[0][1] + " " + results[0][2]
    if len(results):
        t = threading.Thread(target=student_panel.setlblTitleText, args=(student_name,))
        t.start()
        t.join()
        student_panel.show()
        loginStudentPanel.setVisible(False)
    
    else:
        loginStudentPanel.lblIncorrect.setVisible(True)
        
        loginStudentPanel.txtUserName.setText("")
        loginStudentPanel.txtPassword.setText("")


def login_teacher():
    results = login_check(loginTeacherPanel, "hoca", "sicil_no")
    teacher_name = "Hoca Paneli - " + results[0][0] + " " + results[0][1]
    if len(results):
        t = threading.Thread(target=teacher_panel.setlblTitleText, args=(teacher_name,))
        t.start()
        t.join()
        teacher_panel.show()
        loginTeacherPanel.setVisible(False)
    
    else:
        loginTeacherPanel.lblIncorrect.setVisible(True)
        
        loginTeacherPanel.txtUserName.setText("")
        loginTeacherPanel.txtPassword.setText("")


def login_admin():
    results = login_check(loginAdminPanel, "yonetici", "kullanıcı_adı")
    admin_name = "Yönetici Paneli - " + results[0][1]
    if len(results):
        t = threading.Thread(target=admin_panel.setlblTitleText, args=(admin_name,))
        t.start()
        t.join()
        admin_panel.show()
        loginAdminPanel.setVisible(False)
        
    else:
        loginAdminPanel.lblIncorrect.setVisible(True)
        
        loginAdminPanel.txtUserName.setText("")
        loginAdminPanel.txtPassword.setText("")



loginStudentPanel.btnLogIn.clicked.connect(login_student)
loginTeacherPanel.btnLogIn.clicked.connect(login_teacher)
loginAdminPanel.btnLogIn.clicked.connect(login_admin)



sys.exit(app.exec())