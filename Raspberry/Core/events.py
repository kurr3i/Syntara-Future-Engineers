from typing import Optional
from dataclasses import dataclass

class Event:
    pass

@dataclass
class StartEvent(Event):
    pass

@dataclass
class SerialDataReceivedEvent(Event):
    data: str 

@dataclass
class HuskyLensObjectDetectedEvent(Event):
    object_id: int
    x: int
    y: int
    width: int
    height: int
