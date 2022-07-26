#!/usr/bin/python
import PyQt5.QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QWidget, QAction, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIntValidator, QFont
import open3d as o3d
import sys
import os
import shutil
import ntpath



from Software.Backend_Pakete.export_scan import *
from Software.Backend_Pakete.scan import *
# from Software.Backend_Pakete.arduino_Portcheck import *
# from Software.Backend_Pakete.proviMain import *
from Software.Backend_Pakete.arduino import *
from Software.Backend_Pakete.initialize_scan import *
from Software.Backend_Pakete.process_data import *

# TODO - Statusbar in Setings
# TODO - OpenCV Cam raus nehmen, GUI Kleiner, nut buttons, buttons breiter,gräßer
# TODO -

# ARDUINO - global variables
ardPort = "COM5"
baudRate = 9600
# SCAN - global variables
widthFrame = 848
heightFrame = 480
stepSize = 256


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
        inputWidth = 170
        inputHeight = 30

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setGeometry(QtCore.QRect(0, 400, 400, 20))
        self.statusBar.showMessage("Statusbar test")

        self.ArdPortLabel = QtWidgets.QLabel(self)
        self.ArdPortLabel.setText("COM Port Arduino:")
        self.ArdPortLabel.setGeometry(QtCore.QRect(10, 10, 150, 30))

        self.ArdPort = QtWidgets.QLineEdit(self)
        self.ArdPort.setText("COM3")
        self.ArdPort.setObjectName("portText")
        self.ArdPort.setAlignment(QtCore.Qt.AlignCenter)
        self.ArdPort.setGeometry(QtCore.QRect(170, 10, 30, 30))
        self.ArdPort.setFixedSize(inputWidth, inputHeight)

        self.baudRateLabel = QtWidgets.QLabel(self)
        self.baudRateLabel.setText("Baudrate Arduino:")
        self.baudRateLabel.setGeometry(QtCore.QRect(10, 50, 150, 30))

        self.baudRate = QtWidgets.QLineEdit(self)
        self.baudRate.setText(str(9600))
        self.baudRate.setObjectName("baudrate")
        self.onlyInt = QIntValidator()
        self.baudRate.setValidator(self.onlyInt)
        self.baudRate.setAlignment(QtCore.Qt.AlignCenter)
        self.baudRate.setGeometry(QtCore.QRect(170, 50, 30, 30))
        self.baudRate.setFixedSize(inputWidth, inputHeight)

        self.widthFrameLabel = QtWidgets.QLabel(self)
        self.widthFrameLabel.setText("Frame width:")
        self.widthFrameLabel.setGeometry(QtCore.QRect(10, 90, 150, 30))

        self.widthFrame = QtWidgets.QLineEdit(self)
        self.widthFrame.setText(str(84))
        self.widthFrame.setObjectName("widthFrame")
        self.onlyInt = QIntValidator()
        self.widthFrame.setValidator(self.onlyInt)
        self.widthFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.widthFrame.setGeometry(QtCore.QRect(170, 90, 30, 30))
        self.widthFrame.setFixedSize(inputWidth, inputHeight)

        self.heightFrameLabel = QtWidgets.QLabel(self)
        self.heightFrameLabel.setText("Frame height:")
        self.heightFrameLabel.setGeometry(QtCore.QRect(10, 130, 150, 30))

        self.heightFrame = QtWidgets.QLineEdit(self)
        self.heightFrame.setText(str(480))
        self.heightFrame.setObjectName("heightFrame")
        self.onlyInt = QIntValidator()
        self.heightFrame.setValidator(self.onlyInt)
        self.heightFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.heightFrame.setGeometry(QtCore.QRect(170, 130, 30, 30))
        self.heightFrame.setFixedSize(inputWidth, inputHeight)

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
        global ardPort, baudRate, widthFrame, heightFrame
        port = self.ArdPort.text()
        baudRateGUI = self.baudRate.text()
        wFrame = self.widthFrame.text()
        hFrame = self.heightFrame.text()

        ardPort = port
        baudRate = int(baudRateGUI)
        widthFrame = int(wFrame)
        heightFrame = int(hFrame)
        print(ardPort, baudRate, widthFrame, heightFrame)


# endregion

class Ui_MainWindow(PageWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.exporSTLs = ExportScan()
        self.processFotos = ProcessData()
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
        # Arduino init - Arduino braucht COMPort(string), baudRate(int),

        global ardPort, baudRate, widthFrame, heightFrame, stepSize
        self.arduino = Arduino(comPort=ardPort, baudRate=baudRate, timeout=0.1)
        self.scan = Scan(width=widthFrame, height=heightFrame, framerate=30, autoexposureFrames=10)

        self.initScan = InitializeScan(self.scan.width, self.scan.height, self.scan.framerate,
                                       self.scan.autoexposureFrames)




        self.initScan.startPipeline()
        print("test")
        try:
            while True:
                self.initScan.takeFoto()
                angle = float(self.arduino.giveAngle())
                self.colorInit = self.initScan.color_igm()
                self.depthInit = self.initScan.depth_igm()
                self.intrinInit = self.initScan.intrinsics()

                self.arduino.rotate(stepSize)
                #self.processFotos = ProcessData().processFoto(angle, self.depthInit, self.colorInit, self.intrinInit)

                self.processFotos.processFoto(angle, self.depthInit, self.colorInit, self.intrinInit)
                self.arduino.waitForRotation()

                print("hat funktioniert")
                if angle >= 360:
                   break

        except:
            print("error")
        finally:

            self.initScan.stopPipeline()
            self.arduino.close()
            print("ende process")

    def stopScan(self):


        o3d.visualization.draw_geometries([self.processFotos.getPointcloud()])




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

    def saveFile(self):

        #makeSTL

        self.STL = self.exporSTLs.makeSTL(10,0.5, 7, 8,self.processFotos.main_pcd)
        o3d.visualization.draw_geometries([self.STL])

        #saveSTL

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        self.file = QFileDialog.getSaveFileName(self, "Save STL", options=options)

        print(str(ntpath.basename(self.file[0])))

        print(ntpath.dirname(self.file[0]))

        os.chdir(ntpath.dirname(self.file[0]))

        o3d.io.write_triangle_mesh(str(ntpath.basename(self.file[0])) + ".stl", self.STL)

        """Speichern der Punktwolke/Mesh file (.stl)"""

    def quitApp(self):
        """Programm beenden"""
        close = QtWidgets.QMessageBox.question(self, "Quit", "Are you sure you want to quit?",
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
