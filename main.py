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
transcript = convert_from_path('input.pdf')

# Her görüntüyü Tesseract ile işle
text = ""
for c in transcript:
    text += pytesseract.image_to_string(c, lang="tur")

print(text)


# Ders başlıklarını ve notları bulmak için düzenli ifadeler
pattern = r'(.+?)(\d+(\.\d+)?)(?:/(\d+(\.\d+)?))?'  # Ders Adı ve Notlar

matches = re.finditer(pattern, text, re.MULTILINE)

for match in matches:
    course_name = match.group(1).strip()
    grade = match.group(2).strip()
    print(f"Ders: {course_name}, Not: {grade}")