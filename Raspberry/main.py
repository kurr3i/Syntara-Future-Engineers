import threading
import time 
from dataclasses import dataclass
import sys 
import os  
from Core.event_bus import event_publisher
from Core.serial_communication import serial_listen_loop
from Core.events import SerialDataReceivedEvent, HuskyLensObjectDetectedEvent
import Core.handlers
import Core.huskylens_reader
in_sis = False
data = None



if __name__ == "__main__":

    hl_thread = threading.Thread(target=huskylens_loop, daemon=True)
    hl_thread.start()
    
    event_publisher.subscribe(SerialDataReceivedEvent, Core.handlers.handle_serial_data)
    event_publisher.subscribe(HuskyLensObjectDetectedEvent, Core.handlers.handle_huskylens_detection)
    
    print("event bus started")


    listener_thread = threading.Thread(
        target=serial_listen_loop, 
        args=(event_publisher, SerialDataReceivedEvent),
        daemon=True
    )
    listener_thread.start()
    

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("ended")