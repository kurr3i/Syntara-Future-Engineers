import serial, time

hl = serial.Serial("/dev/serial0", 9600, timeout=0.2)

cmd = bytes([0x55, 0xAA, 0x20, 0x00, 0x00, 0x00, 0x00, 0x20])

while True:
    hl.write(cmd)
    time.sleep(0.1)
    data = hl.read(200)
    if data:
        print("RAW:", data.hex())