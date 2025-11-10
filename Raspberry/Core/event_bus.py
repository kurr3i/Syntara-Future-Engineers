from typing import Dict, List, Callable, Type
from .events import Event  

Handler = Callable[[Event], None]

class EventBus:

    def __init__(self):
        self._subscribers: Dict[Type[Event], List[Handler]] = {}

    def subscribe(self, event_type: Type[Event], handler: Handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(handler)
        print(f"Registered subscriber: {event_type.__name__}")

    def publish(self, event: Event):
        event_type = type(event)
        print(f"\n<<< Published event: {event_type.__name__} >>>")

        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(event)
        else:
            print("Error")

event_publisher = EventBus()