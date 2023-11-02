import psycopg2
from psycopg2 import Error, errors
import fitz
import re
import sys
from PyQt5 import QtCore
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
    QComboBox,
    QVBoxLayout,
    QMainWindow,
    QTextEdit,
)
import time
from PyQt5.QtGui import QFont, QPixmap
import threading

from regex import P
import random

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
        self.txtPassword.setEchoMode(QLineEdit.Password)
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


# ÖĞRENCİ GİRİŞİ İÇİN *******************************************************************************************************
class StudentLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show
        self.setWindowTitle("Öğrenci Girişi")
        self.move(1200, 200)
        self.setFixedSize(700, 500)
        self.setStyleSheet("background-color: rgb(140, 0, 0);")

        frame = QWidget(self)
        frame.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        frame.setFixedSize(700, 500)
        self.setCentralWidget(frame)

        self.student_no_label = QLabel("Öğrenci Numarası:", frame)
        self.student_no_input = QLineEdit(frame)
        self.password_label = QLabel("Şifre:", frame)
        self.password_input = QLineEdit(frame)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Giriş", frame)
        # self.login_btn.setIcon(QIcon("/Users/aslinurtopcu/Desktop/StuIkon.png"))

        self.login_btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        background_image_path = "img.jpg"
        background_image = QPixmap(background_image_path)
        # background_image = background_image.scaled(700, 500)
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        layout.addWidget(self.student_no_label)
        layout.addWidget(self.student_no_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(background_label)
        layout.addWidget(self.login_btn)

        frame.setLayout(layout)

    def login(self):
        student_no = self.student_no_input.text()
        password = self.password_input.text()

        if self.validate_student_credentials(student_no, password):
            print("Öğrenci girişi başarılı")
            self.open_student_panel(student_no)
        else:
            print("Başarısız öğrenci girişi")
            self.show_error_message("Giriş başarısız!")

    def validate_student_credentials(self, student_no, password):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT ogrenci_no, şifre FROM ogrenci WHERE ogrenci_no = %s AND şifre = %s",
            (student_no, password),
        )
        result = cursor.fetchone()

        cursor.close()

        return result is not None

    def open_student_panel(self, student_no):
        self.hide()
        self.student_panel = StudentPanel(student_no)
        self.student_panel.show()

    def show_error_message(self, message):
        pass


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

        self.lblChar = QLabel("Mesajlaşma karakter sayısı(0 - 300):", self)
        self.lblChar.move(800, 500)
        self.myFont.setPointSize(9)
        self.lblChar.setFont(self.myFont)
        self.lblChar.setStyleSheet("color : white")
        self.arr.append(self.lblChar)

        self.txtChar = QLineEdit(self)
        self.txtChar.move(1050, 500)
        self.txtChar.resize(200, 30)
        self.txtChar.setPlaceholderText("Karakter sayısı girin...")
        self.txtChar.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChar)

        self.myFont.setPointSize(9)
        self.btntalep_hoca = QPushButton(self)
        self.btntalep_hoca.clicked.connect(self.talep_sayilari_onay)
        self.btntalep_hoca.setText("Parametreleri Onayla")
        self.btntalep_hoca.setFont(self.myFont)
        self.btntalep_hoca.setFixedSize(180, 50)
        self.btntalep_hoca.move(1100, 10)
        self.btntalep_hoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        cur = conn.cursor()
        query = 'SELECT ders_adı FROM "açılanDersler"'
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
        self.talep_hoca_tablosu.setColumnWidth(0, 220)
        self.talep_hoca_tablosu.setColumnWidth(1, 210)

        # Tablo başlıklarının yazı fontunu ayarlama
        font = QFont()
        font.setBold(True)
        font.setPointSize(8)

        self.talep_hoca_tablosu.setHorizontalHeaderLabels(
            ["Ders Adları", "Talep Edilebilecek Hoca Sayısı"]
        )
        header = self.talep_hoca_tablosu.horizontalHeader()
        for _ in range(self.talep_hoca_tablosu.columnCount()):
            header.setFont(font)

        for row, ders_adi in enumerate(self.dersler):
            self.talep_hoca_tablosu.setItem(row, 0, QTableWidgetItem(ders_adi))
            self.talep_hoca_tablosu.setItem(row, 1, QTableWidgetItem("1"))

            # Ders adı değiştirilemez
            self.talep_hoca_tablosu.item(row, 0).setFlags(QtCore.Qt.ItemIsEnabled)

        self.talep_hoca_tablosu.setVisible(True)

        self.lblConfirmNum = QLabel(
            "Bir hoca kaç öğrencinin talebini onaylayabilir: ", self
        )
        self.lblConfirmNum.move(730, 550)
        self.myFont.setPointSize(9)
        self.lblConfirmNum.setFont(self.myFont)
        self.lblConfirmNum.setStyleSheet("color : white")
        self.arr.append(self.lblConfirmNum)

        self.txtConfirmNum = QLineEdit(self)
        self.txtConfirmNum.move(1050, 550)
        self.txtConfirmNum.resize(200, 30)
        self.txtConfirmNum.setPlaceholderText("Öğrenci sayısı girin...")
        self.txtConfirmNum.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtConfirmNum)

        self.btnTime = QPushButton(self)
        self.btnTime.setText("2. Aşamaya geç")
        self.btnTime.setFont(self.myFont)
        self.btnTime.clicked.connect(self.asama2)
        self.btnTime.setFixedSize(180, 50)
        self.btnTime.move(1000, 600)
        self.btnTime.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.arr.append(self.btnTime)


        self.myFont.setPointSize(11)
        self.btnStart = QPushButton(self)
        self.btnStart.setText("1. Aşamayı başlat")
        self.btnStart.setFont(self.myFont)
        self.btnStart.clicked.connect(self.start)
        self.btnStart.setFixedSize(180, 50)
        self.btnStart.move(240, 10)
        self.btnStart.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.arr.append(self.btnStart)

        self.myFont.setPointSize(8)
        self.btntalep_ogr = QPushButton(self)
        self.btntalep_ogr.setText("Öğrenci talep geçmişi")
        self.btntalep_ogr.setFont(self.myFont)
        self.btntalep_ogr.clicked.connect(self.ogrenci_talep_gecmisi)
        self.btntalep_ogr.setFixedSize(150, 50)
        self.btntalep_ogr.move(460, 10)
        self.btntalep_ogr.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(8)
        self.btntalep_hoca = QPushButton(self)
        self.btntalep_hoca.setText("Hoca talep geçmişi")
        self.btntalep_hoca.setFont(self.myFont)
        self.btntalep_hoca.clicked.connect(self.hoca_talep_gecmisi)
        self.btntalep_hoca.setFixedSize(150, 50)
        self.btntalep_hoca.move(620, 10)
        self.btntalep_hoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(8)
        self.btn_ders_ekleme = QPushButton(self)
        self.btn_ders_ekleme.setText("Öğrenciye ders ekleme")
        self.btn_ders_ekleme.setFont(self.myFont)
        self.btn_ders_ekleme.clicked.connect(self.ogrenci_ders_ekleme)
        self.btn_ders_ekleme.setFixedSize(150, 50)
        self.btn_ders_ekleme.move(780, 10)
        self.btn_ders_ekleme.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        # öğrenci ekleme

        self.txtAdd_ogr_no = QLineEdit(self)
        self.txtAdd_ogr_no.move(100, 100)
        self.txtAdd_ogr_no.resize(60, 30)
        self.txtAdd_ogr_no.setPlaceholderText("no")
        self.txtAdd_ogr_no.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtAdd_ogr_no)

        self.txtAdd_ogr_isim = QLineEdit(self)
        self.txtAdd_ogr_isim.move(170, 100)
        self.txtAdd_ogr_isim.resize(60, 30)
        self.txtAdd_ogr_isim.setPlaceholderText("isim")
        self.txtAdd_ogr_isim.setStyleSheet("color : black; background-color : white")

        self.txtAdd_ogr_soyIsim = QLineEdit(self)
        self.txtAdd_ogr_soyIsim.move(240, 100)
        self.txtAdd_ogr_soyIsim.resize(60, 30)
        self.txtAdd_ogr_soyIsim.setPlaceholderText("soyİsim")
        self.txtAdd_ogr_soyIsim.setStyleSheet("color : black; background-color : white")

        self.txtAdd_ogr_sifre = QLineEdit(self)
        self.txtAdd_ogr_sifre.move(310, 100)
        self.txtAdd_ogr_sifre.resize(60, 30)
        self.txtAdd_ogr_sifre.setPlaceholderText("şifre")
        self.txtAdd_ogr_sifre.setStyleSheet("color : black; background-color : white")

        self.txtAdd_ogr_ort = QLineEdit(self)
        self.txtAdd_ogr_ort.move(380, 100)
        self.txtAdd_ogr_ort.resize(60, 30)
        self.txtAdd_ogr_ort.setPlaceholderText("ortalama")
        self.txtAdd_ogr_ort.setStyleSheet("color : black; background-color : white")

        self.myFont.setPointSize(8)
        self.btnAdd_ogr = QPushButton(self)
        self.btnAdd_ogr.setText("Öğrenciyi ekle")
        self.btnAdd_ogr.setFont(self.myFont)
        self.btnAdd_ogr.clicked.connect(self.addStudent)
        self.btnAdd_ogr.setFixedSize(100, 30)
        self.btnAdd_ogr.move(450, 100)
        self.btnAdd_ogr.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblResultAddSt = QLabel("Başarılı", self)
        self.lblResultAddSt.move(570, 100)
        self.lblResultAddSt.setFont(self.myFont)
        self.lblResultAddSt.setStyleSheet("color : white")
        self.lblResultAddSt.setVisible(False)

        # Öğrenci bilgi değiştirme

        self.txtChangeOgr_no = QLineEdit(self)
        self.txtChangeOgr_no.move(30, 200)
        self.txtChangeOgr_no.resize(80, 30)
        self.txtChangeOgr_no.setPlaceholderText("no girin...")
        self.txtChangeOgr_no.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChangeOgr_no)

        self.cbxChangeOgr = QComboBox(self)
        self.cbxChangeOgr.move(120, 200)
        self.cbxChangeOgr.resize(170, 30)
        self.cbxChangeOgr.setStyleSheet("background-color : white")

        table_name = "ogrenci"
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        )
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()

        del columns[columns.index("anlaşma_talep_sayısı")]

        self.cbxChangeOgr.addItems(columns)
        self.cbxChangeOgr.setVisible(True)

        self.txtChangeOgr = QLineEdit(self)
        self.txtChangeOgr.move(310, 200)
        self.txtChangeOgr.resize(120, 30)
        self.txtChangeOgr.setPlaceholderText("Yeni değeri girin...")
        self.txtChangeOgr.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChangeOgr)

        self.lblResultChangeSt = QLabel("Başarılı", self)
        self.lblResultChangeSt.move(570, 200)
        self.lblResultChangeSt.setFont(self.myFont)
        self.lblResultChangeSt.setStyleSheet("color : white")
        self.lblResultChangeSt.setVisible(False)

        self.myFont.setPointSize(11)
        self.btnChange = QPushButton(self)
        self.btnChange.setText("Güncelle")
        self.btnChange.setFont(self.myFont)
        self.btnChange.clicked.connect(self.changeStudent)
        self.btnChange.setFixedSize(100, 30)
        self.btnChange.move(450, 200)
        self.btnChange.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.arr.append(self.btnChange)

        # Öğrenci silme
        self.txtRem_ogr_no = QLineEdit(self)
        self.txtRem_ogr_no.move(350, 300)
        self.txtRem_ogr_no.resize(60, 30)
        self.txtRem_ogr_no.setPlaceholderText("no")
        self.txtRem_ogr_no.setStyleSheet("color : black; background-color : white")

        self.myFont.setPointSize(8)
        self.btnRem_ogr = QPushButton(self)
        self.btnRem_ogr.setText("Öğrenciyi sil")
        self.btnRem_ogr.setFont(self.myFont)
        self.btnRem_ogr.clicked.connect(self.removeStudent)
        self.btnRem_ogr.setFixedSize(100, 30)
        self.btnRem_ogr.move(450, 300)
        self.btnRem_ogr.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblResultRemoveSt = QLabel("Başarılı", self)
        self.lblResultRemoveSt.move(570, 300)
        self.lblResultRemoveSt.setFont(self.myFont)
        self.lblResultRemoveSt.setStyleSheet("color : white")
        self.lblResultRemoveSt.setVisible(False)

        # Hoca ekleme
        self.txtAdd_hoca_isim = QLineEdit(self)
        self.txtAdd_hoca_isim.move(130, 150)
        self.txtAdd_hoca_isim.resize(60, 30)
        self.txtAdd_hoca_isim.setPlaceholderText("isim")
        self.txtAdd_hoca_isim.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtAdd_hoca_isim)

        self.txtAdd_hoca_soyIsim = QLineEdit(self)
        self.txtAdd_hoca_soyIsim.move(200, 150)
        self.txtAdd_hoca_soyIsim.resize(60, 30)
        self.txtAdd_hoca_soyIsim.setPlaceholderText("soyİsim")
        self.txtAdd_hoca_soyIsim.setStyleSheet(
            "color : black; background-color : white"
        )
        self.arr.append(self.txtAdd_hoca_soyIsim)

        self.txtAdd_hoca_sifre = QLineEdit(self)
        self.txtAdd_hoca_sifre.move(270, 150)
        self.txtAdd_hoca_sifre.resize(60, 30)
        self.txtAdd_hoca_sifre.setPlaceholderText("şifre")
        self.txtAdd_hoca_sifre.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtAdd_hoca_sifre)

        self.txtAdd_acilan_ders = QLineEdit(self)
        self.txtAdd_acilan_ders.move(340, 150)
        self.txtAdd_acilan_ders.resize(100, 30)
        self.txtAdd_acilan_ders.setPlaceholderText("verdiği dersler")
        self.txtAdd_acilan_ders.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtAdd_acilan_ders)

        self.myFont.setPointSize(8)
        self.btnAdd_hoca = QPushButton(self)
        self.btnAdd_hoca.setText("Hocayı ekle")
        self.btnAdd_hoca.setFont(self.myFont)
        self.btnAdd_hoca.clicked.connect(self.addTeacher)
        self.btnAdd_hoca.setFixedSize(100, 30)
        self.btnAdd_hoca.move(450, 150)
        self.btnAdd_hoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblResultAddTch = QLabel("Başarılı", self)
        self.lblResultAddTch.move(570, 150)
        self.lblResultAddTch.setFont(self.myFont)
        self.lblResultAddTch.setStyleSheet("color : white")
        self.lblResultAddTch.setVisible(False)

        # Hoca bilgi değiştirme
        self.txtChange_hoca_sicil_no = QLineEdit(self)
        self.txtChange_hoca_sicil_no.move(30, 250)
        self.txtChange_hoca_sicil_no.resize(80, 30)
        self.txtChange_hoca_sicil_no.setPlaceholderText("sicil no girin...")
        self.txtChange_hoca_sicil_no.setStyleSheet(
            "color : black; background-color : white"
        )
        self.arr.append(self.txtChange_hoca_sicil_no)

        self.cbxChangeHoca = QComboBox(self)
        self.cbxChangeHoca.move(120, 250)
        self.cbxChangeHoca.resize(170, 30)
        self.cbxChangeHoca.setStyleSheet("background-color : white")

        table_name = "hoca"
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        )
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()

        del columns[columns.index("ilgi_alanları")]
        del columns[columns.index("açılan_dersler")]
        del columns[columns.index("kriter_dersler")]

        self.cbxChangeHoca.addItems(columns)
        self.cbxChangeHoca.setVisible(True)

        self.txtChangeHoca = QLineEdit(self)
        self.txtChangeHoca.move(310, 250)
        self.txtChangeHoca.resize(120, 30)
        self.txtChangeHoca.setPlaceholderText("Yeni değeri girin...")
        self.txtChangeHoca.setStyleSheet("color : black; background-color : white")
        self.arr.append(self.txtChangeHoca)

        self.lblResultChangeTch = QLabel("Başarılı", self)
        self.lblResultChangeTch.move(570, 250)
        self.lblResultChangeTch.setFont(self.myFont)
        self.lblResultChangeTch.setStyleSheet("color : white")
        self.lblResultChangeTch.setVisible(False)

        self.myFont.setPointSize(11)
        self.btnChangeHoca = QPushButton(self)
        self.btnChangeHoca.setText("Güncelle")
        self.btnChangeHoca.setFont(self.myFont)
        self.btnChangeHoca.clicked.connect(self.changeTeacher)
        self.btnChangeHoca.setFixedSize(100, 30)
        self.btnChangeHoca.move(450, 250)
        self.btnChangeHoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        # Hoca Silme
        self.txtRemove_hoca_sicil_no = QLineEdit(self)
        self.txtRemove_hoca_sicil_no.move(350, 350)
        self.txtRemove_hoca_sicil_no.resize(80, 30)
        self.txtRemove_hoca_sicil_no.setPlaceholderText("sicil no")
        self.txtRemove_hoca_sicil_no.setStyleSheet(
            "color : black; background-color : white"
        )

        self.myFont.setPointSize(11)
        self.btnRemoveHoca = QPushButton(self)
        self.btnRemoveHoca.setText("Hocayı sil")
        self.btnRemoveHoca.setFont(self.myFont)
        self.btnRemoveHoca.clicked.connect(self.removeTeacher)
        self.btnRemoveHoca.setFixedSize(100, 30)
        self.btnRemoveHoca.move(450, 350)
        self.btnRemoveHoca.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblResultRemoveTch = QLabel("Başarılı", self)
        self.lblResultRemoveTch.move(570, 350)
        self.lblResultRemoveTch.setFont(self.myFont)
        self.lblResultRemoveTch.setStyleSheet("color : white")
        self.lblResultRemoveTch.setVisible(False)

        # İlgi alanı ekleme
        self.txtAddİlgi_alani = QLineEdit(self)
        self.txtAddİlgi_alani.move(320, 400)
        self.txtAddİlgi_alani.resize(100, 30)
        self.txtAddİlgi_alani.setPlaceholderText("ilgi alanı")
        self.txtAddİlgi_alani.setStyleSheet("color : black; background-color : white")

        self.myFont.setPointSize(9)
        self.btnAddİlgi_alani = QPushButton(self)
        self.btnAddİlgi_alani.setText("İlgi alanı ekle")
        self.btnAddİlgi_alani.setFont(self.myFont)
        self.btnAddİlgi_alani.clicked.connect(self.addIlgi_alani)
        self.btnAddİlgi_alani.setFixedSize(100, 30)
        self.btnAddİlgi_alani.move(450, 400)
        self.btnAddİlgi_alani.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblResultAddIlgi_alani = QLabel("Başarılı", self)
        self.lblResultAddIlgi_alani.move(570, 400)
        self.lblResultAddIlgi_alani.setFont(self.myFont)
        self.lblResultAddIlgi_alani.setStyleSheet("color : white")
        self.lblResultAddIlgi_alani.setVisible(False)

        # İlgi alanı sil
        self.txtRemoveİlgi_alani = QLineEdit(self)
        self.txtRemoveİlgi_alani.move(320, 450)
        self.txtRemoveİlgi_alani.resize(100, 30)
        self.txtRemoveİlgi_alani.setPlaceholderText("ilgi alanı")
        self.txtRemoveİlgi_alani.setStyleSheet(
            "color : black; background-color : white"
        )

        self.myFont.setPointSize(11)
        self.btnRemoveİlgi_alani = QPushButton(self)
        self.btnRemoveİlgi_alani.setText("İlgi alanı sil")
        self.btnRemoveİlgi_alani.setFont(self.myFont)
        self.btnRemoveİlgi_alani.clicked.connect(self.removeIlgi_alani)
        self.btnRemoveİlgi_alani.setFixedSize(100, 30)
        self.btnRemoveİlgi_alani.move(450, 450)
        self.btnRemoveİlgi_alani.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.lblRemoveIlgi_alani = QLabel("Başarılı", self)
        self.lblRemoveIlgi_alani.move(570, 450)
        self.lblRemoveIlgi_alani.setFont(self.myFont)
        self.lblRemoveIlgi_alani.setStyleSheet("color : white")
        self.lblRemoveIlgi_alani.setVisible(False)

        self.lblResultRemoveIlgi_alani = QLabel("Başarılı", self)
        self.lblResultRemoveIlgi_alani.move(570, 450)
        self.lblResultRemoveIlgi_alani.setFont(self.myFont)
        self.lblResultRemoveIlgi_alani.setStyleSheet("color : white")
        self.lblResultRemoveIlgi_alani.setVisible(False)

    def addStudent(self):
        ogr_no = self.txtAdd_ogr_no.text()
        isim = self.txtAdd_ogr_isim.text()
        soyİsim = self.txtAdd_ogr_soyIsim.text()
        sifre = self.txtAdd_ogr_sifre.text()
        ortalama = self.txtAdd_ogr_ort.text()

        self.txtAdd_ogr_no.setText = ""
        self.txtAdd_ogr_isim.setTextext = ""
        self.txtAdd_ogr_soyIsim.setText = ""
        self.txtAdd_ogr_sifre.setText = ""
        self.txtAdd_ogr_ort.setText = ""

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ogrenci (ogrenci_no, isim, soy_isim, genel_not_ortalaması, şifre)
                VALUES (%s, %s, %s, %s, %s) """,
                (ogr_no, isim, soyİsim, ortalama, sifre),
            )
            cursor.close()

            self.lblResultAddSt.setVisible(True)

        except:
            self.lblResultAddSt.setText = "Hata"
            self.lblResultAddSt.setVisible(True)

    def changeStudent(self):
        changeItem = self.cbxChangeOgr.currentText()
        no = self.txtChangeOgr_no.text()
        new_value = self.txtChangeOgr.text()

        self.txtChangeOgr_no.setText = ""
        self.txtChangeOgr.setText = ""

        try:
            cur = conn.cursor()
            query = f'UPDATE "ogrenci" SET {changeItem} = %s WHERE ogrenci_no = %s'
            cur.execute(query, (str(new_value), str(no)))
            cur.close()

            self.lblResultChangeSt.setVisible(True)

        except:
            self.lblResultChangeSt.setText = "Hata"
            self.lblResultChangeSt.setVisible(True)

    def removeStudent(self):
        no = self.txtRem_ogr_no.text()

        self.txtRem_ogr_no.setText = ""
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM ogrenci WHERE ogrenci_no = {no}"
            cursor.execute(query)
            cursor.close()

            self.lblResultRemoveSt.setVisible(True)

        except:
            self.lblResultRemoveSt.setText = "Hata"
            self.lblResultRemoveSt.setVisible(True)

    def addTeacher(self):
        isim = self.txtAdd_hoca_isim.text()
        soy_isim = self.txtAdd_hoca_soyIsim.text()
        sifre = self.txtAdd_hoca_sifre.text()
        acilan_dersler = self.txtAdd_acilan_ders.text()

        self.txtAdd_hoca_isim.setText = ""
        self.txtAdd_hoca_soyIsim.setText = ""
        self.txtAdd_hoca_sifre.setText = ""
        self.txtAdd_acilan_ders.setText = ""

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO hoca (isim, soy_isim, şifre, açılan_dersler)
                VALUES (%s, %s, %s, %s) """,
                (isim, soy_isim, sifre, acilan_dersler),
            )
            cursor.close()

            self.lblResultAddTch.setVisible(True)

        except:
            self.lblResultAddTch.setText = "Hata"
            self.lblResultAddTch.setVisible(True)

    def changeTeacher(self):
        sicil_no = self.txtChange_hoca_sicil_no.text()
        changeItem = self.cbxChangeHoca.currentText()
        newValue = self.txtChangeHoca.text()

        self.txtChange_hoca_sicil_no.setText = ""
        self.txtChangeHoca.setText = ""

        try:
            cur = conn.cursor()
            query = f'UPDATE "hoca" SET {changeItem} = %s WHERE sicil_numarası = %s'
            cur.execute(query, (str(newValue), str(sicil_no)))
            cur.close()

            self.lblResultChangeTch.setVisible(True)

        except:
            self.lblResultChangeTch.setText = "Hata"
            self.lblResultChangeTch.setVisible(True)

    def removeTeacher(self):
        sicil_no = self.txtRemove_hoca_sicil_no.text()
        self.txtRemove_hoca_sicil_no.setText = ""

        try:
            cursor = conn.cursor()
            query = f"DELETE FROM hoca WHERE sicil_numarası = {sicil_no}"

            cursor.execute(query)
            cursor.close()

            self.lblResultRemoveTch.setVisible(True)

        except:
            self.lblResultRemoveTch.setText = "Hata"
            self.lblResultRemoveTch.setVisible(True)

    def addIlgi_alani(self):
        ilgi_alani = self.txtAddİlgi_alani.text()
        self.txtAddİlgi_alani.setText = ""

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO ilgialanlari (ilgi_alanı) VALUES (%s)"
            cursor.execute(sql, (ilgi_alani,))
            cursor.close()

            self.lblResultAddIlgi_alani.setVisible(True)

        except:
            self.lblResultAddIlgi_alani.setText = "Hata"
            self.lblResultAddIlgi_alani.setVisible(True)

    def removeIlgi_alani(self):
        ilgi_alani = self.txtRemoveİlgi_alani.text()
        self.txtRemoveİlgi_alani.setText = ""

        try:
            cursor = conn.cursor()
            query = f"DELETE FROM ilgialanlari WHERE ilgi_alanı = %s"
            cursor.execute(query, (ilgi_alani,))
            cursor.close()

            self.lblRemoveIlgi_alani.setVisible(True)

        except Exception:
            print(Exception)
            self.lblRemoveIlgi_alani.setText = "Hata"
            self.lblRemoveIlgi_alani.setVisible(True)

    def setlblTitleText(self, text):
        self.lblTitle.setText(text)

    def talep_sayilari_onay(self):
        for row, ders_adi in enumerate(self.dersler):
            text = self.talep_hoca_tablosu.item(row, 1).text()
            cur = conn.cursor()
            query = 'UPDATE "açılanDersler" SET talep_edilebilecek_hoca_sayısı = %s WHERE ders_adı = %s'
            cur.execute(query, (str(text), str(ders_adi)))
            cur.close()

        mesaj_karakter = self.txtChar.text()
        cur = conn.cursor()
        query = 'UPDATE "yonetici" SET mesajlaşma_karakter_sayısı = %s'
        cur.execute(query, (mesaj_karakter,))
        cur.close()

        talep_onay = self.txtConfirmNum.text()
        cur = conn.cursor()
        query = 'UPDATE "yonetici" SET bir_hoca_kac_talep_onaylayabilir = %s'
        cur.execute(query, (talep_onay,))
        cur.close()



        self.talep_hoca_tablosu.setVisible(False)
        self.btntalep_hoca.setVisible(False)
        self.lblChar.setVisible(False)
        self.txtChar.setText = ""
        self.txtChar.setVisible(False)
        self.lblConfirmNum.setVisible(False)
        self.txtConfirmNum.setText = ""
        self.txtConfirmNum.setVisible(False)
        

    def start(self):
        char = self.txtChar.text()
        cur = conn.cursor()
        query = 'UPDATE "yonetici" SET mesajlaşma_karakter_sayısı = %s WHERE kullanıcı_adı = %s'
        cur.execute(query, (char, "admin"))
        cur.close()

    def ogrenci_talep_gecmisi(self):
        try:
            self.talepOgrenciPanel = Ogrenci_Talep_Geçmişi()
            self.talepOgrenciPanel.setVisible(True)
            self.talepOgrenciPanel.show()
        except:
            pass

    def hoca_talep_gecmisi(self):
        try:
            self.talepHocaPanel = Hoca_Talep_Geçmişi()
            self.talepHocaPanel.setVisible(True)
            self.talepHocaPanel.show()
        except:
            pass

    def ogrenci_ders_ekleme(self):
        try:
            self.dersEklemePanel = Ogrenci_Ders_Ekleme()
            self.dersEklemePanel.setVisible(True)
            self.dersEklemePanel.show()
        except:
            pass

    
    def asama2(self):
        self.lblChar.close()
        self.txtChar.close()
        self.btntalep_hoca.setVisible(False)
        self.talep_hoca_tablosu.close()
        self.txtConfirmNum.close()
        self.btnTime.close()
        self.btnStart.close()
        self.btntalep_ogr.close()
        self.btn_ders_ekleme.close()
        self.txtAdd_ogr_no.close()
        self.txtAdd_ogr_isim.close()
        self.txtAdd_ogr_soyIsim.close()
        self.txtAdd_ogr_sifre.close()
        self.txtAdd_ogr_ort.close()
        self.btnAdd_ogr.close()
        self.lblResultAddSt.close()
        self.txtChangeOgr_no.close()
        self.cbxChangeOgr.close()
        self.txtChangeOgr.close()
        self.lblResultChangeSt.close()
        self.btnChange.close()
        self.txtRem_ogr_no.close()
        self.btnRem_ogr.close()
        self.lblResultRemoveSt.close()
        self.txtAdd_hoca_isim.close()
        self.txtAdd_hoca_soyIsim.close()
        self.txtAdd_hoca_sifre.close()
        self.txtAdd_acilan_ders.close()
        self.btnAdd_hoca.close()
        self.lblResultAddTch.close()
        self.txtChange_hoca_sicil_no.close()
        self.cbxChangeHoca.close()
        self.txtChangeHoca.close()
        self.lblResultChangeTch.close()
        self.btnChangeHoca.close()
        self.txtRemove_hoca_sicil_no.close()
        self.btnRemoveHoca.close()
        self.lblResultRemoveTch.close()
        self.txtAddİlgi_alani.close()
        self.btnAddİlgi_alani.close()
        self.lblResultAddIlgi_alani.close()
        self.txtRemoveİlgi_alani.close()
        self.btnRemoveİlgi_alani.close()
        self.lblRemoveIlgi_alani.close()
        self.lblResultRemoveIlgi_alani.close()
        self.lblConfirmNum.close()
        
        self.myFont.setPointSize(10)
        self.btn1 = QPushButton(self)
        self.btn1.clicked.connect(self.rastgele_atama)
        self.btn1.setText("Rastgele Atama")
        self.btn1.setFont(self.myFont)
        self.btn1.setFixedSize(280, 80)
        self.btn1.move(120, 300)
        self.btn1.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn1.setVisible(True)
        
        
        
        self.myFont.setPointSize(10)
        self.btn2 = QPushButton(self)
        self.btn2.clicked.connect(self.not_ortalamasina_gore_atama)
        self.btn2.setText("Not Ortalamasına Göre Atama")
        self.btn2.setFont(self.myFont)
        self.btn2.setFixedSize(280, 80)
        self.btn2.move(510, 300)
        self.btn2.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn2.setVisible(True)
        
        
        
        self.myFont.setPointSize(10)
        self.btn3 = QPushButton(self)
        self.btn3.clicked.connect(self.belirli_derslere_gore_atama)
        self.btn3.setText("Belirli Derslere Göre Atama")
        self.btn3.setFont(self.myFont)
        self.btn3.setFixedSize(280, 80)
        self.btn3.move(900, 300)
        self.btn3.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn3.setVisible(True)
    
        
    def rastgele_atama(self):
        # Aşama 1 ######################################################################################################
            # Öğrenci listesini almak için bir işlev
        def get_student_list_from_database():

            cursor = conn.cursor()
            cursor.execute(
                "SELECT ogrenci_no, isim, soy_isim FROM ogrenci WHERE anlaşma_talep_sayısı = '0'"
            )

            student_list = cursor.fetchall()

            cursor.close()

            return student_list

        # Öğretmen listesini almak için bir işlev
        def get_teacher_list_from_database():

            cursor = conn.cursor()
            cursor.execute(
                "SELECT sicil_numarası, isim, soy_isim FROM hoca"
            )

            teacher_list = cursor.fetchall()

            cursor.close()

            return teacher_list

        
        # Açılan Derslerin Listesi
        def lesson_list():
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ders_kodu, ders_adı FROM \"açılanDersler\""
            )

            lesson_list = cursor.fetchall()
            print(lesson_list)
            cursor.close()
            
            return lesson_list
        
        def assign_student_to_teacher(student_id, teacher_id, lesson):
            cursor = conn.cursor()
            query = "SELECT EXISTS (SELECT 1 FROM ogrenci_aldigi_dersler WHERE ders_kodu = %s AND ogrenci_no = %s)"
            cursor.execute(query, (lesson[0], student[0]))
            result = cursor.fetchone()[0]
            cursor.close()
            
            if not result :
                
                cursor = conn.cursor()
                query = f"SELECT hoca_sicil_numarası FROM \"açılanDersler_hoca\" WHERE ders_kodu = '{lesson[0]}'"
                cursor.execute(query)
                results = cursor.fetchall()
                results = [result[0] for result in results]
                
                random.shuffle(results)
                if len(results) != 0:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO ogrenci_aldigi_dersler (ogrenci_no, ders_kodu, hoca_sicil_no) VALUES (%s, %s, %s)",
                        (student[0], lesson[0], results[0]),
                    )
                    conn.commit()
                    print(f"{student[0]} numaralı öğrenci ataması {results[0]} sicil no'lu akademisyene yapıldı")
                    cursor.close()
                

        # Öğrenci ve öğretmen listelerini alın (örneğin student_list ve teacher_list olarak).
        student_list = get_student_list_from_database()
        teacher_list = get_teacher_list_from_database()

        # Eğer öğretmen listesi boşsa hata almamak için kontrol yapın
        if not teacher_list:
            print("Öğretmen listesi boş, atama yapılamadı.")
            return

        random.shuffle(student_list)
        random.shuffle(teacher_list)
        
    #   Öğrencileri sırayla öğretmenlere atayın.
        for i, student in enumerate(student_list):
            for lesson in lesson_list():
                # Öğrenci ve öğretmen listelerini karıştırın.
                
                teacher = teacher_list[i % len(teacher_list)]
                assign_student_to_teacher(student, teacher, lesson)

    def not_ortalamasina_gore_atama(self):
        pass
    
    
    def belirli_derslere_gore_atama(self):
        pass
    
    
    
    
