from abc import ABC

import pygame


class Component(ABC):
    pass


class SnakeSpriteComponent(Component):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        square_rect = pygame.Rect(x, y, self.width, self.height)

        # Draw the square on the screen with the specified color
        pygame.draw.rect(screen, (255, 255, 255), square_rect, 1)


class FoodSpriteComponent(Component):
    def __init__(self, radius: int):
        self.radius = radius

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (x + self.radius * 2, y + self.radius * 2), radius=self.radius)


class TransformComponent(Component):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class PhysicsBodyComponent(Component):
    def __init__(self) -> None:
        self.vel_x = 0
        self.vel_y = 0
        self.x_dir = 0
        self.y_dir = 0


class PlayerControllerComponent(Component):
    pass


class AiFollowComponent(Component):
    def __init__(self, game_object) -> None:
        self.target = game_object
