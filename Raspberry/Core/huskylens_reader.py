import time
from huskylib import HuskyLensLibrary
from .event_bus import event_publisher
from .events import HuskyLensObjectDetectedEvent

hl = HuskyLensLibrary("I2C", "", address=0x32)

STABILITY = 4
id1_count = 0
id2_count = 0

last_event = None

def huskylens_loop():
    global id1_count, id2_count, last_event

    while True:
        try:
            objects = hl.requestAll()

            if not objects:
                id1_count = 0
                id2_count = 0
                last_event = None
                time.sleep(0.01)
                continue

            saw_id1 = False
            saw_id2 = False
            obj1 = None
            obj2 = None

            for obj in objects:
                if obj.ID == 1:
                    saw_id1 = True
                    obj1 = obj

                elif obj.ID == 2:
                    saw_id2 = True
                    obj2 = obj

            # Actualizar contadores
            if saw_id1:
                id1_count += 1
            else:
                id1_count = 0

            if saw_id2:
                id2_count += 1
            else:
                id2_count = 0

            # ESTABILIDAD ALCANZADA → PUBLICAR EVENTO
            if id1_count >= STABILITY and last_event != 1:
                last_event = 1
                event_publisher.publish(
                    HuskyLensObjectDetectedEvent(
                        object_id=1,
                        x=obj1.x,
                        y=obj1.y,
                        width=obj1.width,
                        height=obj1.height
                    )
                )

            if id2_count >= STABILITY and last_event != 2:
                last_event = 2
                event_publisher.publish(
                    HuskyLensObjectDetectedEvent(
                        object_id=2,
                        x=obj2.x,
                        y=obj2.y,
                        width=obj2.width,
                        height=obj2.height
                    )
                )

            time.sleep(0.01)

        except Exception as e:
            print("HuskyLens ERROR:", e)
            time.sleep(0.05)
