import serial
import time
from typing import Optional
from .event_bus import event_publisher
from .events import SerialDataReceivedEvent

SERIAL_PORT = '/dev/ttyACM0'    
BAUD_RATE = 115200        

ser: Optional[serial.Serial] = None 

def initialize_serial_connection() -> Optional[serial.Serial]:
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
        time.sleep(2)
        ser.reset_input_buffer()
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

def read_serial_data() -> Optional[str]:
    data = None
    global ser
    if ser and ser.is_open:
        try:
            if ser.in_waiting > 0:
                data_bytes = ser.read(ser.in_waiting)
                data = data_bytes.decode('ascii', errors='ignore').strip()
                data = data.replace('\x00', '')
            if data:
                return data
            else:
                return None
        except Exception as e:
            print("Error reading serial:", repr(e))
            return None
    else:
        print("No serial connection available")
        return None
    
def serial_listen_loop(event_publisher, SerialDataReceivedEvent):

    if not initialize_serial_connection():
        return
        
    try:
        while True:
            data = read_serial_data()
            
            if data is not None:
                event = SerialDataReceivedEvent(data=data)
                event_publisher.publish(event)
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\nLoop stopped")
    finally:
        close_serial_connection()


def close_serial_connection():
    global ser
    if ser and ser.is_open:
        ser.close()
        print("Connection closed")
