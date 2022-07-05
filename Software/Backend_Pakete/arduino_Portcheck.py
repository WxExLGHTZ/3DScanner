import serial.tools.list_ports

def check_arduino_connection():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        print("Arduino verbunden")
        return True
    else:
        print("Arduino nicht verbunden")
        return False
