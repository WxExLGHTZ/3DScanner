import serial.tools.list_ports

def check_arduino_connection():
    ports = list(serial.tools.list_ports.comports())

    string = "USB"

    for p in ports:

        check = str(p).find(string)

        if check == -1:
            print("Arduino nicht verbunden")

        else:
            print("Arduino verbunden")




