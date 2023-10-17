from typing import List

from Component import PlayerControllerComponent, PhysicsBodyComponent
from GameObject import GameObject, Snake, Food
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

        self.player = Snake(length=0)
        self.player.add_component(PlayerControllerComponent())
        self.add_game_object(self.player)

        player_phys_body = self.player.get_component(PhysicsBodyComponent)

        if player_phys_body:
            player_phys_body.add_collision_handler(Food, lambda food: event_system.on_eat_food(self.player, food))
            player_phys_body.add_collision_handler(Snake, lambda snake: event_system.on_eat_snake(self.player))

        self.add_game_object(Food(128, 128))

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
