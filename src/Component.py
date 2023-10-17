from typing import Tuple
from abc import ABC

import pygame


class Component(ABC):
    pass


class BoxSpriteComponent(Component):
    def __init__(self, width: int, height: int, color: Tuple[int, int, int] = (255, 255, 255), outline: bool = False) -> None:
        """
        Create a new BoxSpriteComponent.

        :param width: The width of the square.
        :param height: The height of the square.
        :param color: The color of the square.
        :param outline: Whether or not to draw an outline around the square.
        """
        self.width = width
        self.height = height
        self.color = color
        self.outline = outline

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a square on the screen at the specified position.

        :param screen: The screen to draw the square on.
        :param x: The x position of the square.
        :param y: The y position of the square.
        """
        square_rect = pygame.Rect(x, y, self.width, self.height)

        # Draw the square on the screen with the specified color
        pygame.draw.rect(screen, self.color, square_rect, self.outline)


class CircleSpriteComponent(Component):
    def __init__(self, radius: int, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Create a new CircleSpriteComponent.

        :param radius: The radius of the circle.
        :param color: The color of the circle.
        """
        self.radius = radius
        self.color = color

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a circle on the screen at the specified position.

        :param screen: The screen to draw the circle on.
        :param x: The x position of the circle.
        :param y: The y position of the circle.
        """
        pygame.draw.circle(screen, self.color, (x + self.radius * 2, y + self.radius * 2), radius=self.radius)


class TransformComponent(Component):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create a new TransformComponent.

        :param x: The x position of the game object.
        :param y: The y position of the game object.
        :param width: The width of the game object.
        :param height: The height of the game object.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class PhysicsBodyComponent(Component):
    def __init__(self) -> None:
        """
        Create a new PhysicsBodyComponent.
        """
        self.vel_x = 0
        self.vel_y = 0
        self.x_dir = 0
        self.y_dir = 0

        self.handlers = {}

    def add_collision_handler(self, game_object_type, handler) -> None:
        """
        Add a collision handler for a specific game object type.

        :param game_object_type: The type of game object to handle collisions for.
        :param handler: The collision handler.
        """
        if self.handlers.get(game_object_type) is None:
            self.handlers[game_object_type] = []
        self.handlers[game_object_type].append(handler)

    def on_collision(self, game_object) -> None:
        if self.handlers.get(type(game_object)) is not None:
            for handler in self.handlers[type(game_object)]:
                handler(game_object)


class PlayerControllerComponent(Component):
    pass


class AiFollowComponent(Component):
    def __init__(self, game_object) -> None:
        """
        Create a new AiFollowComponent.

        :param game_object: The game object to follow.
        """
        self.target = game_object

    def get_target(self):
        """
        Get the game object to follow.

        :return: The game object to follow.
        """
        return self.target
