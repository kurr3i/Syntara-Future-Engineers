from .serial_communication import send_command
from .events import StartEvent, SerialDataReceivedEvent
from .event_bus import event_publisher 

def handle_serial_data(event: SerialDataReceivedEvent):

    global in_sis
    data = event.data

    if data == 'q':
        if not in_sis:
            in_sis = True
            
            print("hello world")

        else:
            print("System already initialized")
