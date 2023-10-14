"""
This module is responsible for containing the window class and any window management utilities.
"""
from typing import Tuple, List, Callable
import pygame


class Window:
    """
    The window class is responsible for managing the game window.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))

        self.events: List[Tuple[int, Callable[[pygame.event.Event], None]]] = []

    def registerEvent(self, pygameEvent: int, callback: Callable[[pygame.event.Event], None]) -> None:
        """
        Register a pygame event.
        """
        self.events.append((pygameEvent, callback))

    def update(self) -> None:
        """
        Update the game window.
        """
        # Handle pygame events
        for event in pygame.event.get():
            for pygameEvent, callback in self.events:
                if event.type == pygameEvent:
                    callback(event)

        # Update the game window
        pygame.display.update()
