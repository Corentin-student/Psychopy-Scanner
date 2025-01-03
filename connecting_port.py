import serial
import time

port = 'COM7'
baud_rate = 115200
timeout = 1

try:
    with serial.Serial(port, baud_rate, timeout=timeout) as ser:
        if ser.isOpen():
            print(f"Port {port} is open.")
            time.sleep(2)
            if ser.inWaiting() > 0:
                response = ser.read(ser.inWaiting()).decode()
                print(f"Received response: {response}")
            else:
                print("No response received.")
        else:
            print("Failed to open port.")
except serial.SerialException as e:
    print(f"Error: {e}")
