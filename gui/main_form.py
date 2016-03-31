# coding: utf8


from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QAction, QErrorMessage, QTableWidgetItem
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap, QImage

from graphviz import Digraph
from csv import reader

import os.path
import numpy as np
from gui.read_data import read_data
from gui.error_message import error
from gui.tablewidget import tw
from openpyxl import Workbook
from logic.math import *

form_class, base_class = loadUiType(os.path.join(os.path.dirname(__file__), 'main_form.ui'))


class MainWindow(QDialog):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)


        self.ui = form_class()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)

        self.graph = Digraph(comment='Когнитивная карта', name='Cognitive map', format='png')
        self.labels = None
        self.matrix = None

        #set tableWidget
        self.tw = tw(self.ui.tw)
        #self.tw.verticalHeader().hide()
        #self.tw.setRowCount(0)
        #self.column_size = 50
        # for index, size in enumerate(column_size):
        #      self.ui.tw.setColumnWidth(index,size)
        # return

    @pyqtSlot()
    def saveImage(self): 
        """
        save image as png
        :return:
        """
        name = QFileDialog.getSaveFileName(self, "Save as", "", "PNG(*.png)")[0]
        if name != "":
            try:
                self.graph.render(name, cleanup=True)
                error("Збережено", 1, False)
            except Exception as e:
                error("Помилка збереження. " + str(e))
            #self.ui.graphView.grab().save(name)


    @pyqtSlot(int)
    def pageChanged(self, page):
        if page == 1: # Graph page
            try:
                if self.tw.data.shape[0] == 0:
                    self.ui.tabWidget.setCurrentIndex(0)
                    error("add data to sheet")
                    return
                self.render_graph()
            except Exception as e:
                self.ui.tabWidget.setCurrentIndex(0)
                error("while building graph; "+str(e))
            try:
                self.calc()
            except Exception as e:
                error(e)

    def calc(self):
        """
        calculate math operations
        :return:
        """
        eig = eigenvalues(self.tw.data)
        maxeig = round(np.max(np.abs(eig)), 3)
        self.ui.lambda_max.setText(str(maxeig))
        if maxeig < 1:
            self.ui.stable_value.setChecked(True)
        else:
            self.ui.stable_value.setChecked(False)
        if maxeig <=1:
            self.ui.stable_disturbance.setChecked(True)
        else:
            self.ui.stable_disturbance.setChecked(False)



    def render_graph(self):
        """
        build graph from data and labels
        :return:
        """
        if self.tw.data.shape[0] == 0 or self.tw.data.shape[0] != self.tw.data.shape[1]:
            return
        self.graph = Digraph(comment='Когнитивна карта', name='Cognitive map', format='png')
        for i, label in enumerate(self.tw.labels):
            self.graph.node(str(i), label, color='blue')
        size = len(self.tw.labels)
        for i in range(size):
            for j in range(size):
                weight = self.tw.data[i, j]
                if weight != 0:
                    self.graph.edge(str(i), str(j), label=str(weight),
                                    color='green' if weight > 0 else 'red')
        graph = QImage.fromData(self.graph.pipe(), "png")
        self.ui.graphView.setPixmap(QPixmap.fromImage(graph))

    @pyqtSlot()
    def import_sheet(self):
        """
        import data to tablewidet from file
        :return:
        """
        try:
            name = QFileDialog.getOpenFileName(self, "Open file", "", "Microsoft Excel(*.xlsx *.xls)")[0]
            if name == '':
                return
            labels, matrix= read_data(name)
            matrix = np.array(matrix)
            if len(matrix) == 0 or len(matrix) != len(matrix[0]):
                raise Exception('Reformat matrix in file')
            self.tw.table_from_data(np.nan_to_num(matrix))
            self.tw.tw.setHorizontalHeaderLabels(labels)
            self.tw.tw.setVerticalHeaderLabels(labels)
            self.tw.lbl_update()
        except Exception as e:
            error(e)

    def twitem(self, s):
        item = QTableWidgetItem(str(s))
        item.setTextAlignment(Qt.AlignHCenter)
        return item

    @pyqtSlot()
    def addFactor(self):
        """
        add Factor or row and column to tablewidget
        :return:
        """
        try:
            n = len(self.tw.data)
            matrix = np.zeros(shape = (n+1, n+1), dtype = float)
            matrix[:n, :n] = self.tw.data
            self.tw.data = matrix
            self.tw.tw.insertRow(n)
            self.tw.tw.insertColumn(n)
            for i in range(0, n):
                self.tw.tw.setItem(n, i, self.twitem('0.0'))
                self.tw.tw.setItem(i, n, self.twitem('0.0'))
            self.tw.tw.setItem(n, n, self.twitem('0.0'))
            self.tw.lbl_update()
        except Exception as e:
            error(e)

    @pyqtSlot(QTableWidgetItem)
    def tableItemChanged(self, item):
        i = item.row()
        j = item.column()
        if str(self.tw.data[i,j]) == item.data(0): #nothing change
            return
        value = None
        try:
            value = np.float64(item.data(0))
            if not np.isfinite(value):
                raise ValueError('NaN')
            self.tw.data[i,j] = value
        except ValueError:
            return
        finally:
        #     if self.tw.data[i,j] == np.nan:
        #         self.tw.data[i,j] = 0.0
            item.setData(0, str(self.tw.data[i, j]))


    def keyPressEvent(self, e):
        """
        delete selected rows and columns
        :param e: event
        :return:
        """
        a = e.nativeScanCode()
        if a == 339 or 14:
            indexrow = self.tw.tw.selectionModel().selectedRows()
            indexcol = self.tw.tw.selectionModel().selectedColumns()
            indexes = sorted(set(index.row() for index in indexrow).union(\
                index.column() for index in indexcol), reverse = True)
            #error(indexes)
            if indexes == []:
                return
            else:
                self.tw.delRow(indexes)
                self.tw.update_data_from_table()
                self.tw.lbl_update()


    @pyqtSlot()
    def saveTable(self):
        """
        save data from talbe to file
        :return:
        """
        self.tw.update_data_from_table()
        if len(self.tw.data) == 0:
            error("Неможливо зберегти.Таблиця порожня.",2)
            return
        self.tw.lbl_update()
        name = QFileDialog.getSaveFileName(self, "Save as", "", "Microsoft Excel(*.xlsx *.xls)")[0]
        if name == "":
            return
        wb = Workbook()
        #get active worksheet
        ws = wb.active
        ws.append(self.tw.labels)
        for i in range(len(self.tw.data)):
            ws.append(self.tw.data[i].tolist())
        wb.save(name)
        error("Збережено", 1, False)

    @pyqtSlot(bool)
    def checkBoxClicked(self, state):
        """
        keep state after click checkBox
        :param state: true is checkbox is checked, else - false
        :return:
        """
        checkBox = self.sender()
        checkBox.setChecked(not state)