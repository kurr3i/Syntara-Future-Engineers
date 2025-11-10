import RPi.GPIO as GPIO
import time
import events #not defined
from event_system import event_publisher #not defined

BUTTON_PIN = 17

def button_callback(channel):
    GPIO.remove_event_detect(channel)
    time.sleep(0.1) 
    event_publisher.publish(events.system_started())
    
def main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("started")
        GPIO.add_event_detect(
            BUTTON_PIN, 
            GPIO.FALLING, 
            callback=button_callback, 
            bouncetime=300
        )
        while True:
            time.sleep(1) 
            
    except KeyboardInterrupt:
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()