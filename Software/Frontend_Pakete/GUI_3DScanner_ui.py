#!/usr/bin/python

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QWidget, QAction, QHBoxLayout
from PyQt5.QtGui import QPainter, QImage
import cv2
import open3d as o3d
import sys
import time
import threading
import queue as Queue
import os
import shutil

IMG_SIZE = 1920, 1080  # 640,480 or 1280,720 or 1920,1080
IMG_FORMAT = QImage.Format_RGB888
DISP_SCALE = 2  # Scaling factor for display image
DISP_MSEC = 50  # Delay between display cycles
CAP_API = cv2.CAP_ANY  # API: CAP_ANY or CAP_DSHOW etc...
EXPOSURE = 0  # Zero for automatic exposure
camera_num = 1  # Default camera (first in list)
image_queue = Queue.Queue()  # Queue to hold images
capturing = True


# region Cam Methods + Image Class
def grab_images(cam_num, queue):
    cap = cv2.VideoCapture(cam_num - 1 + CAP_API)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
    if EXPOSURE:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    else:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    while capturing:
        if cap.grab():
            retval, image = cap.retrieve(0)
            if image is not None and queue.qsize() < 2:
                queue.put(image)
            else:
                time.sleep(DISP_MSEC / 1000.0)
        else:
            print("Error: can't grab camera image")
            break
    cap.release()


class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        self.setGeometry(QtCore.QRect(50, 50, 50, 50))
        self.setMinimumSize(image.size())
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


# endregion

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
        width = 900
        height = 470
        self.resize(width, height)
        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

        self.UiComponents()

    def goBack(self):
        global capturing
        capturing = True
        self.goto("main")

    def UiComponents(self):
        self.portLabel = QtWidgets.QLabel(self)
        self.portLabel.setText("Serial Port Eingabe")
        self.portLabel.setGeometry(QtCore.QRect(120, 50, 150, 30))

        self.port = QtWidgets.QLineEdit(self)
        self.port.setText(str(camera_num))
        self.port.setObjectName("portText")
        self.port.setGeometry(QtCore.QRect(250, 50, 30, 30))
        self.port.setMinimumSize(QtCore.QSize(30, 30))
        self.port.setMaximumSize(QtCore.QSize(30, 30))

        self.backButton = QtWidgets.QPushButton("Back to Main", self)
        self.backButton.setGeometry(QtCore.QRect(750, 50, 160, 400))
        self.backButton.setMinimumSize(QtCore.QSize(120, 40))
        self.backButton.setMaximumSize(QtCore.QSize(120, 40))
        self.backButton.clicked.connect(self.goBack)

        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setGeometry(QtCore.QRect(750, 200, 160, 400))
        self.saveButton.setMinimumSize(QtCore.QSize(120, 40))
        self.saveButton.setMaximumSize(QtCore.QSize(120, 40))
        self.saveButton.clicked.connect(self.SaveSettings)

    def SaveSettings(self):
        global camera_num
        pText = self.port.text()
        camera_num = int(pText)


# endregion

