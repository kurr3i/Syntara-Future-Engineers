from .serial_communication import send_command
from .events import StartEvent, SerialDataReceivedEvent
from .event_bus import event_publisher 
in_sis = False 


def handle_serial_data(event: SerialDataReceivedEvent):
    global in_sis
    data = event.data

    # INICIO DEL SISTEMA
    if data == 'q':
        if not in_sis:
            in_sis = True
            print("hello world")
            send_command('w')
        else:
            print("System already initiated")

    # OBSTÁCULO A LA DERECHA (Arduino mandó 'r')
    elif data == 'r':
        print("RIGHT obstacle event")
        send_command('e')   # respuesta a Arduino

    # OBSTÁCULO A LA IZQUIERDA (Arduino mandó 'l')
    elif data == 'l':
        print("LEFT obstacle event")
        send_command('t')   # respuesta a Arduino
