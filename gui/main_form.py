# coding: utf8


from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap, QImage

from graphviz import Digraph

import os.path

form_class, base_class = loadUiType(os.path.join(os.path.dirname(__file__), 'main_form.ui'))


class MainWindow(QDialog):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.ui = form_class()
        self.ui.setupUi(self)
        self.graph = Digraph(comment='Когнитивная карта', name='Cognitive map', format='png')
        self.labels = None
        self.matrix = None

    def load_labels(self, path):
        pass

    def load_matrix(self, path):
        pass

    @pyqtSlot(int)
    def pageChanged(self, page):
        if page == 1:
            self.render_graph()

    def render_graph(self):
        if not self.matrix:
            return
        self.graph.node('A', 'King Arthur', color='blue')
        img = QImage.fromData(self.graph.pipe(), "png")
        self.ui.graphLabel.setPixmap(QPixmap.fromImage(img))