# Öğrenci Paneli
class StudentPanel(QWidget):
    def __init__(self, ogrenci_no):
        super().__init__()
        self.ogrenci_no = ogrenci_no
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
        self.btn_sec.setText("Talep Gönder")
        self.btn_sec.setFont(self.myFont)
        self.btn_sec.setFixedSize(180, 50)
        self.btn_sec.move(200, 50)
        self.btn_sec.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_sec.setVisible(False)
        self.btn_sec.clicked.connect(self.talep_olustur)

        self.myFont.setPointSize(11)
        self.btn_filter = QPushButton(self)
        self.btn_filter.setText("Hoca Filtrele")
        self.btn_filter.setFont(self.myFont)
        self.btn_filter.setFixedSize(180, 50)
        self.btn_filter.move(400, 50)
        self.btn_filter.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_filter.setVisible(False)
        self.btn_filter.clicked.connect(self.filter_teacher)

        self.myFont.setPointSize(11)
        self.btn_send_message = QPushButton(self)
        self.btn_send_message.setText("Mesaj Gönder")
        self.btn_send_message.setFont(self.myFont)
        self.btn_send_message.setFixedSize(180, 50)
        self.btn_send_message.move(600, 50)
        self.btn_send_message.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_send_message.setVisible(False)
        self.btn_send_message.clicked.connect(self.send_message)

        self.myFont.setPointSize(11)
        self.btn_inmail = QPushButton(self)
        self.btn_inmail.setText("Gelen Mesajlar")
        self.btn_inmail.setFont(self.myFont)
        self.btn_inmail.setFixedSize(180, 50)
        self.btn_inmail.move(800, 50)
        self.btn_inmail.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_inmail.setVisible(False)
        self.btn_inmail.clicked.connect(self.in_mail)

        self.myFont.setPointSize(11)
        self.btn_talepler = QPushButton(self)
        self.btn_talepler.setText("Taleplerim")
        self.btn_talepler.setFont(self.myFont)
        self.btn_talepler.setFixedSize(180, 50)
        self.btn_talepler.move(990, 50)
        self.btn_talepler.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_talepler.setVisible(False)
        self.btn_talepler.clicked.connect(self.talep_listele)

        # Ders Seçim Tablosu
        self.lessonTable = QTableWidget(self)
        self.lessonTable.move(10, 120)
        self.lessonTable.setFixedSize(700, 500)
        self.lessonTable.setVisible(False)

        self.hoca_talepTable = QTableWidget(self)
        self.hoca_talepTable.move(715, 120)
        self.hoca_talepTable.setFixedSize(560, 500)
        self.hoca_talepTable.setStyleSheet("color : black; background-color : white")
        self.hoca_talepTable.setVisible(False)

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
        self.btn_filter.setVisible(True)
        self.btn_inmail.setVisible(True)
        self.btn_talepler.setVisible(True)
        self.btn_send_message.setVisible(True)
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
        
        for lesson in lessons:     
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO gecmis_donem_dersler (ders_kodu, ders_adı, ders_statusu, ogretim_dili, \"AKTS\")
                    VALUES (%s, %s, %s, %s, %s) """,
                    (lesson["ders_kodu"], lesson["ders_adi"], lesson["ders_statusu"], lesson["ogretim_dili"], str(lesson["AKTS"])),
                )
                cursor.close()
        
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO transkript (ogrenci_no, ders_kodu, harf_notu)
                    VALUES (%s, %s, %s) """,
                    (self.ogrenci_no, lesson["ders_kodu"], lesson["not"]),
                )
                cursor.close()
                
                
        self.transcript_panel = Transcript(lessons)
        self.transcript_panel.show()

        
        self.ders_secim_tablo()
        self.hoca_talep_tablo()

    def ders_secim_tablo(self, filter_set=set()):
        lessons = dict()
        cursor = conn.cursor()
        query = 'SELECT ders_kodu, ders_adı FROM "açılanDersler"'
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            ders_kodu = row[0]
            ders_adi = row[1]
            lessons[ders_kodu] = ders_adi

        self.lessons_teacher = dict()
        for ders_kodu, ders_adi in lessons.items():
            table = "açılanDersler_hoca"
            kod = "ders_kodu"

            cur = conn.cursor()
            query = f"SELECT hoca_sicil_numarası FROM \"{table}\" WHERE {kod} = '{ders_kodu}'"
            cur.execute(query)
            results = cur.fetchall()
            sicil_numbers = [result[0] for result in results]
            cur.close()

            if len(filter_set) != 0:
                for number in sicil_numbers:
                    for ilgi_alanı in filter_set:
                        table = "ilgialanı_hoca"
                        cur = conn.cursor()
                        query = f"SELECT id FROM \"{table}\" WHERE ilgi_alanı = '{ilgi_alanı}' AND hoca_sicil_numarası = '{number}'"
                        cur.execute(query)
                        results = cur.fetchall()
                        cur.close()

                        if len(results) == 0:
                            del sicil_numbers[sicil_numbers.index(number)]

            self.teachers = []
            teacher_list = []
            for number in sicil_numbers:
                table = "hoca"
                column = "sicil_numarası"

                cur = conn.cursor()
                query = f"SELECT isim, soy_isim FROM \"{table}\" WHERE {column} = '{number}'"
                cur.execute(query)
                results = cur.fetchall()
                for result in results:
                    l = list()
                    l.append(result[0])
                    l.append(result[1])
                teacher_list.append(l)
                
            self.lessons_teacher[ders_adi] = teacher_list

        max_element_count = 0

        for lesson, self.teachers in self.lessons_teacher.items():
            if len(self.teachers) > max_element_count:
                max_element_count = len(self.teachers)

        self.lessonTable.setStyleSheet("color : black; background-color : white")
        self.lessonTable.setRowCount(len(self.lessons_teacher))
        self.lessonTable.setColumnCount(max_element_count + 1)

        labels = ["Ders Adı"]
        for i in range(max_element_count):
            labels.append("Öğretmenler")
        
        labels.append("Talep Gönder")
        
        self.lessonTable.setHorizontalHeaderLabels(labels)

        row = 0
        for lesson, self.teachers in self.lessons_teacher.items():
            lesson_item = QTableWidgetItem(lesson)
            self.lessonTable.setItem(row, 0, lesson_item)
            table = "açılanDersler"
            cur = conn.cursor()
            query = f"SELECT talep_edilebilecek_hoca_sayısı FROM \"{table}\" WHERE ders_adı = %s"
            cur.execute(query, (lesson,))
            results = cur.fetchall()
            results = results[0][0]
            cur.close()
            if len(self.teachers) > 0:
                self.teachers.append([])
            for col, teacher in enumerate(self.teachers, 1):
                if col == len(self.teachers)-1:
                    self.button = QPushButton(self)
                    self.button.setText("talep gönder")
                    self.button.setFixedSize(120, 30)
                    self.button.setStyleSheet("color : white; background-color : brown; border-radius : 5px")
                    index = row
                    #self.button.clicked.connect(lambda _, idx=index: self.iptal(results[idx], idx))
                    self.lessonTable.setCellWidget(row, col, self.button)
                    
                elif col > results:
                    continue
                
                elif len(teacher) != 0:
                    print(len(teacher))
                    teacher_combobox = QComboBox()
                    teacher_combobox.addItems(
                        [teacher[0] + " " + teacher[1]]
                    )
                    self.lessonTable.setCellWidget(row, col, teacher_combobox)
            row += 1

        self.lessonTable.setVisible(True)
        self.hoca_talepTable.setVisible(True)

    def hoca_talep_tablo(self):
        table = "talep_hoca"
        cursor = conn.cursor()
        query = f"SELECT hoca_sicil_no, ders_kodu FROM {table} WHERE ogrenci_no = {self.ogrenci_no}"
        cursor.execute(query)
        results = cursor.fetchall()
        table_list = []

        for result in results:
            table = "hoca"
            cursor = conn.cursor()
            query = (
                f"SELECT isim, soy_isim FROM {table} WHERE sicil_numarası = {result[0]}"
            )
            cursor.execute(query)
            ogr_isim = cursor.fetchall()
            ogr_isim = [ogr[0] + " " + ogr[1] for ogr in ogr_isim]

            table = "açılanDersler"
            cursor = conn.cursor()
            query = f"SELECT ders_adı FROM \"{table}\" WHERE ders_kodu = '{result[1]}'"
            cursor.execute(query)
            ders_isim = cursor.fetchall()
            ders_isim = [d[0] for d in ders_isim]

            table_list.append((ogr_isim, ders_isim, "onayla"))

        self.hoca_talepTable.setColumnCount(3)
        self.hoca_talepTable.setRowCount(len(table_list))
        self.hoca_talepTable.setHorizontalHeaderLabels(["Hoca", "Ders Adı", "Onay"])

        for row_index, row_data in enumerate(table_list):
            for col_index, col_data in enumerate(row_data):
                if col_index == 2:
                    self.button = QPushButton(self)
                    self.button.setText("Onayla")
                    self.button.setFixedSize(125, 37)
                    self.button.setStyleSheet(
                        "color : white; background-color : black; border-radius : 5px"
                    )
                    self.button.clicked.connect(
                        lambda: self.hoca_talep_onay(list(results[row_index]))
                    )
                    self.hoca_talepTable.setCellWidget(
                        row_index, col_index, self.button
                    )

                else:
                    self.hoca_talepTable.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data[0]))
                    )
                    self.hoca_talepTable.setColumnWidth(col_index, 200)

    def hoca_talep_onay(self, results):
        ogrenci_no = str(self.ogrenci_no)
        sicil_no = results[0]
        ders_kodu = results[1]

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ogrenci_aldigi_dersler (ogrenci_no, ders_kodu, hoca_sicil_no)
            VALUES (%s, %s, %s) """,
            (ogrenci_no, ders_kodu, sicil_no),
        )
        cursor.close()

        cursor = conn.cursor()
        sql = "DELETE FROM talep_hoca WHERE hoca_sicil_no = %s AND ders_kodu = %s AND ogrenci_no = %s"
        cursor.execute(sql, (sicil_no, ders_kodu, ogrenci_no))
        conn.commit()  # Değişiklikleri veritabanına kaydetmek için commit yapın
        cursor.close()
        
        self.hoca_talep_tablo()

    # Transkript panelini gösterip gizleme
    def toggle_table(self):
        self.table_visible = not self.table_visible
        self.transcript_panel.setVisible(self.table_visible)

    def setlblTitleText(self, text):
        self.lblTitle.setText(text)

    def filter_teacher(self):
        self.filterTeacherPanel = Hoca_Filtreleme()
        self.filterTeacherPanel.show()

    def send_message(self):
        self.mesaj_gonder_panel = Ogrenci_Mesaj_Gonder(self.ogrenci_no)
        self.mesaj_gonder_panel.show()

    def in_mail(self):
        self.gelen_mesaj_panel = Ogrenci_Gelen_Mesaj(self.ogrenci_no)
        self.gelen_mesaj_panel.show()

    def talep_olustur(self):
        data = {}
        for row in range(self.lessonTable.rowCount()):
            print(self.lessons_teacher.values())
            teachers = list(self.lessons_teacher.values())
            teachers = [teacher[0] if len(teacher) != 0 else [] for teacher in teachers]
            row_data = {}
            string_item = self.lessonTable.item(row, 0)
            combo_item = self.lessonTable.cellWidget(row, 1)

            if string_item:
                row_data["Ders Adı"] = string_item.text()

            if combo_item:
                row_data["Öğretmen"] = teachers[row]

            data[f"Satır {row+1}"] = row_data
            print(teachers[row])
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO talep_ogrenci (ogrenci_no, ders_isim, hoca_isim, hoca_soy_isim, durum)
                VALUES (%s, %s, %s, %s, %s) """,
                (
                    self.ogrenci_no,
                    row_data["Ders Adı"],
                    teachers[row][0],
                    teachers[row][1],
                    "beklemede",
                ),
            )
            cursor.close()

        print(data)

        """
        table = "talep_ogrenci"
        ogrenci_no = self.ogrenci_no
        ders_isim = 
        hoca_isim =
        hoca_soy_isim ="""

    def talep_listele(self):
        self.talep_list_panel = Ogrenci_Talep_Gecmisi(self.ogrenci_no)
        self.talep_list_panel.show()


