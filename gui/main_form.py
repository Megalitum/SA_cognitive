# coding: utf8

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType
import os.path

form_class, base_class = loadUiType(os.path.join(os.path.dirname(__file__), 'main_form.ui'))


class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        self.setupUi(self)
        import Graphviz
        self.graphLabel.setPixmap(QPixmap.fromImage(Graphviz.img))