#!/usr/bin/python

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QWidget, QAction, QHBoxLayout
from PyQt5.QtGui import QIntValidator, QFont
import cv2
import open3d as o3d
import sys
import time
import threading
import queue as Queue
import os
import shutil

from Software.Backend_Pakete.export_scan import *


# TODO - Statusbar in Setings
# TODO - OpenCV Cam raus nehmen, GUI Kleiner, nut buttons, buttons breiter,gräßer
# TODO -


# region PageWindows, HelpWindow, SettingWindow
class PageWindow(QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class HelpWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Help")
        self.UiComponents()

    def UiComponents(self):
        width = 400
        height = 400
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))
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
        self.text.move(10, 10)
        self.text.resize(380, 380)
        self.text.setDisabled(True)
        self.text.setReadOnly(True)


class SettingsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Settings")
        width = 350
        height = 420
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

        self.UiComponents()

    def goBack(self):
        self.goto("main")

    def UiComponents(self):

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setGeometry(QtCore.QRect(0, 400, 400, 20))
        self.statusBar.showMessage("Statusbar test")

        self.portLabel = QtWidgets.QLabel(self)
        self.portLabel.setText("Serial Port Eingabe")
        self.portLabel.setGeometry(QtCore.QRect(40, 30, 150, 30))

        self.port = QtWidgets.QLineEdit(self)
        self.port.setText(str(1))
        self.port.setObjectName("portText")
        self.onlyInt = QIntValidator()
        self.port.setValidator(self.onlyInt)
        self.port.setAlignment(QtCore.Qt.AlignCenter)
        self.port.setGeometry(QtCore.QRect(190, 30, 30, 30))
        self.port.setMinimumSize(QtCore.QSize(30, 30))
        self.port.setMaximumSize(QtCore.QSize(30, 30))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 300, 200, 100))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.backButton = QtWidgets.QPushButton("Back to Main", self)
        self.backButton.setGeometry(QtCore.QRect(70, 360, 160, 400))
        self.backButton.setMinimumSize(QtCore.QSize(200, 40))
        self.backButton.setMaximumSize(QtCore.QSize(200, 40))
        self.backButton.clicked.connect(self.goBack)


        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setGeometry(QtCore.QRect(70, 320, 160, 400))
        self.saveButton.setMinimumSize(QtCore.QSize(200, 40))
        self.saveButton.setMaximumSize(QtCore.QSize(200, 40))
        self.saveButton.clicked.connect(self.SaveSettings)

        self.verticalLayout.addWidget(self.saveButton)
        self.verticalLayout.addWidget(self.backButton)

    def SaveSettings(self):
        pText = self.port.text()
        print(pText)


# endregion

