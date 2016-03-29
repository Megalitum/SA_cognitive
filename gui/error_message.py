from PyQt5.QtWidgets import  QErrorMessage

def error(e):
    error = QErrorMessage()
    error.showMessage(str("error:"+ "{}".format(e)))
    error.exec_()