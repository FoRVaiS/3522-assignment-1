import pygame


class UI:
    def __init__(self) -> None:
        self.font_header = pygame.font.Font('freesansbold.ttf', 26)
        self.font_regular = pygame.font.Font('freesansbold.ttf', 20)

    def render_score(self, surface: pygame.Surface, x: int, y: int, score: int) -> None:
        text = self.font_regular.render(f'Score: {score}', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.x = x
        textRect.y = y
        surface.blit(text, textRect)

    def render_game_over(self, surface: pygame.Surface, x: int, y: int) -> None:
        text = self.font_header.render('Game Over | Press [R] to retry', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (x, y)
        surface.blit(text, textRect)
