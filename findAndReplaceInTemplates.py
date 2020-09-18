# -*- coding: utf-8 -*-
# Copyright: Venkata Ramana P <pvrreddy155@gmail.com>
# encoding: utf8
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Feel free to contribute to this code on https://github.com/itsmepvr/anki-find-and-replace-in-templates

from aqt.qt import *
from aqt.utils import showInfo, askUser
from aqt import mw
from anki.hooks import addHook
from PyQt5 import QtCore, QtGui, QtWidgets

class FindAndReplaceInTemplates_Dialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 440)
        Form.setStyleSheet("")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 441, 25))
        self.comboBox.setObjectName("comboBox")
        notetypes = mw.col.models.allNames()
        notetypes = ['All Notetypes'] + notetypes
        self.comboBox.addItems(notetypes)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 140, 71, 31))
        self.label.setStyleSheet("font-size:20px;\n"
"font-weight:800;")
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(120, 130, 341, 101))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 260, 81, 31))
        self.label_2.setStyleSheet("font-size:20px;\n"
"font-weight:800;")
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(120, 250, 341, 101))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 211, 31))
        self.label_3.setStyleSheet("font-size:20px;")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(160, 370, 191, 41))
        self.pushButton.setStyleSheet("font-size:16px;\n"
"font-weight:800;\n"
"padding:5px 10px;\n"
"font: 75 oblique 14pt \"DejaVu Sans\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 370, 101, 41))
        self.pushButton_2.setStyleSheet("font-size:16px;\n"
"font-weight:800;\n"
"padding:5px 10px;\n"
"font: 75 oblique 14pt \"DejaVu Sans\";")
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.pushButton.clicked.connect(self.findAndReplace)
        self.pushButton_2.clicked.connect(Form.reject)        
        
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(130, 90, 93, 23))
        self.checkBox.setStyleSheet("font-size:16px;")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setGeometry(QtCore.QRect(250, 90, 93, 23))
        self.checkBox_2.setStyleSheet("font-size:16px;")
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Form)
        self.checkBox_3.setGeometry(QtCore.QRect(350, 90, 93, 23))
        self.checkBox_3.setStyleSheet("font-size:16px;")
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setObjectName("checkBox_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Find and Replace in Templates"))
        self.label.setText(_translate("Form", "Find"))
        self.label_2.setText(_translate("Form", "Replace"))
        self.label_3.setText(_translate("Form", "Select Notetype :"))
        self.pushButton.setText(_translate("Form", "Find and Replace"))
        self.pushButton_2.setText(_translate("Form", "Cancel"))
        self.checkBox.setText(_translate("Form", "Front"))
        self.checkBox_2.setText(_translate("Form", "Back"))
        self.checkBox_3.setText(_translate("Form", "CSS"))

    def findAndReplace(self):
        notetype = self.comboBox.currentText()
        findText = self.textEdit.toPlainText()
        replaceText = self.textEdit_2.toPlainText()
        question = self.checkBox.isChecked()
        answer = self.checkBox_2.isChecked()
        css = self.checkBox_3.isChecked()
        
        if askUser('Are you sure you want replace ?', defaultno=True):
            if notetype == 'All Notetypes':
                for model in mw.col.models.all():
                    if css:
                        model['css'] = model['css'].replace(findText, replaceText)   
                    for tmpls in model.get('tmpls'):
                        for key, value in tmpls.items():
                            if key in ('qfmt', 'afmt'):
                                if question and key == 'qfmt':
                                    tmpls[key] = value.replace(findText, replaceText)
                                if answer and key == 'afmt':
                                    tmpls[key] = value.replace(findText, replaceText)
            else:
                for model in mw.col.models.all():
                    if model['name'] == notetype:
                        if css:
                            model['css'] = model['css'].replace(findText, replaceText)  
                        for tmpls in model.get('tmpls'):
                            for key, value in tmpls.items():
                                if key in ('qfmt', 'afmt', 'css'):
                                    if question and key == 'qfmt':
                                        tmpls[key] = value.replace(findText, replaceText)
                                    if answer and key == 'afmt':
                                        tmpls[key] = value.replace(findText, replaceText)                    
            showInfo('Done', parent=mw.app.activeWindow())
            self.textEdit.clear()
            self.textEdit_2.clear()                            
    
    def closeIt(self):
        self.close()    

class MyDialog(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = FindAndReplaceInTemplates_Dialog()
        self.dialog.setupUi(self)

def onBatchEdit(browser):
    dialog = MyDialog()
    if dialog.exec():
        showInfo('dialog closed')

def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Find and Replace in Templates...')
    a.setShortcut(QKeySequence("Ctrl+Alt+T"))
    a.triggered.connect(lambda _, b=browser: onBatchEdit(b))

addHook("browser.setupMenus", setupMenu)