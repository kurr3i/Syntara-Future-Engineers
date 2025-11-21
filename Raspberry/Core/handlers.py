from .serial_communication import send_command
from .events import SerialDataReceivedEvent, HuskyLensObjectDetectedEvent

from .event_bus import event_publisher 
in_sis = False 


counters = {
    "r": 0,
    "l": 0,
    "f": 0,
    "p": 0,
    "ñ": 0
}

# Condiciones de estabilidad
STABILITY = {
    "r": 3,
    "l": 3,
    "f": 3,
    "p": 5,
    "ñ": 5
}

# Estado de secuencia en ejecución
current_sequence = None  # None, "right_far", "front_close", etc.

def handle_serial_data(event: SerialDataReceivedEvent):
    global in_sis, counters, current_sequence
    data = event.data

    # --- INICIO DEL SISTEMA ---
    if data == 'q':  
        if not in_sis:
            in_sis = True
            print("[SYSTEM] Started! Sending 'w' to Arduino")
            send_command('w')  # Arduino comienza a moverse
        else:
            print("[SYSTEM] Already started")
        return  # ignorar otras secuencias mientras inicia

    # --- Reset de contadores de otras letras ---
    for key in counters.keys():
        if key != data:
            counters[key] = 0

    # --- Contadores ---
    if data in counters:
        counters[data] += 1
    else:
        return  # letra desconocida, ignorar

    # --- Prioridad máxima: frente ---
    if data == "f" and counters["f"] >= STABILITY["f"]:
        if current_sequence != "front_close":
            current_sequence = "front_close"
            print("[ACTION] Front obstacle! Stopping")
            send_command("u")
            current_sequence = None
            for k in counters.keys():
                counters[k] = 0
        return

    # --- Secuencias normales (solo si no hay evento crítico) ---
    if current_sequence is None:
        # Evitar obstáculos laterales
        if data == "r" and counters["r"] >= STABILITY["r"]:
            current_sequence = "right_close"
            print("[ACTION] Obstacle right! Avoiding")
            send_command("e")
            current_sequence = None
            for k in counters.keys():
                counters[k] = 0
            return

        if data == "l" and counters["l"] >= STABILITY["l"]:
            current_sequence = "left_close"
            print("[ACTION] Obstacle left! Avoiding")
            send_command("t")
            current_sequence = None
            for k in counters.keys():
                counters[k] = 0
            return

        # Pared lejos → acercarse
        if data == "p" and counters["p"] >= STABILITY["p"]:
            current_sequence = "right_far"
            print("[ACTION] Moving right to approach wall")
            send_command("v")
            current_sequence = None
            for k in counters.keys():
                counters[k] = 0
            return

        if data == "ñ" and counters["ñ"] >= STABILITY["ñ"]:
            current_sequence = "left_far"
            print("[ACTION] Moving left to approach wall")
            send_command("ñ")
            current_sequence = None
            for k in counters.keys():
                counters[k] = 0
            return



def execute_left_far_sequence():
    print("[ACTION] Moving left to approach wall")
    send_command("ñ")  # ejemplo de comando
    

def execute_front_close_sequence():
    print("[ACTION] Front obstacle! Stopping")
    send_command("u")  # prioridad máxima
    

def execute_right_near_sequence():
    print("[ACTION] Obstacle right! Taking evasive action")
    send_command("e")  
    

def execute_left_near_sequence():
    print("[ACTION] Obstacle left! Taking evasive action")
    send_command("t")  
    


def handle_huskylens_detection(event: HuskyLensObjectDetectedEvent):
    oid = event.object_id

    payload = f"{oid},{event.x},{event.y},{event.width},{event.height}\n"

    # ID 1 → letra 'A'
    # ID 2 → letra 'B'
    if oid == 1:
        print("[Handler] Detected ID 1 → sending 'A' + coords")
        send_command("A" + payload)
    
    elif oid == 2:
        print("[Handler] Detected ID 2 → sending 'B' + coords")
        send_command("B" + payload)
