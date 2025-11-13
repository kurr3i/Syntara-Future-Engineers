import threading
import time 
from dataclasses import dataclass
import sys 
import os  
from Core.event_bus import event_publisher
import Core.handlers
from Core.events import SerialDataReceivedEvent
from Core.serial_communication import serial_listen_loop
in_sis = False
data = None


if __name__ == "__main__":
    
    event_publisher.subscribe(SerialDataReceivedEvent, Core.handlers.handle_serial_data)
    
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