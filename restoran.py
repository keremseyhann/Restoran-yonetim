from veritabani import Veritabani
from datetime import datetime

class Urun:
    def __init__(self,ID, ad, Miktar, Fiyat, fotograf):
        self.id = ID
        self.ad = ad
        self.miktar = Miktar
        self.fiyat = Fiyat
        self.fotograf = fotograf

    def stokguncelle(self, miktar):
        Veritabani.query('update urunler set miktar=? where id=?',(miktar,self.id))

    @staticmethod
    def hareketekle(stokid, kullaniciid, eylem):
        Veritabani.query('insert into hareketler(stokid,kullaniciid,eylem,tarih) values(?,?,?,?)',(stokid, kullaniciid, eylem, datetime.now()))

    def fiyatguncelle(self,fiyat,KullaniciID):
        Veritabani.query('update stok set fiyat=? where id=?',(fiyat,self.id))
        self.hareketekle(self.id, KullaniciID, "Fiyat Güncelleme")

    @staticmethod
    def urunekle(ad, miktar, fiyat, fotograf):
        Veritabani.query('insert into urunler (ad, miktar, fiyat, fotograf) values(?,?,?,?)', (ad, miktar, fiyat, fotograf))


class Siparis:
    def __init__(self,id,kullaniciid,ToplamFiyat,tarih,durum):
        self.id = id
        self.toplamfiyat = ToplamFiyat
        self.tarih = tarih
        self.durum = durum

        Veritabani.query('SELECT * FROM kullanicilar WHERE id = ?', (kullaniciid,))
        uyesql = Veritabani.fetchone()
        self.musteri = Kullanici(*uyesql)

    @staticmethod
    def siparisekle(kullaniciid, urunler):
        tarih = datetime.now()
        fiyat = 0

        for urun in urunler:
            Veritabani.query('UPDATE urunler SET miktar = miktar - ? WHERE id = ?', (urun["miktar"], urun["urun"].id))
            fiyat += urun["urun"].fiyat * urun["miktar"]

        Veritabani.query('insert into siparisler(kullaniciid, ToplamFiyat, Tarih, durum) values(?,?,?,?)', (kullaniciid,fiyat, tarih, 'Yeni Sipariş'))
        Veritabani.query('SELECT last_insert_rowid()')
        siparisid = Veritabani.fetchone()[0]

        for urun in urunler:
            Veritabani.query('INSERT INTO siparisurunler (siparisid, urunid, miktar) values (?, ?, ?)', (siparisid, urun["urun"].id, urun["miktar"]))

    def durumguncelle(self, yenidurum):
        Veritabani.query('update siparisler set durum=? where id=?',(yenidurum, self.id))


class Kullanici:
    def __init__(self,id,kullaniciadi, sifre, ad, soyad, telefon):
        self.id = id
        self.kullaniciadi = kullaniciadi
        self.sifre = sifre
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon

    @staticmethod
    def kayitol(kullaniciadi, sifre, ad, soyad, telefon):
        Veritabani.query('INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES(?, ?, ?, ?, ?)', (kullaniciadi, sifre, ad, soyad, telefon))
    