class Ui_MainWindow(PageWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.setWindowTitle("3D Scanner")

    # region Cam Methods
    def startCam(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:
                                   self.show_image(image_queue, self.disp, DISP_SCALE))
        self.timer.start(DISP_MSEC)
        self.capture_thread = threading.Thread(target=grab_images,
                                               args=(camera_num, image_queue))
        self.capture_thread.start()

    def stopCam(self):
        global capturing
        capturing = False
        self.capture_thread.join()
        cap = cv2.VideoCapture(1 - 1 + CAP_API)
        cap.release()

    def show_image(self, imageq, display, scale):
        if not imageq.empty():
            image = imageq.get()
            if image is not None and len(image) > 0:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.display_image(img, display, scale)

    def display_image(self, img, display, scale=1):
        disp_size = img.shape[1] // scale, img.shape[0] // scale
        disp_bpl = disp_size[0] * 3
        if scale > 1:
            img = cv2.resize(img, disp_size, interpolation=cv2.INTER_CUBIC)
            qimg = QImage(img.data, disp_size[0], disp_size[1], disp_bpl, IMG_FORMAT)
        display.setImage(qimg)

    # endregion

    def UiComponents(self):
        app.aboutToQuit.connect(self.closeEvent)
        self.startCam()
        self.setWindowTitle("3D Scanner")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.displays = QHBoxLayout(self.centralwidget)
        self.disp = ImageWidget(self)
        self.displays.addWidget(self.disp)

        buttonWidth = 120
        buttonHeight = 40
        btnSize = QtCore.QSize(buttonWidth, buttonHeight)

        self.statusBar = QtWidgets.QStatusBar(self.centralwidget)
        self.statusBar.setGeometry(QtCore.QRect(0, 480, 900, 20))
        self.statusBar.showMessage("Statusbar test")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(750, 30, 160, 450))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.starteKameraBtn = QtWidgets.QPushButton()
        self.starteKameraBtn.setGeometry(QtCore.QRect(750, 330, 160, 450))
        self.starteKameraBtn.setMinimumSize(btnSize)
        self.starteKameraBtn.setMaximumSize(btnSize)
        self.starteKameraBtn.setObjectName("starteCamTest")
        self.verticalLayout.addWidget(self.starteKameraBtn)

        self.stopKameraBtn = QtWidgets.QPushButton()
        self.stopKameraBtn.setGeometry(QtCore.QRect(750, 330, 160, 450))
        self.stopKameraBtn.setMinimumSize(btnSize)
        self.stopKameraBtn.setMaximumSize(btnSize)
        self.stopKameraBtn.setObjectName("stopCamTest")
        self.verticalLayout.addWidget(self.stopKameraBtn)

        self.helpButton = QtWidgets.QPushButton()
        self.helpButton.setGeometry(QtCore.QRect(750, 380, 160, 450))
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
        self.stopScanButton.clicked.connect(self.stopCam)
        self.importButton.clicked.connect(self.importFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.settingsButton.clicked.connect(self.make_handleButton("settingsButton"))
        self.helpButton.clicked.connect(self.helpMainWindow)
        self.quitButton.clicked.connect(self.quitApp)
        self.starteKameraBtn.clicked.connect(self.startCam)
        self.stopKameraBtn.clicked.connect(self.stopCam)

        self.mainMenu = self.menuBar()
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.closeEvent)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)

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
        self.starteKameraBtn.setText(_translate("MainWindow", "Start Cam"))
        self.stopKameraBtn.setText(_translate("MainWindow", "Stop Cam"))

    # region Button Funktionalitäten

    def helpMainWindow(self):
        self.w = HelpWindow()
        self.w.show()

    def make_handleButton(self, button):
        def handleButton():
            # global capturing
            # capturing = False
            # self.capture_thread.join()
            self.stopCam()
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
                                                    "PC Format (*.ply *.asc)")
        file_path, file_ext = os.path.splitext(fileDialog)

        if file_ext == ".ply":
            dataPath = "./Frontend_Pakete/data/importedPLYFile.ply"
            shutil.copy(fileDialog, dataPath)

            PLYFile = os.getcwd() + "/Frontend_Pakete/data/importedPLYFile.ply"
            pcd = o3d.io.read_point_cloud(PLYFile)
            o3d.visualization.draw_geometries([pcd])
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
        close = QtWidgets.QMessageBox.question(self, "QUIT", "Are you sure you want to stop process?",
                                               QMessageBox.No | QMessageBox.Yes)
        if close == QMessageBox.Yes:
            global capturing
            capturing = False
            self.capture_thread.join()
            QtCore.QCoreApplication.instance().quit()

    def closeEvent(self):
        global capturing
        capturing = False
        self.capture_thread.join()
        QtCore.QCoreApplication.instance().quit()

    # endregion


# region Window Klasse für Stacked Widgets
class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        width = 900
        height = 500
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
    if len(sys.argv) > 1:
        try:
            camera_num = int(sys.argv[1])
        except:
            camera_num = 0
    if camera_num < 1:
        print("Invalid camera number '%s'" % sys.argv[1])
    else:
        app = QtWidgets.QApplication(sys.argv)
        # seting = SettingsWindow()
        # seting.show()
        w = Window()
        w.show()
        sys.exit(app.exec_())