class Ogrenci_Talep_Gecmisi(QWidget):
    def __init__(self, ogrenci_no):
        super().__init__()
        self.ogrenci_no = ogrenci_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Taleplerim")
        self.move(900, 300)
        self.setFixedSize(600, 400)

        self.lblTitle = QLabel("Taleplerim", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)
        
        self.init()
        
    def init(self):
        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ders Isim", "Hoca Isim", "Durum"])
        self.table.setStyleSheet("color : black; background-color : white")
        table = "talep_ogrenci"
        cur = conn.cursor()
        query = f"SELECT ders_isim, hoca_isim, hoca_soy_isim, durum, id FROM {table} WHERE ogrenci_no = {self.ogrenci_no}"
        cur.execute(query)
        results = cur.fetchall()
        results = [
            [result[0], result[1] + " " + result[2], result[3], result[4]] for result in results
        ]
        print(results[0])
        cur.close()
        self.table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, col_data in enumerate(row_data):
                if col_index == 2 and col_data == "beklemede":
                    print(results[row_index])
                    self.button = QPushButton(self)
                    self.button.setText("geri çek")
                    self.button.setFixedSize(143, 68)
                    self.button.setStyleSheet("color : white; background-color : brown; border-radius : 5px")
                    index = row_index
                    self.button.clicked.connect(lambda _, idx=index: self.iptal(results[idx], idx))
                    self.table.setCellWidget(row_index, col_index, self.button)
                elif col_index != 4:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )
                self.table.setRowHeight(row_index, 70)
                self.table.setColumnWidth(col_index, 150)

    def iptal(self, results, index):
        print(results)
        cursor = conn.cursor()
        query = f"DELETE FROM talep_ogrenci WHERE id = {results[3]}"
        cursor.execute(query)
        cursor.close()
        self.table.removeRow(index)
        
        

