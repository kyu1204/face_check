# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'face.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(713, 618)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 541, 621))
        self.graphicsView.setObjectName("graphicsView")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(540, 110, 181, 171))
        self.listView.setObjectName("listView")
        self.listView_2 = QtWidgets.QListView(Form)
        self.listView_2.setGeometry(QtCore.QRect(540, 280, 181, 171))
        self.listView_2.setObjectName("listView_2")
        self.listView_3 = QtWidgets.QListView(Form)
        self.listView_3.setGeometry(QtCore.QRect(540, 450, 181, 171))
        self.listView_3.setObjectName("listView_3")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(540, 0, 181, 111))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

