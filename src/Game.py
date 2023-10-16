"""
This module is responsible for containing the game loop, game states, and any other game management utilies
"""
import datetime as datetime
from datetime import timezone
from math import floor

import pygame

from PygameEventManager import PygameEventManager
from Window import Window
from World import World
from System import RenderingSystem, KeyboardInputSystem, MovementSystem, AiFollowSystem
from Component import RenderComponent, TransformComponent, PlayerControllerComponent, AiFollowComponent
from GameObject import Snake


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
        self.pg_event_manager = PygameEventManager()

        self.window = Window(width, height)
        self.pg_event_manager.subscribe(pygame.QUIT, lambda event: self.stop())

        screen = self.window.get_surface()

        self.world = World()

        self.player = Snake(length=2)
        self.player.add_component(PlayerControllerComponent())
        for segment in self.player.get_segments():
            self.world.add_game_object(segment)

        self.rendering_system = RenderingSystem(screen, [TransformComponent, RenderComponent])
        self.keyboard_input_system = KeyboardInputSystem(self.pg_event_manager, [PlayerControllerComponent, TransformComponent])
        self.movement_system = MovementSystem(32, [TransformComponent])
        self.follow_system = AiFollowSystem([AiFollowComponent, TransformComponent])

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
        objects = self.world.get_game_objects()

        self.movement_system.process(objects)
        self.follow_system.process(objects)
        self.rendering_system.process(objects)
        self.window.update()

    def onImmediateUpdate(self) -> None:
        """
        Run an update immediately.
        """
        objects = self.world.get_game_objects()

        self.keyboard_input_system.process(objects)
        self.pg_event_manager.update()

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
