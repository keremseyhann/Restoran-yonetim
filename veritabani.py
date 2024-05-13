import sqlite3

class veritabani:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='siparisler'")
        tablo_var_mi = self.cursor.fetchone()

        if not tablo_var_mi:  # Tablo yok
            self.cursor.execute('CREATE TABLE IF NOT EXISTS urunler (ID INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, miktar INTEGER, fiyat INTEGER, fotograf TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS kullanicilar (ID INTEGER PRIMARY KEY AUTOINCREMENT, kullaniciadi TEXT, sifre TEXT, ad TEXT, soyad TEXT, telefon TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS siparisler (ID INTEGER PRIMARY KEY AUTOINCREMENT, kullaniciid INTEGER, ToplamFiyat INTEGER, Tarih TIMESTAMP, durum TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS siparisurunler (ID INTEGER PRIMARY KEY AUTOINCREMENT, siparisid INTEGER, urunid INTEGER, miktar INTEGER)')

            self.cursor.execute('''INSERT INTO urunler (ad, miktar, fiyat, fotograf) VALUES 
                ('Adana Kebap', 15, 300, 'adana.jpg'),
                ('Fıstıklı Baklava', 10, 100, 'baklava.jpg'),
                ('Lahmacun', 20, 250, 'lahmacun.jpg'),
                ('Et Tantuni', 10, 300, 'tantuni.jpg'),
                ('Mantarlı Pizza', 15, 150, 'mantar.jpg')
                ''')
            
            self.cursor.execute("INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES ('enes', '123', 'Enes', 'Biçici', '5323184256')")
            self.connection.commit()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
Veritabani = veritabani('sql.db')
