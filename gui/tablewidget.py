# coding: utf8

from gui.error_message import error
import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QInputDialog
from PyQt5.QtCore import Qt, pyqtSlot


class tw(object):
    def __init__(self, tablewidget):
        #tablewidget
        self.tw = tablewidget
        #matrix from tablewidget
        self.data = np.array([],dtype = float)
        #labels
        self.labels = None
        #header or labels (top)
        self.header = self.tw.horizontalHeader()
        #header (left)
        self.hleft = self.tw.verticalHeader()

        ######################## -- some initial and connections
        self.tw.setRowCount(0)
        #automatic resize columns
        self.header.setSectionResizeMode(QHeaderView.Stretch)
        #connect for rename header
        self.header.sectionDoubleClicked.connect(self.renameColumn)
        self.hleft.sectionDoubleClicked.connect(self.renameColumn)


    def renameColumn(self, index):
        text, ok = QInputDialog.getText(self.tw, 'Змінити назву',
            'Введіть нову назву:')
        if text == '':
            return
        else:
            self.tw.setHorizontalHeaderItem(index, QTableWidgetItem(text))
            self.tw.setVerticalHeaderItem(index, QTableWidgetItem(text))
            self.lbl_update()


    def lbl_update(self):
        """
        update labels
        :return:
        """
        l = []
        for i in range(self.cc()):
            s = self.tw.horizontalHeaderItem(i)
            if s is None:
                l.append(str(i))
            else:
                l.append(s.text())
        self.labels = l


    def cc(self):
        return self.tw.columnCount()

    def setCC(self, n):
        try:
            self.tw.setColumnCount(n)
        except Exception as e:
            error(e)

    def delRow(self, n):
        """
        Attention: list should be sorted in reverse direction
        :param n: list, set or number
        :return:
        """
        try:
            if(type(n) == type([]) or type(n) == type(set())):
                for i in n:
                    self.tw.removeRow(i)
                    self.tw.removeColumn(i)
            elif(type(n) == type(0) and n == 0):
                for i in range(self.tw.rowCount(), -1, -1):
                    self.tw.removeRow(i)
            elif(type(n) == type(0)):
                self.tw.removeRow(n)
                self.tw.removeCol(n)
        except Exception as e:
            error(e)

    def setColumnSize(self, column_size):
        try:
            for index in range(self.cc()):
                self.tw.setColumnWidth(index,column_size)
        except Exception as e:
            error(e)

    def table_from_data(self, matrix):
        """
        matrix -> tablewidget (tw)
        :param matrix: type(matrix) = np.array
        :return:
        """
        self.tw.clear()
        self.setCC(0)
        self.delRow(0)
        try:
            n = matrix.shape[0]
            m = matrix.shape[1]
            self.setCC(m)
            self.tw.setRowCount(n)
            self.data = np.array(matrix, dtype = float)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    item = QTableWidgetItem(str(matrix[i,j]))
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.tw.setItem(i, j, item)
        except Exception as e:
            error('insert data in table' + str(e))

    def update_data_from_table(self):
        """
        update data from table
        :return: void
        """
        m = self.tw.columnCount()
        n = self.tw.rowCount()
        self.data = np.zeros(shape = (n, m), dtype = float)
        value = None
        try:
            for i in range(n):
                for j in range(m):
                    item = self.tw.item(i, j)
                    value = np.float64(item.data(0))
                    if not np.isfinite(value):
                        raise ValueError('NaN')
                    self.data[i, j] = value
        except ValueError as v:
            error("update matrix")
        except Exception as e:
            error(e)


