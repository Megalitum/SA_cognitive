from gui.error_message import error
import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt


class tw(object):
    def __init__(self, tablewidget):
        self.tw = tablewidget
        #self.tw.verticalHeader().hide()
        self.tw.setRowCount(0)
        self.data = np.array([])

    def cc(self):
        return self.tw.columnCount()

    def setCC(self, n):
        try:
            self.tw.setColumnCount(n)
        except Exception as e:
            error(e)

    def setColumnSize(self, column_size):
        try:
            for index in range(self.cc()):
                self.tw.setColumnWidth(index,column_size)
        except Exception as e:
            error(e)

    def update_data(self):
        self.tw.clear()
        self.setCC(len(self.data))
        try:
            for i, j in enumerate(self.data):
                self.insert_string(i, j)
        except Exception as e:
            error(e)

    def insert_string(self, row, data):
        try:
            assert len(data) == self.cc()
            self.tw.insertRow(row)
            for j, d in enumerate(data):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignHCenter)
                self.tw.setItem(row, j, item)
        except Exception as e:
            raise ('insert data in table' + str(e))

