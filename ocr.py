from pdf2image import convert_from_path
import pytesseract

# PDF dosyasını görüntülere dönüştür
images = convert_from_path('input.pdf')

# Her görüntüyü Tesseract ile işle
text = ""
for image in images:
    text += pytesseract.image_to_string(image, lang="tur")

print(text)