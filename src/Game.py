"""
This module is responsible for containing the game loop, game states, and any other game management utilies
"""
import datetime as datetime
from datetime import timezone
from math import floor

import pygame

from GameStateManager import GameStateManager
from PygameEventManager import PygameEventManager
from Window import Window
from World import World
from Grid import Grid
from UI import UI
from System import RenderingSystem, KeyboardInputSystem, MovementSystem, AiFollowSystem, CollisionSystem, FoodSpawnSystem, GridObjectSystem
from Component import BoxSpriteComponent, CircleSpriteComponent, TransformComponent, PhysicsBodyComponent, PlayerControllerComponent, AiFollowComponent


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

    def __init__(self, width: int, height: int, tickrate: int) -> None:
        """
        Create a new game.

        :param width: The width of the game window.
        :param height: The height of the game window.
        :param tickrate: The number of times to update the game per second.
        """
        self._width = width
        self._height = height
        self._tickrate = tickrate

        pixels_to_unit = 32

        pygame.init()
        self._pg_event_manager = PygameEventManager()

        self._window = Window(width, height)
        self._pg_event_manager.subscribe(pygame.QUIT, lambda event: self.stop())

        self._state = GameStateManager()
        self._ui = UI()

        grid_x = int((width - (width // pixels_to_unit) * pixels_to_unit) / 2)
        grid_y = int((height - (height // pixels_to_unit) * pixels_to_unit) / 2)
        self._grid = Grid(grid_x, grid_y, width, height, pixels_to_unit)

        self._world = World(self._grid, self._state)
        self._pg_event_manager.subscribe(pygame.KEYDOWN, lambda event: self._world.reset() if event.key == pygame.K_r else None)

        self._food_spawn_system = FoodSpawnSystem(self._grid, self._world, [])
        self._grid_object_system = GridObjectSystem(self._grid, [[TransformComponent]])
        self._rendering_system = RenderingSystem(self._window.get_surface(), [[TransformComponent, BoxSpriteComponent], [TransformComponent, CircleSpriteComponent]])
        self._keyboard_input_system = KeyboardInputSystem(self._pg_event_manager, [[PlayerControllerComponent, PhysicsBodyComponent]])
        self._movement_system = MovementSystem(grid_x, grid_y, pixels_to_unit, [[TransformComponent, PhysicsBodyComponent]])
        self._collisions_system = CollisionSystem([[PhysicsBodyComponent, TransformComponent]])

        self._follow_system = AiFollowSystem([[AiFollowComponent, TransformComponent]])

        self.start()
        self.loop(tickrate)

    def start(self) -> None:
        """
        Start the game.
        """
        self._isRunning = True

    def stop(self) -> None:
        """
        Stop the game.
        """
        self._isRunning = False

    def onTick(self) -> None:
        """
        Update the game every tick.
        """
        objects = self._world.get_game_objects()

        self._grid.clear_all()

        self._grid_object_system.process(objects)
        self._food_spawn_system.process(objects)
        self._movement_system.process(objects)
        self._follow_system.process(objects)
        self._collisions_system.process(objects)

        surface = self._window.get_surface()
        game_status: str = self._state.get_state("status")

        if game_status == "in-game":
            self._rendering_system.process(objects)
            self._ui.render_score(surface, 8, int((self._grid.get_cell_size() - 20) / 2 + self._grid.get_y_offset()), int(self._state.get_state("score") or 0))
        elif game_status == "game-over":
            self._ui.render_game_over(surface, int(self._width / 2), int(self._height / 2))

        self._window.update()

    def onImmediateUpdate(self) -> None:
        """
        Run an update immediately.
        """
        objects = self._world.get_game_objects()

        self._keyboard_input_system.process(objects)
        self._pg_event_manager.update()

    def loop(self, tickrate: int) -> None:
        """
        Initialize the game loop and performs an update N-tickrate times every second.

        :param tickrate: The number of times to update the game per second.
        """
        ms_per_tick = 1000 / tickrate
        last_time_ms = current_milli_time()
        delta_time = 0.0

        self.onTick()

        while (self._isRunning):
            self.onImmediateUpdate()

            now = current_milli_time()
            delta_time = now - last_time_ms

            if (delta_time >= ms_per_tick):
                self.onTick()
                last_time_ms += ms_per_tick