class Ogrenci_Mesaj_Gonder(QWidget):
    def __init__(self, ogrenci_no):
        super().__init__()
        self.ogrenci_no = ogrenci_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Hocaya mesaj gönder")
        self.move(900, 300)
        self.setFixedSize(600, 400)

        self.lblTitle = QLabel("Hocaya Mesaj Gönder", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        self.myFont.setPointSize(9)
        self.txtMesaj = QTextEdit(self)
        self.txtMesaj.move(10, 50)
        self.txtMesaj.resize(580, 200)
        self.txtMesaj.setPlaceholderText("Mesajınızı girin...")
        self.txtMesaj.setStyleSheet("color : black; background-color : white")

        self.txtsicil_no = QLineEdit(self)
        self.txtsicil_no.move(250, 260)
        self.txtsicil_no.resize(100, 30)
        self.txtsicil_no.setPlaceholderText("sicil no")
        self.txtsicil_no.setStyleSheet("color : black; background-color : white")

        self.btnGonder = QPushButton(self)
        self.btnGonder.setText("Mesajı Gönder")
        self.btnGonder.setFont(self.myFont)
        self.btnGonder.setFixedSize(120, 50)
        self.btnGonder.move(230, 330)
        self.btnGonder.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btnGonder.clicked.connect(self.gonder)

        self.myFont.setPointSize(8)
        self.lblMsgResult = QLabel("Mesaj Gönderildi", self)
        self.lblMsgResult.move(230, 310)
        self.lblMsgResult.setFont(self.myFont)
        self.lblMsgResult.setStyleSheet("color : white")
        self.lblMsgResult.setVisible(False)

    def setlblText(self):
        self.txtMesaj.setText("")
        self.txtsicil_no.setText("")
    
    def setResultText(self, text):
        self.lblMsgResult.setText(text)

    def gonder(self):
        ogrenci_no = self.ogrenci_no
        sicil_no = self.txtsicil_no.text()
        mesaj = self.txtMesaj.toPlainText()

        table = "yonetici"
        cur = conn.cursor()
        query = f"SELECT mesajlaşma_karakter_sayısı FROM {table}"
        cur.execute(query)

        karakter = cur.fetchall()
        karakter = karakter[0][0]
        cur.close()

        
        if len(mesaj) <= karakter:
            try:
                self.setlblText()
                
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO mesaj_ogrenci (ogrenci_no, mesaj, sicil_no)
                    VALUES (%s, %s, %s) """,
                    (ogrenci_no, mesaj, sicil_no),
                )
                cursor.close()

                self.setResultText("Mesaj Gönderildi")
                self.lblMsgResult.setVisible(True)

            except:
                self.setResultText("Hata")
                self.lblMsgResult.setVisible(True)

        else:
            self.setResultText(f"Max.: {karakter} - Mesaj: {len(mesaj)}")
            self.lblMsgResult.setVisible(True)
        
        

class Ogrenci_Gelen_Mesaj(QWidget):
    def __init__(self, ogrenci_no):
        super().__init__()
        self.ogrenci_no = ogrenci_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Gelen Mesajlar")
        self.move(900, 300)
        self.setFixedSize(800, 600)

        self.lblTitle = QLabel("Gelen mesajlar", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        table = "mesaj_hoca"
        cur = conn.cursor()
        query = f"SELECT id, sicil_no, mesaj FROM {table} WHERE ogrenci_no = {self.ogrenci_no}"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()


        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(3)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Mesaj Id", "Gönderen Hoca Sicil No", "Mesaj"])
        self.table.setStyleSheet("color : black; background-color : white")


        for row_index, row_data in enumerate(results):
            for col_index, col_data in enumerate(row_data):
                if col_index == 2:
                    self.TextEdit = QTextEdit(self)
                    self.TextEdit.setStyleSheet(
                        "color: black; background-color : white"
                    )
                    self.TextEdit.setFixedSize(150, 70)
                    self.TextEdit.setText(str(col_data))
                    self.table.setCellWidget(row_index, col_index, self.TextEdit)
                else:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )
                self.table.setRowHeight(row_index, 70)
                self.table.setColumnWidth(col_index, 150)


# Hoca Paneli
class TeacherPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.table_visible = True
        self.sicil_no = int()

    def initUI(self):
        self.arr = []

        self.setStyleSheet("background-color: rgb(140, 0, 0);")

        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Hoca Paneli")
        self.move(600, 200)
        self.setFixedSize(1280, 720)

        self.lblTitle = QLabel(self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(12)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        self.myFont.setPointSize(10)
        self.btnAddİlgi_alani = QPushButton(self)
        self.btnAddİlgi_alani.setText("İlgi alanı ekle")
        self.btnAddİlgi_alani.setFont(self.myFont)
        self.btnAddİlgi_alani.clicked.connect(self.ilgi_alani_ekle)
        self.btnAddİlgi_alani.setFixedSize(110, 40)
        self.btnAddİlgi_alani.move(350, 10)
        self.btnAddİlgi_alani.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(9)
        self.btnFilterOgr = QPushButton(self)
        self.btnFilterOgr.setText("Öğrenci Listele")
        self.btnFilterOgr.setFont(self.myFont)
        self.btnFilterOgr.clicked.connect(self.list_student)
        self.btnFilterOgr.setFixedSize(110, 40)
        self.btnFilterOgr.move(470, 10)
        self.btnFilterOgr.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(9)
        self.btn_msj_gonder = QPushButton(self)
        self.btn_msj_gonder.setText("Mesaj Gönder")
        self.btn_msj_gonder.setFont(self.myFont)
        self.btn_msj_gonder.clicked.connect(self.mesaj_gonder)
        self.btn_msj_gonder.setFixedSize(110, 40)
        self.btn_msj_gonder.move(590, 10)
        self.btn_msj_gonder.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(9)
        self.btn_gelen_msg = QPushButton(self)
        self.btn_gelen_msg.setText("Gelen Mesajlar")
        self.btn_gelen_msg.setFont(self.myFont)
        self.btn_gelen_msg.clicked.connect(self.gelen_mesajlar)
        self.btn_gelen_msg.setFixedSize(110, 40)
        self.btn_gelen_msg.move(710, 10)
        self.btn_gelen_msg.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )

        self.myFont.setPointSize(9)
        self.btn_gelen_talep = QPushButton(self)
        self.btn_gelen_talep.setText("Gelen Talepler")
        self.btn_gelen_talep.setFont(self.myFont)
        self.btn_gelen_talep.clicked.connect(self.gelen_talepler)
        self.btn_gelen_talep.setFixedSize(110, 40)
        self.btn_gelen_talep.move(830, 10)
        self.btn_gelen_talep.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        
        
        
    def setlblTitleText(self, text):
        print(text)
        self.lblTitle.setText(text)
        print(self.lblTitle.text())

    def ilgi_alani_ekle(self):
        self.ilgiAlaniPanel = Hoca_ilgi_alani_ekleme(self.sicil_no)
        self.ilgiAlaniPanel.show()

    def list_student(self):
        self.listPanel = ListStudent1()
        self.listPanel2 = ListStudent2(self.sicil_no)
        self.listPanel.show()
        self.listPanel2.show()

    def mesaj_gonder(self):
        self.mesaj_gonder_panel = Hoca_Mesaj_Gonder(self.sicil_no)
        self.mesaj_gonder_panel.show()

    def gelen_mesajlar(self):
        self.gelen_mesaj_panel = Hoca_Gelen_Mesaj(self.sicil_no)
        self.gelen_mesaj_panel.show()

    def gelen_talepler(self):
        
        self.gelen_talep_panel = Gelen_Talep_Panel(self.sicil_no)
        self.gelen_talep_panel.show()
        
        
                    
    
    
class Gelen_Talep_Panel(QWidget):
    def __init__(self, sicil_no):
        super().__init__()
        self.sicil_no = sicil_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Gelen Mesajlar")
        self.move(900, 300)
        self.setFixedSize(800, 600)

        self.lblTitle = QLabel("Gelen mesajlar", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        self.init()
    
    def init(self):
        table = "hoca"
        cur = conn.cursor()
        query = f"SELECT isim, soy_isim FROM {table} WHERE sicil_numarası =  {self.sicil_no}"
        cur.execute(query)
        results = cur.fetchall()
        results = results[0]
        cur.close()
        
        
        table = "talep_ogrenci"
        cur = conn.cursor()
        query = f"SELECT ogrenci_no, ders_isim FROM {table} WHERE hoca_isim =  '{results[0]}' AND hoca_soy_isim = '{results[1]}'"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()
        
        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(4)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Öğrenci No", "Ders Adı", "Onay", "Red"])
        self.table.setStyleSheet("color : black; background-color : white")

        for row_index, row_data in enumerate(results):
            row_data = list(row_data)
            row_data.append("Onay")
            row_data.append("Red")
            row_data = tuple(row_data)
            for col_index, col_data in enumerate(row_data):
                if col_index == 2:
                    
                    self.button = QPushButton(self)
                    self.button.setText("Onay")
                    self.button.setFixedSize(125, 40)
                    self.button.setStyleSheet(
                        "color : white; background-color : brown; border-radius: 5px"
                    )
                    self.button.clicked.connect(lambda _, idx=row_index: self.onay(results[idx], idx))
                    
                    self.table.setCellWidget(row_index, col_index, self.button)
                
                elif col_index == 3:
                    self.button = QPushButton(self)
                    self.button.setText("Red")
                    self.button.setFixedSize(125, 40)
                    self.button.setStyleSheet(
                        "color : white; background-color : brown; border-radius: 5px"
                    )
                    self.button.clicked.connect(lambda _, idx=row_index: self.red(results[idx], idx))
                    
                    self.table.setCellWidget(row_index, col_index, self.button)
                    
                else:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )

    
    def onay(self,result,index):
        table = "ogrenci_aldigi_dersler"
        ogrenci_no = result[0]
        
        table = "açılanDersler"
        cur = conn.cursor()
        query = f'SELECT ders_kodu FROM "{table}" WHERE ders_adı = %s'
        cur.execute(query, (result[1],))
        ders_kodu = cur.fetchone()
        ders_kodu = ders_kodu[0]
        cur.close()

        table = "ogrenci_aldigi_dersler"
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {table} (ogrenci_no, ders_kodu, hoca_sicil_no)
            VALUES (%s, %s, %s) """,
            (ogrenci_no, ders_kodu, self.sicil_no),
        )
        cursor.close()
        
        cursor = conn.cursor()
        query = f"DELETE FROM talep_ogrenci WHERE ogrenci_no = {ogrenci_no} AND ders_isim = '{result[1]}'"
        cursor.execute(query)
        cursor.close()

        self.table.removeRow(index)
    
    def red(self, result, index):
        
        cursor = conn.cursor()
        query = f"DELETE FROM talep_ogrenci WHERE ogrenci_no = {result[0]} AND ders_isim = '{result[1]}'"
        cursor.execute(query)
        cursor.close()

        self.table.removeRow(index)


