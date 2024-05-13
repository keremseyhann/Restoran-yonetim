from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from urunliste_ui import Ui_Form
from PyQt5 import QtCore
from veritabani import Veritabani
from restoran import Urun

class UrunListeSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        tablo = self.form.sepettablo

        tablo.setColumnWidth(0, 130)
        tablo.setColumnWidth(1, 70)
        tablo.setColumnWidth(2, 70)

    def goster(self):
        tablo = self.form.sepettablo
        Veritabani.query("SELECT * FROM urunler")
        sql = Veritabani.fetchall()
        urunler = []
        for kayit in sql:
            urunler.append(Urun(*kayit))
        tablo.setRowCount(0)
        tablo.setRowCount(len(urunler))
        self.show()

        if urunler is None:
            return
        
        satir = 0

        for urun in urunler:
            uruncell = QTableWidgetItem(urun.ad)
            miktarcell = QTableWidgetItem(str(urun.miktar))
            fiyatcell = QTableWidgetItem(str(urun.fiyat) + " TL")

            #Hepsinin yazısını ortala
            uruncell.setTextAlignment(QtCore.Qt.AlignCenter)
            miktarcell.setTextAlignment(QtCore.Qt.AlignCenter)
            fiyatcell.setTextAlignment(QtCore.Qt.AlignCenter)

            tablo.setItem(satir, 0, uruncell)
            tablo.setItem(satir, 1, miktarcell)
            tablo.setItem(satir, 2, fiyatcell)
            satir+=1