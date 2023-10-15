"""
This module is responsible for containing the game loop, game states, and any other game management utilies
"""
import datetime as datetime
from datetime import timezone
from math import floor

import pygame

from Window import Window


def current_milli_time() -> float:
    """
    Get the current time in milliseconds.

    :return: The current time in milliseconds.
    """
    return floor(datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp() * 1000)


class Game:
    """
    The game class is responsible for managing the game loop and updating the game state.
    """

    def __init__(self, width: int, height: int, tickrate: int):
        self.width = width
        self.height = height
        self.tickrate = tickrate

        pygame.init()
        self.window = Window(width, height)
        self.window.registerEvent(pygame.QUIT, lambda event: self.stop())

        self.start()
        self.loop(tickrate)

    def start(self) -> None:
        """
        Start the game.
        """
        self.isRunning = True

    def stop(self) -> None:
        """
        Stop the game.
        """
        self.isRunning = False

    def onTick(self) -> None:
        """
        Update the game every tick.
        """
        self.window.update()

    def onImmediateUpdate(self) -> None:
        """
        Run an update immediately.
        """
        self.window.process_window_events()


    def loop(self, tickrate: int) -> None:
        """
        Initialize the game loop and performs an update N-tickrate times every second.

        :param tickrate: The number of times to update the game per second.
        """
        ms_per_tick = 1000 / tickrate
        last_time_ms = current_milli_time()
        delta_time = 0.0

        self.onTick()

        while (self.isRunning):
            self.onImmediateUpdate()

            now = current_milli_time()
            delta_time = now - last_time_ms

            if (delta_time >= ms_per_tick):
                self.onTick()
                last_time_ms += ms_per_tick
