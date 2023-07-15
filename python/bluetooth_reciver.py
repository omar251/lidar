import serial

bluetooth_port = "COM17"  # Replace with the appropriate port for your Bluetooth device
baud_rate = 9600

# Open the serial port for communication
ser = serial.Serial(bluetooth_port, baud_rate)

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            if(data):
                print(data)
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
