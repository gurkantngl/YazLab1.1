import sys
import psycopg2
from psycopg2 import Error

# Veritabanı bağlantısı
hostname = "127.0.0.1"
database = "postgres"
username = "postgres"
password = "yazlab1"
port = "5432"

class DB:
    def __init__(self):
        self.connection : psycopg2.connection
    
    #bağlantı açma fonksiyonu
    def DBconnect(self):
        try:
            self.connection = psycopg2.connect(database = database,
                                               user = username,
                                               password = password,
                                               host = hostname,
                                               port = port
                                               )
            self.connection.autocommit = True
        
        except(Exception, Error) as error:
            print("PostgreSQL bağlanırken hata oluştu: ",error)
        
        print("Database bağlandı")
        return self.connection
    
    # bağlantı kapama fonksiyonu
    def closeDBconnect(self):
        try:
            self.connection.close()
        
        except (Exception, Error) as error:
            print("PostgreSQL bağlantısı kapanmadı",error)
        
        print("PostgreSQL bağlantısı kapandı")
        
    def Query(self, query:str, *info):
        try:
            self.connection=self.DBconnect(self)
            cursor = self.connection.cursor()
            cursor.execute(query, info)
        
        except (Exception, Error) as error:
            print("sorgu hatası",error)
            
        try:
            record=cursor.fetchall()
        except (Exception, Error) as error:
            record=self.connection.commit()
        self.closeDBconnect(self)
        
        return record
        