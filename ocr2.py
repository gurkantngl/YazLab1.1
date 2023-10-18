import fitz
import re

pdf_file = "transcript.pdf"  # Okumak istediğiniz PDF dosyasının adını belirtin

doc = fitz.open(pdf_file)

text = ""
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    text += page.get_text()

#print(text)

lines = text.split('\n')
# Üç büyük harf ve üç rakam ile başlayan satırları ayıklayalım
ders_kodlari = re.findall(r"^[A-Z]{3}\d{3}$", text, re.MULTILINE)

lessons = []


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

# Ders bilgilerini yazdıralım
for lesson in lessons:
    print("Ders Kodu:", lesson["ders_kodu"])
    print("Ders Adı:", lesson["ders_adi"])
    print("Ders Statüsü:", lesson["ders_statusu"])
    print("Öğretim Dili:", lesson["ogretim_dili"])
    print("AKTS:", lesson["AKTS"])
    print("Not:", lesson["not"])
    print()
