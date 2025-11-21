import serial

hl = serial.Serial("/dev/serial0", 9600, timeout=1)

while True:
    b = hl.read(1)
    if b:
        print("Byte:", b)
