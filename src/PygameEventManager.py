from typing import List, Dict, Callable

import pygame
from pygame.event import Event


class PygameEventManager:
    def __init__(self) -> None:
        """
        Create a new PygameEventManager.

        The PygameEventManager is responsible for managing events by offering
        an observer api.
        """
        self.event_handlers: Dict[int, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_type: int, handler: Callable[[Event], None]) -> None:
        """
        Subscribe a handler to a specific event type.

        :param event_type: The type of event to subscribe to.
        :param handler: The handler to subscribe.
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def unsubscribe(self, event_type: int, handler: Callable[[Event], None]) -> None:
        """
        Unsubscribe a handler from a specific event type.

        :param event_type: The type of event to unsubscribe from.
        :param handler: The handler to unsubscribe.
        """
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)

    def notify(self, event_type: int, event: Event) -> None:
        """
        Notify all subscribed handlers when an event of a specific type occurs.

        :param event_type: The type of event to notify handlers for.
        :param event: The event to notify handlers with.
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                handler(event)

    def update(self) -> None:
        """
        Update the event manager with the latest events.
        """
        for event in pygame.event.get():
            self.notify(event.type, event)
