from PyQt5.QtWidgets import QWidget, QMessageBox
from stokguncelle_ui import Ui_Form
from restoran import Urun
from PyQt5.QtCore import pyqtSignal
from veritabani import Veritabani

class StokGuncelleSayfa(QWidget):
    stok_guncelle_sinyal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.form.guncelleButon.clicked.connect(self.guncelle)
        self.form.urunBox.currentIndexChanged.connect(self.miktarguncelle)

    def goster(self):
        Veritabani.query("SELECT * FROM urunler")
        sql = Veritabani.fetchall()
        urunler = []
        for kayit in sql:
            urunler.append(Urun(*kayit))
        self.urunler = urunler
        self.form.urunBox.clear()

        for urun in urunler:
            self.form.urunBox.addItem(urun.ad, urun.id)
        self.show()

    def miktarguncelle(self):
        index = self.form.urunBox.currentIndex()
        urun = self.urunler[index]

        self.form.miktarBox.setValue(urun.miktar)

    def guncelle(self):
        index = self.form.urunBox.currentIndex()
        urun = self.urunler[index]

        yanit = QMessageBox.warning(self,"Stok Güncelle","Stok miktarını güncellemek istediğine emin misin?",QMessageBox.Yes,QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        yenimiktar = self.form.miktarBox.value()
        
        urun.stokguncelle(yenimiktar)
        self.stok_guncelle_sinyal.emit()

        yanit = QMessageBox.information(self, "Stok Güncelle", "Stok güncelleme işlemi tamamlandı", QMessageBox.Ok)