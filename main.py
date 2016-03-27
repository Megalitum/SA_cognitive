#coding: utf8
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType

app = QApplication(sys.argv)
app.setApplicationName('Когнитивный анализ')
form_class, base_class = loadUiType('main_form.ui')


class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        self.setupUi(self)
        import Graphviz
        self.graphLabel.setPixmap(QPixmap.fromImage(Graphviz.img))


#-----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('Лабораторная работа №7')
form.show()
sys.exit(app.exec_())