class Transcript(QWidget):
    def __init__(self, lessons):
        super().__init__()
        self.lessons = lessons

        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Transkript")
        self.move(100, 100)
        self.setFixedSize(860, 580)

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


class Ogrenci_Talep_Geçmişi(QWidget):
    def __init__(self):
        super().__init__()
        self.str = str
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenci Talep Geçmişi")
        self.move(100, 100)
        self.setFixedSize(825, 525)

        table = "talep_ogrenci"

        cur = conn.cursor()
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 10, 800, 500)
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(len(results[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["Id", "Öğrenci No", "Ders Kodu", "Hoca Sicil No"]
        )
        self.tableWidget.setStyleSheet("color : black; background-color : white")

        for row, talep in enumerate(results):
            for col, value in enumerate(talep):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)


class Hoca_Talep_Geçmişi(QWidget):
    def __init__(self):
        super().__init__()
        self.str = str
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Hoca Talep Geçmişi")
        self.move(100, 100)
        self.setFixedSize(825, 525)

        table = "talep_hoca"

        cur = conn.cursor()
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        results = cur.fetchall()
        print(results)
        cur.close()

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 10, 800, 500)
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(len(results[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["Id", "Hoca Sicil No", "Ders Kodu", "Öğrenci No"]
        )
        self.tableWidget.setStyleSheet("color : black; background-color : white")

        for row, talep in enumerate(results):
            for col, value in enumerate(talep):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)


# Yönetici Paneli Öğrenciye Ders Ekleme
class Ogrenci_Ders_Ekleme(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.str = str
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenciye Ders Ekleme")
        self.move(700, 500)
        self.setFixedSize(400, 200)

        self.txtOgrNo = QLineEdit(self)
        self.txtOgrNo.move(10, 50)
        self.txtOgrNo.resize(80, 40)
        self.txtOgrNo.setPlaceholderText("öğrenci no")
        self.txtOgrNo.setStyleSheet("color : black; background-color : white")

        self.txtDersKodu = QLineEdit(self)
        self.txtDersKodu.move(100, 50)
        self.txtDersKodu.resize(80, 40)
        self.txtDersKodu.setPlaceholderText("ders kodu")
        self.txtDersKodu.setStyleSheet("color : black; background-color : white")

        self.txtHocaSicil = QLineEdit(self)
        self.txtHocaSicil.move(190, 50)
        self.txtHocaSicil.resize(80, 40)
        self.txtHocaSicil.setPlaceholderText("sicil no")
        self.txtHocaSicil.setStyleSheet("color : black; background-color : white")

        self.myFont.setPointSize(7)
        self.btnDersEkle = QPushButton(self)
        self.btnDersEkle.setText("Dersi Ekle")
        self.btnDersEkle.setFont(self.myFont)
        self.btnDersEkle.setFixedSize(80, 40)
        self.btnDersEkle.move(290, 50)
        self.btnDersEkle.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btnDersEkle.clicked.connect(self.ogrenci_ders_ekleme)


    def ogrenci_ders_ekleme(self):
        ogr_no = self.txtOgrNo.text()
        ders_kodu = self.txtDersKodu.text()
        hoca_sicil_no = self.txtHocaSicil.text()

        self.txtOgrNo.setText = ""
        self.txtDersKodu.setText = ""
        self.txtHocaSicil.setText = ""

        table = "ogrenci_aldigi_dersler"

        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {table} (ogrenci_no, ders_kodu, hoca_sicil_no)
            VALUES (%s, %s, %s) """,
            (ogr_no, ders_kodu, hoca_sicil_no),
        )
        cursor.close()


# Yönetici Paneli Öğrenciye Ders Ekleme
class Hoca_ilgi_alani_ekleme(QWidget):
    def __init__(self, sicil_no):
        super().__init__()
        self.sicil_no = sicil_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle("İlgi Alanı Ekleme")
        self.move(700, 500)
        self.setFixedSize(400, 200)

        table = "ilgialanlari"
        cur = conn.cursor()
        query = f"SELECT ilgi_alanı FROM {table}"
        cur.execute(query)

        results = cur.fetchall()
        results = [result[0] for result in results]
        cur.close()

        self.cbxIlgi_alanlari = QComboBox(self)
        self.cbxIlgi_alanlari.move(50, 100)
        self.cbxIlgi_alanlari.resize(170, 30)
        self.cbxIlgi_alanlari.setStyleSheet("background-color : white")

        self.cbxIlgi_alanlari.addItems(results)
        self.cbxIlgi_alanlari.setVisible(True)

        self.myFont.setPointSize(7)
        self.btnIlgi_alani_ekle = QPushButton(self)
        self.btnIlgi_alani_ekle.setText("İlgi Alanı Ekle")
        self.btnIlgi_alani_ekle.setFont(self.myFont)
        self.btnIlgi_alani_ekle.setFixedSize(100, 40)
        self.btnIlgi_alani_ekle.move(250, 100)
        self.btnIlgi_alani_ekle.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btnIlgi_alani_ekle.clicked.connect(self.ilgi_alani_ekleme)

    def ilgi_alani_ekleme(self):
        ilgi_alani = self.cbxIlgi_alanlari.currentText()
        sicil_no = self.sicil_no
        table = "ilgialanı_hoca"

        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {table} (hoca_sicil_numarası, ilgi_alanı)
            VALUES (%s, %s) """,
            (sicil_no, ilgi_alani),
        )
        cursor.close()


class ListStudent1(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenci Listeleme")
        self.move(600, 300)
        self.setFixedSize(800, 600)

        self.lblTitle = QLabel("Talep oluşturmuş ve onaylanmamış", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        table = "talep_ogrenci"
        cur = conn.cursor()
        query = f"SELECT ogrenci_no, ders_isim FROM {table} WHERE durum =  'beklemede'"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Öğrenci No", "Ders Adı"])
        self.table.setStyleSheet("color : black; background-color : white")

        for row_index, row_data in enumerate(results):
            self.button = QPushButton(self)
            self.button.setText(str(row_data[0]))
            self.button.setFixedSize(125, 40)
            self.button.setStyleSheet(
                "color : black; background-color : white; border-radius: 5px"
            )
            self.button.clicked.connect(self.list_student)
            for col_index, col_data in enumerate(row_data):
                if col_index == 0:
                    self.table.setCellWidget(row_index, col_index, self.button)
                else:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )

    def list_student(self):
        self.listPanel = ListStudent3()
        self.listPanel.show()


class ListStudent2(QWidget):
    def __init__(self, sicil_no):
        super().__init__()
        self.sicil_no = sicil_no
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenci Listeleme")
        self.move(900, 300)
        self.setFixedSize(400, 200)

        self.lblTitle = QLabel("Talep oluşturmuş ve tarafınızca onaylanmış", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)
        
        table = "hoca"
        cur = conn.cursor()
        query = f"SELECT isim, soy_isim FROM {table} WHERE sicil_numarası = {self.sicil_no}"
        cur.execute(query)
        isim = cur.fetchall()
        isim = isim[0]
        
        results = cur.fetchall()
        cur.close()
        
        
        table = "talep_ogrenci"
        cur = conn.cursor()
        query = f"SELECT ogrenci_no, ders_isim FROM {table} WHERE hoca_isim = '{isim[0]}' AND hoca_soy_isim = '{isim[1]}'"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Öğrenci No", "Ders Adı"])
        self.table.setStyleSheet("color : black; background-color : white")

        for row_index, row_data in enumerate(results):
            self.button = QPushButton(self)
            self.button.setText(str(row_data[0]))
            self.button.setFixedSize(125, 40)
            self.button.setStyleSheet(
                "color : black; background-color : white; border-radius: 5px"
            )
            self.ogr_no = row_data[0]
            self.button.clicked.connect(self.list_student)
            for col_index, col_data in enumerate(row_data):
                if col_index == 0:
                    self.table.setCellWidget(row_index, col_index, self.button)
                else:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )

    def list_student(self):
        self.listPanel = ListStudent3(self.ogr_no)
        self.listPanel.show()


class ListStudent3(QWidget):
    def __init__(self, ogrenci_no):
        super().__init__()
        self.ogr_no = ogrenci_no
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenci Listeleme")
        self.move(900, 300)
        self.setFixedSize(400, 200)

        self.lblTitle = QLabel(str(self.ogr_no) + " - aldığı dersler", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        table = "talep_ogrenci"
        cur = conn.cursor()
        query = f"SELECT ders_kodu, hoca_sicil_no FROM {table} WHERE hoca_sicil_no IS NOT NULL"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Öğrenci No", "Ders Kodu"])
        self.table.setStyleSheet("color : black; background-color : white")

        for row_index, row_data in enumerate(results):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(
                    row_index, col_index, QTableWidgetItem(str(col_data))
                )


class Hoca_Mesaj_Gonder(QWidget):
    def __init__(self, sicil_no):
        super().__init__()
        self.sicil_no = sicil_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Öğrenciye mesaj gönder")
        self.move(900, 300)
        self.setFixedSize(600, 400)

        self.lblTitle = QLabel("Öğrenciye Mesaj Gönder", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        self.myFont.setPointSize(9)
        self.txtMesaj = QTextEdit(self)
        self.txtMesaj.move(10, 50)
        self.txtMesaj.resize(580, 200)
        self.txtMesaj.setPlaceholderText("Mesajınızı girin...")
        self.txtMesaj.setStyleSheet("color : black; background-color : white")

        self.txtogr_no = QLineEdit(self)
        self.txtogr_no.move(250, 260)
        self.txtogr_no.resize(100, 30)
        self.txtogr_no.setPlaceholderText("öğrenci no")
        self.txtogr_no.setStyleSheet("color : black; background-color : white")

        self.btnGonder = QPushButton(self)
        self.btnGonder.setText("Mesajı Gönder")
        self.btnGonder.setFont(self.myFont)
        self.btnGonder.setFixedSize(120, 50)
        self.btnGonder.move(230, 330)
        self.btnGonder.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btnGonder.clicked.connect(self.gonder)

        self.myFont.setPointSize(8)
        self.lblMsgResult = QLabel("Mesaj Gönderildi", self)
        self.lblMsgResult.move(230, 310)
        self.lblMsgResult.setFont(self.myFont)
        self.lblMsgResult.setStyleSheet("color : white")
        self.lblMsgResult.setVisible(False)

    def setlblText(self):
        self.txtMesaj.setText("")
        self.txtogr_no.setText("")
        
    def setResultText(self, text):
        self.lblMsgResult.setText(text)

    def gonder(self):
        sicil_no = self.sicil_no
        ogr_no = self.txtogr_no.text()
        mesaj = self.txtMesaj.toPlainText()

        table = "yonetici"
        cur = conn.cursor()
        query = f"SELECT mesajlaşma_karakter_sayısı FROM {table}"
        cur.execute(query)

        karakter = cur.fetchall()
        karakter = karakter[0][0]
        cur.close()

        
        if len(mesaj) <= karakter:
            try:
                self.setlblText()
                
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO mesaj_hoca (sicil_no, ogrenci_no, mesaj)
                    VALUES (%s, %s, %s) """,
                    (sicil_no, ogr_no, mesaj),
                )
                cursor.close()

                self.setResultText("Mesaj Gönder")
                self.lblMsgResult.setVisible(True)

            except:
                self.setResultText("Hata")
                self.lblMsgResult.setVisible(True)

        else:
            self.setResultText(f"Max.: {karakter} - Mesaj: {len(mesaj)}")
            self.lblMsgResult.setVisible(True)
        

class Hoca_Gelen_Mesaj(QWidget):
    def __init__(self, sicil_no):
        super().__init__()
        self.sicil_no = sicil_no

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Gelen Mesajlar")
        self.move(900, 300)
        self.setFixedSize(800, 600)

        self.lblTitle = QLabel("Gelen mesajlar", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        table = "mesaj_ogrenci"
        cur = conn.cursor()
        query = f"SELECT id, mesaj, ogrenci_no FROM {table} WHERE sicil_no = {self.sicil_no}"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

        self.table = QTableWidget(self)
        self.table.move(50, 50)
        self.table.setFixedSize(500, 500)
        self.table.setColumnCount(3)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels(["Id", "Mesaj", "Gönderen öğrenci no"])
        self.table.setStyleSheet("color : black; background-color : white")

        for row_index, row_data in enumerate(results):
            for col_index, col_data in enumerate(row_data):
                if col_index == 2:
                    self.TextEdit = QTextEdit(self)
                    self.TextEdit.setStyleSheet(
                        "color: black; background-color : white"
                    )
                    self.TextEdit.setFixedSize(150, 70)
                    self.TextEdit.setText(str(col_data))
                    self.table.setCellWidget(row_index, col_index, self.TextEdit)
                else:
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data))
                    )
                self.table.setRowHeight(row_index, 70)
                self.table.setColumnWidth(col_index, 150)


class Hoca_Filtreleme(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        self.myFont = QFont("Arial", 8)
        self.myFont.setBold(True)
        self.setWindowTitle("Hoca Filtreleme")
        self.move(700, 300)
        self.setFixedSize(400, 200)

        self.lblTitle = QLabel("Hoca Filtreleme", self)
        self.lblTitle.move(10, 10)
        self.myFont.setPointSize(8)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")
        self.lblTitle.setFixedSize(300, 30)

        table = "ilgialanlari"
        cur = conn.cursor()
        query = f"SELECT ilgi_alanı FROM {table}"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()
        results = [result[0] for result in results]

        self.cbx_filter = QComboBox(self)
        self.cbx_filter.move(20, 70)
        self.cbx_filter.resize(170, 30)
        self.cbx_filter.setStyleSheet("background-color : white")
        self.cbx_filter.addItems(results)
        self.cbx_filter.setVisible(True)

        self.myFont.setPointSize(11)
        self.btn_filter = QPushButton(self)
        self.btn_filter.setText("Filtreye ekle")
        self.btn_filter.setFont(self.myFont)
        self.btn_filter.setFixedSize(150, 40)
        self.btn_filter.move(210, 70)
        self.btn_filter.setStyleSheet(
            "color : black; background-color : white; border-radius: 5px"
        )
        self.btn_filter.clicked.connect(self.filter)

    def filter(self):
        filter_set = set()
        filter_set.add(self.cbx_filter.currentText())
        print(filter_set)
        filter_teacher(filter_set)


# Veritabanı bağlantısı
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="yazlab1",
    host="127.0.0.1",
    port="5432",
)
conn.autocommit = True

# PyQt uygulamasını başlat
app = QApplication(sys.argv)

loginStudentPanel = StudentLoginWindow()
loginTeacherPanel = LoginPanel("Hoca", 600, "Sicil Numarası")
loginAdminPanel = LoginPanel("Admin", 0, "Kullanıcı Adı")


loginStudentPanel.show()
loginTeacherPanel.show()
loginAdminPanel.show()


teacher_panel = TeacherPanel()
admin_panel = AdminPanel()


def filter_teacher(filter_set):
    loginStudentPanel.student_panel.ders_secim_tablo(filter_set)


def login_check(panel, table, txtUserName):
    userName = panel.txtUserName.text()
    password = panel.txtPassword.text()
    results = []
    if table != "yonetici":
        cur = conn.cursor()
        query = f"SELECT isim, soy_isim FROM {table} WHERE {txtUserName} = '{userName}' AND şifre = '{password}'"
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

    return userName, results


def login_teacher():
    username, results = login_check(loginTeacherPanel, "hoca", "sicil_numarası")
    teacher_panel.sicil_no = username

    if results:
        teacher_name = "Hoca Paneli - " + results[0][0] + " " + results[0][1]
    if len(results):
        teacher_panel.setVisible(True)
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
    if results:
        admin_name = "Yönetici Paneli"
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


loginTeacherPanel.btnLogIn.clicked.connect(login_teacher)
loginAdminPanel.btnLogIn.clicked.connect(login_admin)

sys.exit(app.exec_())
