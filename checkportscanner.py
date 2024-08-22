import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port trouvé : {port.device}")

if __name__ == "__main__":
    list_serial_ports()
