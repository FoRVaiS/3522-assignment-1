from typing import List

from Component import PlayerControllerComponent, PhysicsBodyComponent
from GameObject import GameObject, Snake, Food, Wall
from EventSystem import EventSystem
from GameStateManager import GameStateManager
from Grid import Grid


class World:
    def __init__(self, grid: Grid, state: GameStateManager) -> None:
        self.game_objects: List[GameObject] = []
        self.state = state
        self.grid = grid

        self.start()

    def start(self):
        self.reset_state()
        event_system = EventSystem(self, self.grid, self.state)

        cell_size = self.grid.get_cell_size()

        # Spawn a player
        self.player = Snake(cell_size, cell_size, length=0)
        self.player.add_component(PlayerControllerComponent())
        self.add_game_object(self.player)

        player_phys_body = self.player.get_component(PhysicsBodyComponent)

        if player_phys_body:
            player_phys_body.add_collision_handler(Food, lambda food: event_system.on_eat_food(self.player, food))
            player_phys_body.add_collision_handler(Snake, lambda snake: self.defeat())
            player_phys_body.add_collision_handler(Wall, lambda wall: self.defeat())

        # Spawn walls around the perimeter of the grid
        for x in range(self.grid.get_num_cols()):
            min_y = 0
            max_y = self.grid.get_num_rows() - 1

            top_wall = Wall(x * cell_size, min_y, cell_size, cell_size)
            bottom_wall = Wall(x * cell_size, max_y * cell_size, cell_size, cell_size)

            self.add_game_object(top_wall)
            self.add_game_object(bottom_wall)

        for y in range(1, self.grid.get_num_rows() - 1):
            min_x = 0
            max_x = self.grid.get_num_cols() - 1

            left_wall = Wall(min_x, y * cell_size, cell_size, cell_size)
            right_wall = Wall(max_x * cell_size, y * cell_size, cell_size, cell_size)

            self.add_game_object(left_wall)
            self.add_game_object(right_wall)

    def defeat(self):
        self.game_objects.clear()
        self.state.set_state("status", "game-over")

    def reset(self):
        self.game_objects.clear()
        self.start()

    def reset_state(self):
        self.state.set_state("score", 0)
        self.state.set_state("status", "in-game")

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a game object to the world.
        """
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove an game object from the world.
        """
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)

    def get_game_objects(self) -> List[GameObject]:
        """
        Get all game objects in the world.
        """
        return self.game_objects
