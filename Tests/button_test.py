import RPi.GPIO as GPIO
import time
Buttonpin = 17 

GPIO.setmode(GPIO.BCM)

GPIO.setup(Buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def imprimir_mensaje(channel):
    print("¡Hello World!")

GPIO.add_event_detect(
    Buttonpin, 
    GPIO.FALLING, 
    callback=imprimir_mensaje, 
    bouncetime=200
)


try:
    while True:
        time.sleep(1)

        
except KeyboardInterrupt:

    GPIO.cleanup()
    print("\nPrograma terminado y pines limpiados.")