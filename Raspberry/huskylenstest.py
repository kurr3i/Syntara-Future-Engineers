import serial, time

hl = serial.Serial("/dev/serial0", 9600, timeout=0.1)

# pedir datos (comando del protocolo)
cmd = bytes([0x55, 0xAA, 0x11, 0x00, 0x00, 0x00, 0x00, 0x22])

while True:
    hl.write(cmd)         # pedir objetos
    time.sleep(0.1)
    data = hl.read(hl.in_waiting)
    if data:
        print(data)       # respuesta cruda de HuskyLens
