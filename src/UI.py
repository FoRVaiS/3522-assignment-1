import pygame


class UI:
    def __init__(self) -> None:
        """
        Create a new UI.

        The UI is responsible for rendering text on the screen.
        """
        self._font_header = pygame.font.Font('freesansbold.ttf', 26)
        self._font_regular = pygame.font.Font('freesansbold.ttf', 20)

    def render_score(self, surface: pygame.Surface, x: int, y: int, score: int) -> None:
        """
        Render the score on the screen.

        :param surface: The surface to render the score on.
        :param x: The x position of the score.
        :param y: The y position of the score.
        :param score: The score to render.
        """
        text = self._font_regular.render(f'Score: {score}', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.x = x
        textRect.y = y
        surface.blit(text, textRect)

    def render_game_over(self, surface: pygame.Surface, x: int, y: int) -> None:
        """
        Render the game over text on the screen.

        :param surface: The surface to render the game over text on.
        :param x: The x position of the game over text.
        :param y: The y position of the game over text.
        """
        text = self._font_header.render('Game Over | Press [R] to retry', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (x, y)
        surface.blit(text, textRect)
