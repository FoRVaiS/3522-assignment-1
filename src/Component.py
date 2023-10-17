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
        self._width = width
        self._height = height
        self._color = color
        self._outline = outline

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a square on the screen at the specified position.

        :param screen: The screen to draw the square on.
        :param x: The x position of the square.
        :param y: The y position of the square.
        """
        square_rect = pygame.Rect(x, y, self._width, self._height)

        # Draw the square on the screen with the specified color
        pygame.draw.rect(screen, self._color, square_rect, self._outline)


class CircleSpriteComponent(Component):
    def __init__(self, radius: int, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Create a new CircleSpriteComponent.

        :param radius: The radius of the circle.
        :param color: The color of the circle.
        """
        self._radius = radius
        self._color = color

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a circle on the screen at the specified position.

        :param screen: The screen to draw the circle on.
        :param x: The x position of the circle.
        :param y: The y position of the circle.
        """
        pygame.draw.circle(screen, self._color, (x + self._radius * 2, y + self._radius * 2), radius=self._radius)


class TransformComponent(Component):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create a new TransformComponent.

        :param x: The x position of the game object.
        :param y: The y position of the game object.
        :param width: The width of the game object.
        :param height: The height of the game object.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self) -> int:
        """
        Get the x position.

        :return: The x position.
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """
        Set the x position.

        :param value: The new x position.
        """
        self._x = value

    @property
    def y(self) -> int:
        """
        Get the y position.

        :return: The y position.
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """
        Set the y position.

        :param value: The new y position.
        """
        self._y = value

    @property
    def width(self) -> int:
        """
        Get the width.

        :return: The width.
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """
        Set the width.

        :param value: The new width.
        """
        self._width = value

    @property
    def height(self) -> int:
        """
        Get the height.

        :return: The height.
        """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """
        Set the height.

        :param value: The new height.
        """
        self._height = value


class PhysicsBodyComponent(Component):
    def __init__(self) -> None:
        """
        Create a new PhysicsBodyComponent.
        """
        self._vel_x = 0
        self._vel_y = 0
        self._x_dir = 0
        self._y_dir = 0

        self._handlers = {}

    @property
    def vel_x(self) -> int:
        """
        Get the velocity in the x-direction.

        :return: The velocity in the x-direction.
        """
        return self._vel_x

    @vel_x.setter
    def vel_x(self, value: int) -> None:
        """
        Set the velocity in the x-direction.

        :param value: The new velocity in the x-direction.
        """
        self._vel_x = value

    @property
    def vel_y(self) -> int:
        """
        Get the velocity in the y-direction.

        :return: The velocity in the y-direction.
        """
        return self._vel_y

    @vel_y.setter
    def vel_y(self, value: int) -> None:
        """
        Set the velocity in the y-direction.

        :param value: The new velocity in the y-direction.
        """
        self._vel_y = value

    @property
    def x_dir(self) -> int:
        """
        Get the x-direction.

        :return: The x-direction.
        """
        return self._x_dir

    @x_dir.setter
    def x_dir(self, value: int) -> None:
        """
        Set the x-direction.

        :param value: The new x-direction.
        """
        self._x_dir = value

    @property
    def y_dir(self) -> int:
        """
        Get the y-direction.

        :return: The y-direction.
        """
        return self._y_dir

    @y_dir.setter
    def y_dir(self, value: int) -> None:
        """
        Set the y-direction.

        :param value: The new y-direction.
        """
        self._y_dir = value

    def add_collision_handler(self, game_object_type, handler) -> None:
        """
        Add a collision handler for a specific game object type.

        :param game_object_type: The type of game object to handle collisions for.
        :param handler: The collision handler.
        """
        if self._handlers.get(game_object_type) is None:
            self._handlers[game_object_type] = []
        self._handlers[game_object_type].append(handler)

    def on_collision(self, game_object) -> None:
        if self._handlers.get(type(game_object)) is not None:
            for handler in self._handlers[type(game_object)]:
                handler(game_object)


class PlayerControllerComponent(Component):
    pass


class AiFollowComponent(Component):
    def __init__(self, game_object) -> None:
        """
        Create a new AiFollowComponent.

        :param game_object: The game object to follow.
        """
        self._target = game_object

    def get_target(self):
        """
        Get the game object to follow.

        :return: The game object to follow.
        """
        return self._target
