from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from siparisler_ui import Ui_Form
from PyQt5 import QtCore
from veritabani import Veritabani
from restoran import Siparis, Urun

class SiparislerSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        siparislertablo = self.form.siparislertablo

        siparislertablo.setColumnWidth(0, 60)
        siparislertablo.setColumnWidth(1, 100)
        siparislertablo.setColumnWidth(2, 100)
        siparislertablo.setColumnWidth(3, 80)
        siparislertablo.setColumnWidth(4, 80)

        sepettablo = self.form.urunlertablo
        sepettablo.setColumnWidth(0, 140)
        sepettablo.setColumnWidth(1, 60)

        siparislertablo.currentCellChanged.connect(self.urunlisteguncelle)
        self.form.guncelleButon.clicked.connect(self.guncelle)


    def goster(self):
        siparislertablo = self.form.siparislertablo
        Veritabani.query("SELECT id,kullaniciid,toplamfiyat, strftime('%d.%m.%Y %H:%M', tarih) AS tarih, durum FROM siparisler")
        sql = Veritabani.fetchall()
        siparisler = []
        for kayit in sql:
            siparisler.append(Siparis(*kayit))
        self.siparisler = siparisler
        siparislertablo.setRowCount(0)
        siparislertablo.setRowCount(len(siparisler))
        self.show()

        if siparisler is None:
            return
        
        satir = 0

        for siparis in siparisler:
            nocell = QTableWidgetItem(str(siparis.id))
            mustericell = QTableWidgetItem(siparis.musteri.ad + " " + siparis.musteri.soyad)
            tarihcell = QTableWidgetItem(siparis.tarih)
            fiyatcell = QTableWidgetItem(str(siparis.toplamfiyat) + " TL")
            durumcell = QTableWidgetItem(siparis.durum)

            #Hepsinin yazısını ortala
            nocell.setTextAlignment(QtCore.Qt.AlignCenter)
            mustericell.setTextAlignment(QtCore.Qt.AlignCenter)
            tarihcell.setTextAlignment(QtCore.Qt.AlignCenter)
            durumcell.setTextAlignment(QtCore.Qt.AlignCenter)
            fiyatcell.setTextAlignment(QtCore.Qt.AlignCenter)

            siparislertablo.setItem(satir, 0, nocell)
            siparislertablo.setItem(satir, 1, mustericell)
            siparislertablo.setItem(satir, 2, tarihcell)
            siparislertablo.setItem(satir, 3, fiyatcell)
            siparislertablo.setItem(satir, 4, durumcell)
            satir+=1

    def urunlisteguncelle(self):
        siparislertablo = self.form.siparislertablo
        sepettablo = self.form.urunlertablo

        siparisindex = siparislertablo.currentRow()
        sepettablo.setRowCount(0)
        if siparisindex < 0:
            return
        siparis = self.siparisler[siparisindex]

        Veritabani.query("SELECT urunid, miktar FROM siparisurunler WHERE siparisid = ?", (siparis.id,))
        sql = Veritabani.fetchall()
        sepettablo.setRowCount(len(sql))

        satir = 0

        for urunsql in sql:
            Veritabani.query("SELECT ad FROM urunler WHERE id = ?", (urunsql[0],))
            urunad = Veritabani.fetchone()[0]
            uruncell = QTableWidgetItem(urunad)
            miktarcell = QTableWidgetItem(str(urunsql[1]))

            #Hepsinin yazısını ortala
            uruncell.setTextAlignment(QtCore.Qt.AlignCenter)
            miktarcell.setTextAlignment(QtCore.Qt.AlignCenter)

            sepettablo.setItem(satir, 0, uruncell)
            sepettablo.setItem(satir, 1, miktarcell)
            satir+=1

    def guncelle(self):
        siparislertablo = self.form.siparislertablo
        siparisindex = siparislertablo.currentRow()
        siparis = self.siparisler[siparisindex]

        yanit = QMessageBox.warning(self,"Sipariş","Durumu güncellemek istediğinize emin misiniz?",QMessageBox.Yes,QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        yenidurum = self.form.durumBox.currentText()
        
        siparis.durumguncelle(yenidurum)

        durumcell = QTableWidgetItem(yenidurum)
        durumcell.setTextAlignment(QtCore.Qt.AlignCenter)
        siparislertablo.setItem(siparisindex, 4, durumcell)

        yanit = QMessageBox.information(self, "Ürün Ekle", "Durum güncelleme işlemi tamamlandı", QMessageBox.Ok)
