from typing import List

from Component import PlayerControllerComponent, PhysicsBodyComponent
from GameObject import GameObject, Snake, Food
from EventSystem import EventSystem
from GameStateManager import GameStateManager


class World:
    def __init__(self, state: GameStateManager) -> None:
        self.game_objects: List[GameObject] = []
        self.state = state

        event_system = EventSystem(self)

        self.player = Snake(length=0)
        self.player.add_component(PlayerControllerComponent())
        self.add_game_object(self.player)

        player_phys_body = self.player.get_component(PhysicsBodyComponent)

        if player_phys_body:
            player_phys_body.add_collision_handler(Food, lambda food: event_system.on_eat_food(self.player, food))

        self.food = Food(128, 128)
        self.add_game_object(self.food)

    def reset_state(self):
        self.state.set_state("score", 0)

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
