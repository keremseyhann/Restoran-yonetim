from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from ana_ui import Ui_MainWindow
from PyQt5 import QtGui, QtCore
from veritabani import Veritabani
from restoran import *
from urunliste import UrunListeSayfa
from urunekle import UrunEkleSayfa
from siparisler import SiparislerSayfa
from stokguncelle import StokGuncelleSayfa

class AnaSayfa(QMainWindow):
    def __init__(self, uye) -> None:
        super().__init__()
        self.uye = uye
        self.anasayfa = Ui_MainWindow()
        self.anasayfa.setupUi(self)
        self.index = 0
        self.sepet = []
        self.anasayfa.sonrakiButon.clicked.connect(self.sonraki)
        self.anasayfa.oncekiButon.clicked.connect(self.onceki)
        self.anasayfa.kaydetButon.clicked.connect(self.sepeteeklecikar)
        self.listeguncelle()
        self.urunguncelle()
        self.anasayfa.miktarBox.valueChanged.connect(self.fiyatguncelle)
        self.anasayfa.sepettablo.setColumnWidth(0, 140)
        self.anasayfa.sepettablo.setColumnWidth(1, 60)
        self.anasayfa.siparisButon.clicked.connect(self.siparisolustur)
        urunlistesayfa = UrunListeSayfa()
        self.anasayfa.urunliste.triggered.connect(lambda: urunlistesayfa.goster())
        self.toplamfiyatguncelle()
        uruneklesayfa = UrunEkleSayfa()
        self.anasayfa.urunekle.triggered.connect(lambda: uruneklesayfa.show())
        uruneklesayfa.urun_ekle_sinyal.connect(self.listeguncelle)
        siparisayfa = SiparislerSayfa()
        self.anasayfa.siparisliste.triggered.connect(lambda: siparisayfa.goster())
        stokguncellesayfa = StokGuncelleSayfa()
        self.anasayfa.stokGuncelle.triggered.connect(lambda: stokguncellesayfa.goster())
        stokguncellesayfa.stok_guncelle_sinyal.connect(self.sepetbosalt)


    def sonraki(self):
        self.index += 1
        if len(self.urunler) == self.index:
            self.index = 0
        self.urunguncelle()

    def onceki(self):
        self.index -= 1
        if self.index == -1:
            self.index = len(self.urunler)-1
        self.urunguncelle()

    def urungoster(self, yeni_indeks):
        self.index = yeni_indeks
        self.urunguncelle()

    def urunguncelle(self):
        urun = self.urunler[self.index]
        
        self.anasayfa.fotograf.setPixmap(QtGui.QPixmap("fotograflar/" + urun.fotograf))
        self.anasayfa.label.setText(urun.ad)
        self.anasayfa.miktarBox.setValue(1)
        self.anasayfa.miktarBox.setMaximum(urun.miktar)
        self.anasayfa.fiyatLabel.setText(str(urun.fiyat) + " TL")

        if urun.miktar < 1:
            self.anasayfa.kaydetButon.setEnabled(False)
        else:
            self.anasayfa.kaydetButon.setEnabled(True)

        sepetteki = next((urunn for urunn in self.sepet if urunn["urun"].ad == urun.ad), None)

        if sepetteki is None:
            self.anasayfa.kaydetButon.setText("Sepete Ekle")
        else:
            self.anasayfa.kaydetButon.setText("Sepetten Çıkar")


    def kaydet(self):
        yanit = QMessageBox.warning(self,"urun","Kaydetmek istediğinize emin misiniz?",QMessageBox.Yes,QMessageBox.No)
        if yanit == QMessageBox.No :
            return
        
    def sepetbosalt(self):
        self.listeguncelle()
        self.urunguncelle()
        self.anasayfa.sepettablo.setRowCount(0)
        self.sepet = []

        
    def siparisolustur(self):
        if len(self.sepet) < 1:
            QMessageBox.warning(self, "Sipariş", "Sepetiniz boş.", QMessageBox.Ok)
            return
        
        yanit = QMessageBox.warning(self,"Sipariş","Sipariş oluşturmak istediğinize emin misiniz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        Siparis.siparisekle(self.uye.id, self.sepet)
        self.sepet = []
        self.listeguncelle()
        self.urunguncelle()
        self.toplamfiyatguncelle()
        self.anasayfa.sepettablo.setRowCount(0)
        
    def sepeteeklecikar(self):
        urun = self.urunler[self.index]
        miktar = self.anasayfa.miktarBox.value()
        buton = self.anasayfa.kaydetButon
        tablo = self.anasayfa.sepettablo

        if buton.text() == "Sepete Ekle":
            buton.setText("Sepetten Çıkar")

            uruncell = QTableWidgetItem(urun.ad)
            miktarcell = QTableWidgetItem(str(miktar))
            uruncell.setTextAlignment(QtCore.Qt.AlignCenter)
            miktarcell.setTextAlignment(QtCore.Qt.AlignCenter)

            satir = len(self.sepet)
            tablo.setRowCount(satir+1)
            tablo.setItem(satir, 0, uruncell)
            tablo.setItem(satir, 1, miktarcell)
            self.sepet.append({"urun": urun, "miktar": miktar})
            self.toplamfiyatguncelle()

        else:
            index = next((i for i, urunn in enumerate(self.sepet) if urunn["urun"].ad == urun.ad), None)
            del self.sepet[index]
            tablo.removeRow(index)
            buton.setText("Sepete Ekle")

    def toplamfiyatguncelle(self):
        if len(self.sepet) < 1:
            self.anasayfa.toplamfiyat.setText("0 TL")
            return
        
        toplamfiyat = 0
        for urun in self.sepet:
            toplamfiyat += urun["urun"].fiyat * urun["miktar"]

        self.anasayfa.toplamfiyat.setText(str(toplamfiyat) + " TL")

    def listeguncelle(self):
        Veritabani.query("SELECT * FROM urunler")
        sql = Veritabani.fetchall()
        urun = []
        for kayit in sql:
            urun.append(Urun(*kayit))
        self.urunler = urun

    def fiyatguncelle(self):
        urun = self.urunler[self.index]
        miktar = self.anasayfa.miktarBox.value()
        toplamfiyat = urun.fiyat * miktar
        self.anasayfa.fiyatLabel.setText(str(toplamfiyat) + " TL")


    def urunsil(self, index):
        if self.index == index:
            self.index = index-1
        self.guncelle()

    def guncelle(self):
        self.listeguncelle()
        self.urunguncelle()
