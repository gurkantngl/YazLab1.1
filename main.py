import psycopg2
import re
from pdf2image import convert_from_path
import pytesseract
from loginPanel import loginPanel
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="yazlab1",
    host="127.0.0.1",
    port="5432"
)
def read_transcript():
    # convert pdf file
    transcript = convert_from_path('transcript.pdf')

    text = ""
    for c in transcript:
        text += pytesseract.image_to_string(c, lang="tur")
        
        
    pattern = r'([A-Z0-9]{6}) \| ([\w\s-]+) \| (\d) \| (\w{2})'

    ders_bilgileri = re.findall(pattern, text)

    lessons = {}
    for ders in ders_bilgileri:
        ders_kodu, ders_adi, akts, harf_notu = ders
        lessons[ders_adi] = {ders_kodu, akts, harf_notu}

    for k,v in lessons.items():
        print(k,v)

# PyQt uygulamasını başlat
app = QApplication(sys.argv)

adminLogin = loginPanel("Yönetici", 10)
teacherLogin = loginPanel("Hoca", 700)
studentLogin = loginPanel("Öğrenci", 1250)


adminLogin.show()
teacherLogin.show()
studentLogin.show()

# PyQt uygulamasını çalıştır
sys.exit(app.exec_())