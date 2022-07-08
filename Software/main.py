#!/usr/bin/python
from Frontend_Pakete import *
# from Backend_Pakete.arduino_Portcheck import *

""" Öffnet die GUI File."""

exec(open("./Frontend_Pakete/GUI_3DScanner_ui.py").read())
# check_arduino_connection()

#--------------------------------------------------------------------------------------

#import PyQt5
#from PyQt5 import QtWidgets



#if  check_arduino_connection() == True and check_realsense_connection() == True:


    #exec(open("./Frontend_Pakete/GUI_3DScanner_ui.py").read())
#elif check_realsense_connection() == True and check_arduino_connection() == False:

    #msg = "Arduino is not connected, Please Check Arduino connection"


#elif check_realsense_connection() == False and check_arduino_connection() == True:

   #msg = "Camera is not connected, Please Check Camera connection"

#else:

    #msg = "Camera and Arduino are not connected, Please Check Camera and Arduino Connection"


#app = QtWidgets.QApplication([])

#error_dialog = QtWidgets.QErrorMessage()
#error_dialog.setWindowTitle('Error')

#error_dialog.showMessage(msg)


#app.exec_()