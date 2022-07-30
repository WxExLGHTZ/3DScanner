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
from Software.Backend_Pakete.arduino_Portcheck import *

# ARDUINO - global variables
ardPort = "COM5"
baudRate = 9600
# SCAN - global variables
widthFrame =   848
heightFrame = 480
stepSize = 256
# MESH Parameters- global variables
kPoints = 20
stdRatio = 0.5
depth = 7
iterations = 8

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
        width = 800
        height = 450
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

        self.UiComponents()

    def goBack(self):
        self.goto("main")

    def UiComponents(self):
        inputWidth = 150
        inputHeight = 30
        self.onlyInt = QIntValidator()  # Allows only integer inside QText

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setGeometry(QtCore.QRect(0, 430, 800, 20))
        self.statusBar.showMessage("Statusbar test")

        self.headerLabelArduino = QtWidgets.QLabel(self)
        self.headerLabelArduino.setText("Arduino Settings")
        self.headerLabelArduino.setAlignment(QtCore.Qt.AlignCenter)

        self.headerLabelCam = QtWidgets.QLabel(self)
        self.headerLabelCam.setText("Camera Settings")
        self.headerLabelCam.setAlignment(QtCore.Qt.AlignCenter)

        self.ArdPort = QtWidgets.QLineEdit(self)
        self.ArdPort.setText("COM5")
        self.ArdPort.setObjectName("portText")
        self.ArdPort.setAlignment(QtCore.Qt.AlignCenter)
        # self.ArdPort.setFixedSize(inputWidth, inputHeight)

        self.baudRate = QtWidgets.QLineEdit(self)
        self.baudRate.setText(str(9600))
        self.baudRate.setObjectName("baudrate")
        self.baudRate.setValidator(self.onlyInt)
        self.baudRate.setAlignment(QtCore.Qt.AlignCenter)
        # self.baudRate.setFixedSize(inputWidth, inputHeight)

        self.widthFrame = QtWidgets.QLineEdit(self)
        self.widthFrame.setText(str(848))
        self.widthFrame.setObjectName("widthFrame")
        self.widthFrame.setValidator(self.onlyInt)
        self.widthFrame.setAlignment(QtCore.Qt.AlignCenter)
        # self.widthFrame.setFixedSize(inputWidth, inputHeight)

        self.heightFrame = QtWidgets.QLineEdit(self)
        self.heightFrame.setText(str(480))
        self.heightFrame.setObjectName("heightFrame")
        self.heightFrame.setValidator(self.onlyInt)
        self.heightFrame.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        self.stepSize = QtWidgets.QLineEdit(self)
        self.stepSize.setText(str(256))
        self.stepSize.setObjectName("stepSize")
        self.stepSize.setValidator(self.onlyInt)
        self.stepSize.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        self.kp = QtWidgets.QLineEdit(self)
        self.kp.setText(str(10))
        self.kp.setObjectName("kPoints")
        self.kp.setValidator(self.onlyInt)
        self.kp.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        self.stdRatio = QtWidgets.QLineEdit(self)
        self.stdRatio.setText(str(0.5))
        self.stdRatio.setObjectName("stdRatio")
        self.stdRatio.setValidator(self.onlyInt)
        self.stdRatio.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        self.depthL = QtWidgets.QLineEdit(self)
        self.depthL.setText(str(7))
        self.depthL.setObjectName("depth")
        self.depthL.setValidator(self.onlyInt)
        self.depthL.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        self.iter = QtWidgets.QLineEdit(self)
        self.iter.setText(str(8))
        self.iter.setObjectName("iterations")
        self.iter.setValidator(self.onlyInt)
        self.iter.setAlignment(QtCore.Qt.AlignCenter)
        # self.heightFrame.setFixedSize(inputWidth, inputHeight)

        #### Form LINKSOBEN
        self.formWidget = QtWidgets.QWidget(self)
        self.formWidget.setGeometry(QtCore.QRect(0, 0, 320, 200))
        self.formWidget.setObjectName("formWidget")

        self.mainFormLayout = QFormLayout(self.formWidget)
        self.mainFormLayout.setObjectName("Form Layout")
        self.mainFormLayout.addWidget(self.headerLabelArduino)

        self.mainFormLayout.addRow("COM Port Arduino:", self.ArdPort)
        self.mainFormLayout.addRow("Baudrate Arduino:", self.baudRate)

        #### Form LINKSUNTEN - CAM SETTINGS
        self.camFormWidget = QtWidgets.QWidget(self)
        self.camFormWidget.setGeometry(QtCore.QRect(265, 0, 320, 320))
        self.camFormWidget.setObjectName("CamFormWidget")

        self.camLayout = QFormLayout(self.camFormWidget)
        self.camLayout.setObjectName("Cam Layout")
        self.camLayout.addWidget(self.headerLabelCam)

        self.camLayout.addRow("Frame width: ", self.widthFrame)
        self.camLayout.addRow("Frame Height:", self.heightFrame)
        self.camLayout.addRow("Step Size:", self.stepSize)
        self.camLayout.addRow("K Points:", self.kp)
        self.camLayout.addRow("Ratio:", self.stdRatio)
        self.camLayout.addRow("Depth:", self.depthL)
        self.camLayout.addRow("Iterations:", self.iter)

        ### RECHTE SEITE
        # verticalLayout
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(570, 20, 200, 430))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.resetDefault = QtWidgets.QPushButton("Reset Default Settings", self)
        self.resetDefault.setGeometry(QtCore.QRect(80, 240, 160, 400))
        self.resetDefault.setFixedSize(200, 40)
        self.resetDefault.clicked.connect(self.resetDefaultSettings)

        self.backButton = QtWidgets.QPushButton("Back to Main", self)
        self.backButton.setGeometry(QtCore.QRect(70, 360, 160, 400))
        self.backButton.setMinimumSize(QtCore.QSize(200, 40))
        self.backButton.setMaximumSize(QtCore.QSize(200, 40))
        self.backButton.clicked.connect(self.goBack)

        self.saveButton = QtWidgets.QPushButton("Save Settings", self)
        self.saveButton.setGeometry(QtCore.QRect(70, 280, 160, 400))
        self.saveButton.setMinimumSize(QtCore.QSize(200, 40))
        self.saveButton.setMaximumSize(QtCore.QSize(200, 40))
        self.saveButton.clicked.connect(self.SaveSettings)

        spacerItem2 = QtWidgets.QSpacerItem(200, 180, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.verticalLayout.addWidget(self.resetDefault)
        self.verticalLayout.addWidget(self.saveButton)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.backButton)

    def SaveSettings(self):
        global ardPort, baudRate, widthFrame, heightFrame, stepSize
        global kPoints, stdRatio, depth, iterations

        ardPort = self.ArdPort.text()
        baudRate = int(self.baudRate.text())
        widthFrame = int(self.widthFrame.text())
        heightFrame = int(self.heightFrame.text())
        stepSize = int(self.stepSize.text())
        kPoints = int(self.kp.text())
        stdRatio = float(self.stdRatio.text())
        depth = int(self.depthL.text())
        iterations = int(self.iter.text())
        print(ardPort, baudRate, widthFrame, heightFrame, stepSize, kPoints, stdRatio, depth, iterations)

    def resetDefaultSettings(self):
        global ardPort, baudRate, widthFrame, heightFrame, stepSize
        global kPoints, stdRatio, depth, iterations

        ardPort = "COM3"
        baudRate = 9600
        widthFrame = 848
        heightFrame = 480
        stepSize = 256
        kPoints = 10
        stdRatio = 0.5
        depth = 7
        iterations = 8
        self.ArdPort.setText(ardPort)
        self.baudRate.setText(str(baudRate))
        self.widthFrame.setText(str(widthFrame))
        self.heightFrame.setText(str(heightFrame))
        self.kp.setText(str(kPoints))
        self.stepSize.setText(str(stepSize))
        self.stdRatio.setText(str(stdRatio))
        self.depthL.setText(str(depth))
        self.iter.setText(str(iterations))


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
        btnSizeStart = QtCore.QSize(200, 60)

        self.statusBar = QtWidgets.QStatusBar(self.centralwidget)
        self.statusBar.setGeometry(QtCore.QRect(0, 450, 800, 20))
        self.statusBar.showMessage("Statusbar test")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(570, 20, 200, 470))
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
        self.startScanButton.setMinimumSize(btnSizeStart)
        self.startScanButton.setMaximumSize(btnSizeStart)
        self.startScanButton.setObjectName("startScanButton")
        self.verticalLayout.addWidget(self.startScanButton)

        spacerItem = QtWidgets.QSpacerItem(30, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.showPCButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.showPCButton.setMinimumSize(btnSize)
        self.showPCButton.setMaximumSize(btnSize)
        self.showPCButton.setObjectName("showPCButton")

        self.importButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.importButton.setMinimumSize(btnSize)
        self.importButton.setMaximumSize(btnSize)
        self.importButton.setObjectName("importButton")
        self.verticalLayout.addWidget(self.importButton)
        self.verticalLayout.addWidget(self.showPCButton)

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
        self.showPCButton.clicked.connect(self.showPointCloud)
        self.importButton.clicked.connect(self.importFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.settingsButton.clicked.connect(self.make_handleButton("settingsButton"))
        self.helpButton.clicked.connect(self.helpMainWindow)
        self.quitButton.clicked.connect(self.quitApp)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.quitApp)

        self.showPCButton.setEnabled(False)
        # self.importButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("3D-Scanner", "MainWindow"))
        self.startScanButton.setText(_translate("MainWindow", "Start Scan"))
        self.showPCButton.setText(_translate("MainWindow", "Show Pointcloud"))
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

        ardcheck = check_arduino_connection()
        camcheck = check_realsense_connection()

        if ardcheck == True and camcheck == True:

            global ardPort, baudRate, widthFrame, heightFrame, stepSize
            self.arduino = Arduino(comPort=ardPort, baudRate=baudRate, timeout=0.1)
            self.scan = Scan(width=widthFrame, height=heightFrame, framerate=30, autoexposureFrames=10)

            self.initScan = InitializeScan(self.scan.width, self.scan.height, self.scan.framerate,
                                           self.scan.autoexposureFrames)

            self.initScan.pipelineStarten()

            try:
                while True:
                    self.initScan.aufnahme()
                    angle = float(self.arduino.winkel())
                    self.colorInit = self.initScan.color_img()
                    self.depthInit = self.initScan.depth_img()
                    self.intrinInit = self.initScan.intrinsics()

                    self.arduino.rotieren(stepSize)
                    # self.processFotos = ProcessData().processFoto(angle, self.depthInit, self.colorInit, self.intrinInit)

                    self.processFotos.konvertieren(angle, self.depthInit, self.colorInit, self.intrinInit)
                    self.arduino.warteAufRotation()

                    if angle >= 360:
                        break

            except:
                print("error")
            finally:
                self.showPCButton.setEnabled(True)
                self.saveButton.setEnabled(True)
                # self.importButton.setEnabled(True)
                self.initScan.pipelineStoppen()
                self.arduino.close()
                print("ende process")
        else:
            print("error, please check connections")

    def showPointCloud(self):
        o3d.visualization.draw_geometries([self.processFotos.getPointcloud()])

    def importFile(self):
        """Startet QFileDialog. Eine .ply oder .stl Datei kann ausgewählt werden. """
        fDialog = QFileDialog(self)
        fDialog.setFileMode(QFileDialog.Directory)
        fDialog.setNameFilter("PC Format (*.pcd)")

        fileDialog, _ = fDialog.getOpenFileName(self, "Punktwolke Datei öffnen", "",
                                                "PC Format (*.pcd)")
        print(fileDialog)
        o3d.visualization.draw_geometries(fileDialog)
        file_path, file_ext = os.path.splitext(fileDialog)

        if file_ext == ".ply":
            dataPath = "./Frontend_Pakete/data/importedPLYFile.pcd"
            shutil.copy(fileDialog, dataPath)

            PLYFile = os.getcwd() + "/Frontend_Pakete/data/importedPLYFile.pcd"
            pcd = o3d.io.read_point_cloud(PLYFile)

            if o3d.io.read_point_cloud(PLYFile):
                self.saveButton.setEnabled(True)

            o3d.visualization.draw_geometries([pcd],
                                              width=500,
                                              height=500,
                                              window_name="Imported Point Cloud")
            self.processFotos.hauptPointCloud = pcd
            print(self.processFotos.hauptPointCloud)

    def saveFile(self):

        # makeSTL
        print(self.processFotos.hauptPointCloud)
        self.STL = self.exporSTLs.stlErstellen(10, 0.5, 7, 8, self.processFotos.hauptPointCloud)
        o3d.visualization.draw_geometries([self.STL])

        # saveSTL

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
        width = 800
        height = 470

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
