import time
from huskylib import HuskyLensLibrary

hl = HuskyLensLibrary("I2C", "", address=0x32)

last_detected = None

def on_id_1(obj):
    print(f">>> EVENTO ID 1: (x={obj.x}, y={obj.y}, w={obj.width}, h={obj.height})")

def on_id_2(obj):
    print(f">>> EVENTO ID 2: (x={obj.x}, y={obj.y}, w={obj.width}, h={obj.height})")

print("Leyendo HuskyLens continuamente...\n")

while True:
    try:
        objects = hl.requestAll()

        if not objects:
            last_detected = None
            continue

        for obj in objects:
            if obj.ID == 1 and last_detected != 1:
                last_detected = 1
                on_id_1(obj)

            elif obj.ID == 2 and last_detected != 2:
                last_detected = 2
                on_id_2(obj)

        time.sleep(0.01)

    except Exception as e:
        print("Error:", e)
        time.sleep(0.05)
