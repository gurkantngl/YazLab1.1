CREATE TABLE ogrenci (
    ogrenci_no SERIAL PRIMARY KEY,
    ad varchar(255),
    soyad varchar(255),
    tc_kimlik_no varchar(11) UNIQUE,
    e_posta varchar(255),
    sifre varchar(255),
    anlasmaTalepSayisi integer,
    anlaşmaDurumu varchar(50)
);


CREATE TABLE akademisyen (
    sicil_no SERIAL PRIMARY KEY,
    ad varchar(255),
    soyad varchar(255),
    tc_kimlik_no varchar(11) UNIQUE,
    e_posta varchar(255),
    sifre varchar(255),
    ilgiAlanlari varchar(255),
    kontenjanBilgisi integer,
    acilanDersler varchar(255),
    kriterDersler varchar(255)


);


CREATE TABLE dersler (
    ders_kodu SERIAL PRIMARY KEY,
    ders_adi varchar(255) UNIQUE,
    ders_durumu varchar(255),
    ogretim_dili varchar(255),
    ders_notu numeric(4, 0)

);

CREATE TABLE donemler (
    donem_id SERIAL PRIMARY KEY,
    ders_donemi varchar(255) UNIQUE
);

CREATE TABLE transkript (
    transkript_id SERIAL PRIMARY KEY,
    ogrenci_no INT REFERENCES ogrenci(ogrenci_no),
    ders_adi varchar REFERENCES dersler(ders_adi),
    ders_tarihi date,
    ders_donemi varchar(255)
);

CREATE TABLE anlasma (
    anlasma_id SERIAL PRIMARY KEY,
    ogrenci_no INT REFERENCES ogrenci(ogrenci_no),
    sicil_no INT REFERENCES akademisyen(sicil_no),
    durum varchar(255) DEFAULT 'Talepte Bulunmadı'
);

SELECT * FROM ogrenci;
DROP table dersler;
DROP table transkript;

SELECT * from dersler
SELECT * FROM transkript