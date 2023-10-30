import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog
"""
class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Öğrenci Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)

        # Dersler sekmesi
        self.courses_tab = QWidget()
        self.courses_layout = QVBoxLayout(self.courses_tab)
        self.course_list = QListWidget()
        self.load_courses_button = QPushButton("Transkript Yükle")
        self.load_courses_button.setStyleSheet("color: white;")
        self.load_courses_button.setStyleSheet("background-color: red;")
        self.load_courses_button.clicked.connect(self.open_file_dialog)
        self.courses_layout.addWidget(self.load_courses_button)
        self.courses_layout.addWidget(self.course_list)
        self.central_widget.addTab(self.courses_tab, "Aldığım Dersler")

        # Hocalar sekmesi
        self.professors_tab = QWidget()
        self.professors_layout = QVBoxLayout(self.professors_tab)
        self.professor_list = QListWidget()
        self.load_professors_button = QPushButton("Ders Alabileceğim Hocaları Göster")
        self.professors_layout.addWidget(self.load_professors_button)
        self.professors_layout.addWidget(self.professor_list)
        self.central_widget.addTab(self.professors_tab, "Ders Alabileceğim Hocalar")



    def open_file_dialog(self):
        options = QFileDialog.options()
        options |= QFileDialog.FileMode.ExistingFiles
        file_dialog = QFileDialog.getOpenFileName(self, "PDF Dosyasını Seç", "", "PDF Dosyaları (*.pdf);;Tüm Dosyalar (*)", options=options)
        if file_dialog[0]:
            selected_file = file_dialog[0]
            # transkript işlemleri
            print("Seçilen dosya:", selected_file)
            
            

def main():
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

def dosya_sec():
    dosya_diyalog = QFileDialog()
    dosya_yolu, _ = dosya_diyalog.getOpenFileName()
    if dosya_yolu:
        print(f"Seçilen dosya: {dosya_yolu}")

app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(100, 100, 400, 200)
window.setWindowTitle("Dosya Seçme Örneği")

dosya_sec_dugme = QPushButton("Dosya Seç")
dosya_sec_dugme.clicked.connect(dosya_sec)

window.setCentralWidget(dosya_sec_dugme)
window.show()

sys.exit(app.exec())

"""
import psycopg2

# Veritabanı bağlantısı oluştur
# Veritabanı bağlantısı***************************************
conn = psycopg2.connect(

    database="postgres",
    user="aslinurtopcu",
    password="çilek",
    host="localhost",
    port="5432",
)
conn.autocommit = True
"""
def create_req(ogrenci_no, ders_kodu, hoca_sayisi=1):
    # Öğrencinin talep ettiği dersi ve hoca sayısını kaydet
    sql = "INSERT INTO anlasma (ogrenci_no, ders_kodu, talep_edilebilecek_hoca_sayısı, durum) VALUES (%s, %s, %s, %s)"
    degerler = (ogrenci_no, ders_kodu, hoca_sayisi, 'Beklemede')
    cursor.execute(sql, degerler)
    conn.commit()
    print("Talep başarıyla oluşturuldu")

def delete_req(ogrenci_no, ders_kodu):
    # Öğrencinin talebini geri çek
    sql = "DELETE FROM anlasma WHERE ogrenci_no = %s AND ders_kodu = %s"
    degerler = (ogrenci_no, ders_kodu)
    cursor.execute(sql, degerler)
    conn.commit()
    print("Talep başarıyla geri çekildi")


# Kullanım:
# Talep oluşturma
create_req(1, 101, 2)  # Öğrenci 1, ders kodu 101 için 2 hoca talebinde bulunuyor.

# Talebi geri çekme
delete_req(1, 101)  # Öğrenci 1, ders kodu 101 için talebini geri çekiyor.
"""

# Veritabanı bağlantısını oluştur

cursor = conn.cursor()

def mesaj_gonder(gonderen_id, alici_id, icerik):
    # Mesaj gönderme işlemi
    sql = "INSERT INTO mesajlar (gonderen_id, alici_id, icerik) VALUES (%s, %s, %s)"
    degerler = (gonderen_id, alici_id, icerik)
    cursor.execute(sql, degerler)
    conn.commit()
    print("Mesaj gönderildi")

def mesajlari_getir(kullanici_id):
    # Kullanıcının aldığı veya gönderdiği mesajları getirme işlemi
    sql = "SELECT mesaj_id, gonderen_id, alici_id, icerik, tarih FROM mesajlar WHERE gonderen_id = %s OR alici_id = %s"
    degerler = (kullanici_id, kullanici_id)
    cursor.execute(sql, degerler)
    mesajlar = cursor.fetchall()
    
    if mesajlar:
        for mesaj in mesajlar:
            mesaj_id, gonderen_id, alici_id, icerik, tarih = mesaj
            print(f"Mesaj ID: {mesaj_id}, Gönderen: {gonderen_id}, Alıcı: {alici_id}, İçerik: {icerik}, Tarih: {tarih}")
    else:
        print("Mesajlar bulunamadı")

# Kullanım:
# Mesaj gönderme
#mesaj_gonder(210202103, 210202103, "Merhaba, ders hakkında bir sorum var.")

# Kullanıcının mesajlarını getirme
#mesajlari_getir(210202103)  # Kullanıcı 1'in gönderdiği ve aldığı mesajları getirir.

# Bağlantıyı kapatmayı unutmayın
conn.close()