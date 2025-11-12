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
