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
        self.width = width
        self.height = height
        self.tickrate = tickrate

        pixels_to_unit = 32

        pygame.init()
        self.pg_event_manager = PygameEventManager()

        self.window = Window(width, height)
        self.pg_event_manager.subscribe(pygame.QUIT, lambda event: self.stop())

        self.state = GameStateManager()
        self.ui = UI()

        grid_x = int((width - (width // pixels_to_unit) * pixels_to_unit) / 2)
        grid_y = int((height - (height // pixels_to_unit) * pixels_to_unit) / 2)
        self.grid = Grid(grid_x, grid_y, width, height, pixels_to_unit)

        self.world = World(self.grid, self.state)
        self.pg_event_manager.subscribe(pygame.KEYDOWN, lambda event: self.world.reset() if event.key == pygame.K_r else None)

        self.food_spawn_system = FoodSpawnSystem(self.grid, self.world, [])
        self.grid_object_system = GridObjectSystem(self.grid, [[TransformComponent]])
        self.rendering_system = RenderingSystem(self.window.get_surface(), [[TransformComponent, BoxSpriteComponent], [TransformComponent, CircleSpriteComponent]])
        self.keyboard_input_system = KeyboardInputSystem(self.pg_event_manager, [[PlayerControllerComponent, PhysicsBodyComponent]])
        self.movement_system = MovementSystem(grid_x, grid_y, pixels_to_unit, [[TransformComponent, PhysicsBodyComponent]])
        self.collisions_system = CollisionSystem([[PhysicsBodyComponent, TransformComponent]])

        self.follow_system = AiFollowSystem([[AiFollowComponent, TransformComponent]])

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

        self.grid.clear_all()

        self.grid_object_system.process(objects)
        self.food_spawn_system.process(objects)
        self.movement_system.process(objects)
        self.follow_system.process(objects)
        self.collisions_system.process(objects)

        surface = self.window.get_surface()
        game_status: str = self.state.get_state("status")

        if game_status == "in-game":
            self.rendering_system.process(objects)
            self.ui.render_score(surface, 8, int((self.grid.get_cell_size() - 20) / 2 + self.grid.get_y_offset()), int(self.state.get_state("score") or 0))
        elif game_status == "game-over":
            self.ui.render_game_over(surface, int(self.width / 2), int(self.height / 2))

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
