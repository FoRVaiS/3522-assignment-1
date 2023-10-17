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
        """
        Create a new window.

        :param width: The width of the window.
        :param height: The height of the window.
        """
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))

        self.events: List[Tuple[int, Callable[[pygame.event.Event], None]]] = []

    def registerEvent(self, pygameEvent: int, callback: Callable[[pygame.event.Event], None]) -> None:
        """
        Register a pygame event.

        :param pygameEvent: The pygame event to register.
        :param callback: The callback to call when the event occurs.
        """
        self.events.append((pygameEvent, callback))

    def update(self) -> None:
        """
        Update the game window.
        """
        # Update the game window
        pygame.display.update()

        # Clear the game window
        self.window.fill((0, 0, 0))

    def get_surface(self) -> pygame.Surface:
        """
        Get the surface of the game window.

        :return: The surface of the game window.
        """
        return self.window
