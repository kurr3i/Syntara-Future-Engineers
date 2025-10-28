from typing import Dict, List, Callable, Type
from .events import Event  

Handler = Callable[[Event], None]

class SimpleEventBus:

    def __init__(self):
        self._subscribers: Dict[Type[Event], List[Handler]] = {}

    def subscribe(self, event_type: Type[Event], handler: Handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(handler)
        print(f"-> Suscriptor registrado para evento: {event_type.__name__}")

    def publish(self, event: Event):
        event_type = type(event)
        print(f"\n<<< Evento Publicado: {event_type.__name__} >>>")

        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(event)
        else:
            print("No hay suscriptores para este evento. Evento ignorado.")