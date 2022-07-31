import serial.tools.list_ports
import pyrealsense2 as rs


#check ob arduino verbunden ist und ausgabe des Coms
def check_arduino_connection():
    ports = list(serial.tools.list_ports.comports())

    string = "USB"

    for p in ports:

        print(p)

        check = str(p).find(string)

        if check != -1:

            print("Arduino verbunden")
            return True


    return False

#check verbindung der Kamera
def check_realsense_connection():
    try:
        pipe = rs.pipeline()
        profile = pipe.start()
        return True

    except:
        return False



