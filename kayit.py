from PyQt5.QtWidgets import QWidget, QMessageBox
from kayit_ui import Ui_Form
from restoran import Kullanici

class KayitSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.anasayfa = Ui_Form()
        self.anasayfa.setupUi(self)
        self.anasayfa.kayitButon.clicked.connect(self.kayitol)

    def kayitol(self):
        kullaniciadi = self.anasayfa.kullaniciadiLabel.text()
        sifre = self.anasayfa.sifreLabel.text()
        telefon = self.anasayfa.telefonLabel.text()
        soyad = self.anasayfa.soyadLine.text()
        ad = self.anasayfa.adLine.text()

        Kullanici.kayitol(kullaniciadi, sifre, ad, soyad, telefon)

        yanit = QMessageBox.information(self, "Kayıt", "Kayıt işlemi tamamlandı.",QMessageBox.Ok)

        self.close()
