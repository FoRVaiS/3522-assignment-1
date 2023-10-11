"""
This module is responsible for containing the game loop, game states, and any other game management utilies
"""
import datetime as datetime
from datetime import timezone
from math import floor

import pygame

from Window import Window


def current_milli_time():
    """
    Get the current time in milliseconds.

    :return: The current time in milliseconds.
    """
    return floor(datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp() * 1000)


class Game:
    """
    The game class is responsible for managing the game loop and updating the game state.
    """

    def __init__(self, width, height, tickrate):
        self.width = width
        self.height = height
        self.tickrate = tickrate

        pygame.init()
        self.window = Window(width, height)
        self.window.registerEvent(pygame.QUIT, lambda event: self.stop())

        self.start()
        self.loop(tickrate)

    def start(self):
        """
        Start the game.
        """
        self.isRunning = True

    def stop(self):
        """
        Stop the game.
        """
        self.isRunning = False

    def update(self):
        """
        Update the game.
        """
        self.window.update()

    def loop(self, tickrate):
        """
        Initialize the game loop and performs an update N-tickrate times every second.

        :param tickrate: The number of times to update the game per second.
        """
        ms_per_tick = 1000 / tickrate
        last_time_ms = current_milli_time()
        delta_time = 0

        self.update()

        while (self.isRunning):
            now = current_milli_time()
            delta_time = now - last_time_ms

            if (delta_time >= ms_per_tick):
                self.update()
                last_time_ms += ms_per_tick