class Ui_MainWindow(PageWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.setWindowTitle("3D Scanner")

    def UiComponents(self):
        app.aboutToQuit.connect(self.closeEvent)
        self.setWindowTitle("3D Scanner")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        buttonWidth = 200
        buttonHeight = 40
        btnSize = QtCore.QSize(buttonWidth, buttonHeight)

        self.statusBar = QtWidgets.QStatusBar(self.centralwidget)
        self.statusBar.setGeometry(QtCore.QRect(0, 400, 400, 20))
        self.statusBar.showMessage("Statusbar test")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 20, 200, 450))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.helpButton = QtWidgets.QPushButton()
        self.helpButton.setGeometry(QtCore.QRect(20, 380, 160, 450))
        self.helpButton.setMinimumSize(btnSize)
        self.helpButton.setMaximumSize(btnSize)
        self.helpButton.setObjectName("helpButton")

        self.startScanButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startScanButton.setMinimumSize(btnSize)
        self.startScanButton.setMaximumSize(btnSize)
        self.startScanButton.setObjectName("startScanButton")
        self.verticalLayout.addWidget(self.startScanButton)

        self.stopScanButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopScanButton.setMinimumSize(btnSize)
        self.stopScanButton.setMaximumSize(btnSize)
        self.stopScanButton.setObjectName("stopScanButton")
        self.verticalLayout.addWidget(self.stopScanButton)

        spacerItem = QtWidgets.QSpacerItem(30, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.importButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.importButton.setMinimumSize(btnSize)
        self.importButton.setMaximumSize(btnSize)
        self.importButton.setObjectName("importButton")
        self.verticalLayout.addWidget(self.importButton)

        self.saveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveButton.setMinimumSize(btnSize)
        self.saveButton.setMaximumSize(btnSize)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)

        spacerItem1 = QtWidgets.QSpacerItem(30, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)

        self.settingsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.settingsButton.setMinimumSize(btnSize)
        self.settingsButton.setMaximumSize(btnSize)
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout.addWidget(self.settingsButton)

        self.verticalLayout.addWidget(self.helpButton)

        # spacerItem2 = QtWidgets.QSpacerItem(200, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # self.verticalLayout.addItem(spacerItem2)

        self.quitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.quitButton.setMinimumSize(btnSize)
        self.quitButton.setMaximumSize(btnSize)
        self.quitButton.setObjectName("quitButton")
        self.verticalLayout.addWidget(self.quitButton)

        spacerItem2 = QtWidgets.QSpacerItem(150, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        self.setCentralWidget(self.centralwidget)

        # button connect
        self.startScanButton.clicked.connect(self.startScan)
        self.stopScanButton.clicked.connect(self.stopScan)
        self.importButton.clicked.connect(self.importFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.settingsButton.clicked.connect(self.make_handleButton("settingsButton"))
        self.helpButton.clicked.connect(self.helpMainWindow)
        self.quitButton.clicked.connect(self.quitApp)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.quitApp)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

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

    # region Button Funktionalitäten

    def helpMainWindow(self):
        self.w = HelpWindow()
        self.w.show()

    def make_handleButton(self, button):
        def handleButton():
            if button == "settingsButton":
                self.goto("settings")

        return handleButton

    def startScan(self):
        """Verbindet sich mit der Kamera und startet den Scan Prozess."""

    def stopScan(self):
        """Stoppt den Scan Prozess."""

    def importFile(self):
        """Startet QFileDialog. Eine .ply oder .stl Datei kann ausgewählt werden. """
        fileDialog, _ = QFileDialog.getOpenFileName(self, "Punktwolke Datei öffnen", "",
                                                    "PC Format (*.ply)")
        file_path, file_ext = os.path.splitext(fileDialog)

        if file_ext == ".ply":
            dataPath = "./Frontend_Pakete/data/importedPLYFile.ply"
            shutil.copy(fileDialog, dataPath)

            PLYFile = os.getcwd() + "/Frontend_Pakete/data/importedPLYFile.ply"
            pcd = o3d.io.read_point_cloud(PLYFile)
            o3d.visualization.draw_geometries([pcd],
                                              width=500,
                                              height=500,
                                              window_name="Imported Point Cloud")
        # else:
        #     msg = "This .ply file seems broken. Try another."
        #     q = QMessageBox(QMessageBox.Warning, "...", QString(msg))
        #     q.setStandardButtons(QMessageBox.OK)
        #     q.exec_()
        # elif file_ext == ".pcd":
        #     dataPath = "./Frontend_Pakete/data/importedPCDFile.pcd"
        #     shutil.copy(fileDialog, dataPath)
        #     PLYFile = os.getcwd() + "/Frontend_Pakete/data/importedPLYFile.ply"
        #     pcd = o3d.io.read_point_cloud(PLYFile)
        #     o3d.visualization.draw_geometries([pcd])
        # elif file_ext == ".stl":
        #     dataPath = "./Frontend_Pakete/data/importedSTLFile.stl"
        #     shutil.copy(fileDialog, dataPath)
        #
        #     STLFile = os.getcwd() + "/Frontend_Pakete/data/importedSTLFile.stl"
        #
        #     o3d.visualization.draw_geometries([STLFile], zoom=0.8)

    def saveFile(self):
        """Speichern der Punktwolke/Mesh file (.stl)"""

    def quitApp(self):
        """Programm beenden"""
        close = QtWidgets.QMessageBox.question(self, "QUIT", "Are you sure you want to quit?",
                                               QMessageBox.No | QMessageBox.Yes)
        if close == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def closeEvent(self):
        QtCore.QCoreApplication.instance().quit()
    # endregion


# region Window Klasse für Stacked Widgets
class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        width = 350
        height = 420

        self.setWindowTitle("3D Scanner")
        self.setObjectName("MainWindow")
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.m_pages = {}
        self.register(Ui_MainWindow(), "main")
        self.register(SettingsWindow(), "settings")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


# endregion

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # seting = SettingsWindow()
    # seting.show()
    w = Window()
    w.show()
    sys.exit(app.exec_())
