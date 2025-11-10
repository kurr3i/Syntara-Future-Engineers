from serial_communication import send_command
from .events import StartEvent 
from event_bus import event_publisher 

def StartRunning(event: StartEvent):
    send_command('M')
event_publisher.subscribe(StartEvent, StartRunning)