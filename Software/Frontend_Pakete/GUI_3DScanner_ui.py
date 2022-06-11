# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_3DScanner.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class helpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        width = 400
        height = 400
        self.setWindowTitle("Help")
        self.resize(width,height)
        self.setMaximumSize(QtCore.QSize(width,height))
        self.setMinimumSize(QtCore.QSize(width,height))
        self.text = QPlainTextEdit(self)
        self.text.insertPlainText("Anleitung\n\n\n"
                                  "Vor der Nutzung sollte die Serial Ports richtig gesetzt werden. Dies findest du unter dem Button \"Settings Knopf\"\n\n"
                                  "Liegt das Objekt auf der Plattform, so kann der Scan gestartet werden -> \"Start Scan Knopf\""
                                  "\nDieser Prozess dauert weniger als 1 Minute.\n\n"
                                  "Nach dem Scan wird das gescannte Objekt als Punktwolke auf der linken Seite des Programms angezeigt."
                                  "Diese Punktwolke kann anschließend als .stl Datei umgewandelt werden und abgespeichert werden ->\"Save Knopf\""
                                  "\n\nMit \"Import\"-Knopf kann eine .stl oder eine Punktwolke Datei eingefügt werden und man kann diese dann anschließend"
                                  "im 3D-Viewer anschauen."
                                  "\nMit \"Exit\"-Knopf wird das Programm beendet.")
        self.text.move(10,10)
        self.text.resize(380,380)
        self.text.setDisabled(True)
        self.text.setReadOnly(True)

class settingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        width = 400
        height = 400
        self.setWindowTitle("Settings")
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))
        self.text = QTextEdit(self)
        self.text.setText("Setting Page")
        self.text.move(10, 10)
        self.text.resize(380, 380)
        self.text.setReadOnly(True)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 700)
        MainWindow.setMinimumSize(QtCore.QSize(950, 700))
        MainWindow.setMaximumSize(QtCore.QSize(950, 700))



        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(780, 50, 162, 464))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.startScanButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startScanButton.setMinimumSize(QtCore.QSize(150, 40))
        self.startScanButton.setMaximumSize(QtCore.QSize(150, 40))
        self.startScanButton.setObjectName("startScanButton")
        self.verticalLayout.addWidget(self.startScanButton)
        self.stopScanButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopScanButton.setMinimumSize(QtCore.QSize(150, 40))
        self.stopScanButton.setMaximumSize(QtCore.QSize(150, 40))
        self.stopScanButton.setObjectName("stopScanButton")
        self.verticalLayout.addWidget(self.stopScanButton)
        spacerItem = QtWidgets.QSpacerItem(150, 170, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.importButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.importButton.setMinimumSize(QtCore.QSize(150, 40))
        self.importButton.setMaximumSize(QtCore.QSize(150, 40))
        self.importButton.setObjectName("importButton")
        self.verticalLayout.addWidget(self.importButton)
        self.saveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveButton.setMinimumSize(QtCore.QSize(150, 40))
        self.saveButton.setMaximumSize(QtCore.QSize(150, 40))
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        self.settingsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.settingsButton.setMinimumSize(QtCore.QSize(150, 40))
        self.settingsButton.setMaximumSize(QtCore.QSize(150, 40))
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout.addWidget(self.settingsButton)
        self.quitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.quitButton.setMinimumSize(QtCore.QSize(150, 40))
        self.quitButton.setMaximumSize(QtCore.QSize(150, 40))
        self.quitButton.setObjectName("quitButton")
        self.verticalLayout.addWidget(self.quitButton)
        spacerItem2 = QtWidgets.QSpacerItem(150, 170, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        #self.helpButton.setGeometry(QtCore.QRect(0, 10, 150, 40))
        self.helpButton.setGeometry(QtCore.QRect(780, 620, 162, 464))
        self.helpButton.setMinimumSize(QtCore.QSize(150, 40))
        self.helpButton.setMaximumSize(QtCore.QSize(150, 40))
        self.helpButton.setObjectName("helpButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # button connect
        self.startScanButton.clicked.connect(self.startScan)
        self.stopScanButton.clicked.connect(self.stopScan)
        self.importButton.clicked.connect(self.importFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.settingsButton.clicked.connect(self.settingsMainWindow)
        self.helpButton.clicked.connect(self.helpMainWindow)
        self.quitButton.clicked.connect(self.quitApp)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("3D-Scanner", "MainWindow"))
        self.startScanButton.setText(_translate("MainWindow", "Start Scan"))
        self.stopScanButton.setText(_translate("MainWindow", "Stop Scan"))
        self.importButton.setText(_translate("MainWindow", "Import"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))
        self.helpButton.setText(_translate("MainWindow", "Help"))

    def helpMainWindow(self):
        self.w = helpWindow()
        self.w.show()

    def settingsMainWindow(self):
        self.settings = settingsWindow()
        self.settings.show()


    def startScan(self):
        """Verbindet sich mit der Kamera und startet den Scan Prozess."""
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Start Scan Button Test")
        self.msg.setText("Button Test\n\n\"Software verbindet sich mit der Kamera und der Prozess startet.\"\n\nTest bestanden!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()

    def stopScan(self):
        """Stoppt den Scan Prozess."""
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Stop Scan Button Test")
        self.msg.setText(
            "Button Test\n\n\"Software stoppen...\"\n\nTest bestanden!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()


    def importFile(self):
        """Startet QFileDialog. Eine .stl Datei kann ausgewählt werden. """
        self.msg = QMessageBox()
        self.msg.setWindowTitle("import Button Test")
        self.msg.setText(
            "Button Test\n\n\"File Dialog öffnet sich. Datei kann ausgewählt werden.\"\n\nTest bestanden!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()

    def saveFile(self):
        """Speichern der Punktwolke/Mesh file (.stl)"""
        self.msg = QMessageBox()
        self.msg.setWindowTitle("save Button Test")
        self.msg.setText(
            "Button Test\n\n\"File Dialog öffnet sich. Datei kann als .stl abgespeichert werden.\"\n\nTest bestanden!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()

    def quitApp(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

