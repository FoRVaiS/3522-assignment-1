from typing import List

from Component import PlayerControllerComponent, PhysicsBodyComponent
from GameObject import GameObject, Snake, Food
from EventSystem import EventSystem


class World:
    def __init__(self) -> None:
        self.game_objects: List[GameObject] = []

        event_system = EventSystem(self)

        self.player = Snake(length=0)
        self.player.add_component(PlayerControllerComponent())
        for segment in self.player.get_segments():
            self.add_game_object(segment)

        player_phys_body = self.player.get_component(PhysicsBodyComponent)

        if player_phys_body:
            player_phys_body.add_collision_handler(Food, event_system.on_eat_food)

        self.food = Food(128, 128)
        self.add_game_object(self.food)

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
