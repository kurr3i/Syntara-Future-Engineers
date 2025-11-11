import time
from gpiozero import Button

PIN_BOTON = 17
boton = Button(PIN_BOTON)

def imprimir_mensaje():
    """Función que se llama cuando se presiona el botón."""
    print("¡Hello World!")
    
boton.when_pressed = imprimir_mensaje

print(f"Programa iniciado. Esperando la pulsación en el pin GPIO {PIN_BOTON}...")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")