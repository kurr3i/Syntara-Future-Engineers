import serial
import time
from typing import Optional

SERIAL_PORT = '/dev/ttyACM0'    
BAUD_RATE = 115200        

ser: Optional[serial.Serial] = None 

def initialize_serial_connection() -> Optional[serial.Serial]:
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
        time.sleep(2)
        return ser
        
    except serial.SerialException as e:
        print("error")
        return None

def send_command(command: str) -> bool:
    global ser
    if ser and ser.is_open:
        try:
            ser.write(command.encode('ascii'))
            return True
        except Exception as e:
            print("ERROR")
            return False
    else:
        print("No serial conection available")
        return False

def close_serial_connection():
    global ser
    if ser and ser.is_open:
        ser.close()
        print("Connection closed")
