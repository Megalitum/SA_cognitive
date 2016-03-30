from PyQt5.QtWidgets import  QErrorMessage, QMessageBox

def error(e, type_icon = 2, err = True):
    """
    show MessageBox
    :param e: string(error)
    :param type_icon: type_icon
    :param err: need "error" in message
    :return:
    """
    error = QMessageBox()
    if err:
        error.setText(str("error:"+ "{}".format(e)))
    else:
        error.setText(str("{}".format(e)))
    error.icon = type_icon
    error.exec_()

    # error = QErrorMessage()
    # error.showMessage(str("error:"+ "{}".format(e)))
    # error.exec_()