from abc import ABC

import pygame


class Component(ABC):
    pass


class RenderComponent(Component):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        square_rect = pygame.Rect(x, y, self.width, self.height)

        # Draw the square on the screen with the specified color
        pygame.draw.rect(screen, (255, 255, 255), square_rect)


class PositionComponent(Component):
    def __init__(self, x: int, y: int) -> None:
        self.set_position(x, y)

    def move(self, x: int, y: int) -> None:
        self.x += x
        self.y += y

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> tuple[int, int]:
        return (self.x, self.y)


class PlayerControllerComponent(Component):
    def __init__(self, velocity: int):
        self._velocity = velocity

    def get_velocity(self) -> int:
        return self._velocity
