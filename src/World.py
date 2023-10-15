from typing import List

from GameObject import GameObject


class World:
    def __init__(self) -> None:
        self.game_objects: List[GameObject] = []

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
