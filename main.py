import psycopg2
import re
from pdf2image import convert_from_path
import pytesseract

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="yazlab1",
    host="127.0.0.1",
    port="5432"
)

# PDF dosyasını görüntülere dönüştür
transcript = convert_from_path('transcript.pdf')

# Her görüntüyü Tesseract ile işle
text = ""
for c in transcript:
    text += pytesseract.image_to_string(c, lang="tur")

#print(text)


"""# Ders başlıklarını ve notları bulmak için düzenli ifadeler
pattern = r'(.+?)(\d+(\.\d+)?)(?:/(\d+(\.\d+)?))?'  # Ders Adı ve Notlar

matches = re.finditer(pattern, text, re.MULTILINE)

for match in matches:
    course_name = match.group(1).strip()
    grade = match.group(2).strip()
    print(f"Ders: {course_name}, Not: {grade}")"""
    
    
# Ders bilgilerini ayıklamak için düzenli ifade
pattern = r'([A-Z0-9]{6}) \| ([\w\s-]+) \| (\d) \| (\w{2})'

# Metindeki tüm ders bilgilerini bul
ders_bilgileri = re.findall(pattern, text)

for ders in ders_bilgileri:
    ders_kodu, ders_adi, akts, harf_notu = ders
    print(f"Ders Kodu: {ders_kodu.strip()}")
    print(f"Ders Adı: {ders_adi.strip()}")
    print(f"AKTS: {akts.strip()}")
    print(f"Harf Notu: {harf_notu.strip()}")
    print()