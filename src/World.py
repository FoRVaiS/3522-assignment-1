from typing import List

from Component import PlayerControllerComponent, PhysicsBodyComponent
from GameObject import GameObject, Snake, Food, Wall
from EventSystem import EventSystem
from GameStateManager import GameStateManager
from Grid import Grid


class World:
    def __init__(self, grid: Grid, state: GameStateManager) -> None:
        """
        Create a new world.

        The world is responsible for managing all game objects and game state.

        :param grid: The grid to use for the world.
        :param state: The game state to use for the world.
        """
        self._game_objects: List[GameObject] = []
        self._state = state
        self._grid = grid

        self.start()

    def start(self) -> None:
        """
        Initialize all default game objects and game state.
        """
        self.reset_state()
        event_system = EventSystem(self, self._grid, self._state)

        cell_size = self._grid.get_cell_size()

        # Spawn a player
        self._player = Snake(cell_size, cell_size, length=0)
        self._player.add_component(PlayerControllerComponent())
        self.add_game_object(self._player)

        player_phys_body = self._player.get_component(PhysicsBodyComponent)

        if player_phys_body:
            player_phys_body.add_collision_handler(Food, lambda food: event_system.on_eat_food(self._player, food))
            player_phys_body.add_collision_handler(Snake, lambda snake: self.defeat())
            player_phys_body.add_collision_handler(Wall, lambda wall: self.defeat())

        # Spawn walls around the perimeter of the grid
        for x in range(self._grid.get_num_cols()):
            min_y = 0
            max_y = self._grid.get_num_rows() - 1

            top_wall = Wall(x * cell_size, min_y, cell_size, cell_size)
            bottom_wall = Wall(x * cell_size, max_y * cell_size, cell_size, cell_size)

            self.add_game_object(top_wall)
            self.add_game_object(bottom_wall)

        for y in range(1, self._grid.get_num_rows() - 1):
            min_x = 0
            max_x = self._grid.get_num_cols() - 1

            left_wall = Wall(min_x, y * cell_size, cell_size, cell_size)
            right_wall = Wall(max_x * cell_size, y * cell_size, cell_size, cell_size)

            self.add_game_object(left_wall)
            self.add_game_object(right_wall)

    def defeat(self) -> None:
        """
        Trigger the defeated game state.
        """
        self._game_objects.clear()
        self._state.set_state("status", "game-over")

    def reset(self) -> None:
        """
        Reset the game.
        """
        self._game_objects.clear()
        self.start()

    def reset_state(self) -> None:
        """
        Reset the game state.
        """
        self._state.set_state("score", 0)
        self._state.set_state("status", "in-game")

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a game object to the world.

        :param game_object: The game object to add.
        """
        self._game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove an game object from the world.

        :param game_object: The game object to remove.
        """
        if game_object in self._game_objects:
            self._game_objects.remove(game_object)

    def get_game_objects(self) -> List[GameObject]:
        """
        Get all game objects in the world.

        :return: A list of all game objects in the world.
        """
        return self._game_objects
