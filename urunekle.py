from PyQt5.QtWidgets import QWidget, QMessageBox
from urunekle_ui import Ui_Form
from restoran import Urun
from PyQt5.QtCore import pyqtSignal

class UrunEkleSayfa(QWidget):
    urun_ekle_sinyal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.form.ekleButon.clicked.connect(self.urunekle)

    def urunekle(self):
        urunisim = self.form.urunline.text()
        miktar = self.form.miktarBox.value()
        fiyat = self.form.fiyatbox.value()

        yanit = QMessageBox.warning(self,"Ürün Ekle","Ürün eklemek istediğine emin misin?",QMessageBox.Yes,QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        Urun.urunekle(urunisim, miktar, fiyat, "topluyemek.jpg")
        self.urun_ekle_sinyal.emit()

        yanit = QMessageBox.information(self, "Ürün Ekle", "Ürün ekleme işlemi tamamlandı", QMessageBox.Ok)
        self.close()