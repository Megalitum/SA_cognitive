# coding: utf8
import sys

from PyQt5.QtWidgets import QApplication
from gui.main_form import MainWindow


app = QApplication(sys.argv)
app.setApplicationName('Когнитивный анализ')


#-----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('Лабораторная работа №7')
form.load_matrix('data/test_huge.npy')
form.load_labels('data/labels_huge.csv')
form.show()
sys.exit(app.exec_())