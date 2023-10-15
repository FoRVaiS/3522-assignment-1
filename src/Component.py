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
        self.x = x
        self.y = y


class TransformComponent(PositionComponent):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y)
        self.width = width
        self.height = height

        self.vel_x = 0
        self.vel_y = 0


class PlayerControllerComponent(Component):
    pass
