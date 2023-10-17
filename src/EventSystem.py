from Grid import Grid
from GameStateManager import GameStateManager
from GameObject import Snake, Food


class EventSystem:
    def __init__(self, world, grid: Grid, state: GameStateManager) -> None:
        """
        The event system is responsible for handling events that occur in the game.

        :param world: The world to handle events for.
        :param grid: The grid to handle events for.
        :param state: The game state to handle events for.
        """
        self.world = world
        self.state = state
        self.grid = grid

    def on_eat_food(self, snake: Snake, food: Food) -> None:
        """
        Handle the event of a snake eating food.

        :param snake: The snake that ate the food.
        :param food: The food that was eaten.
        """
        self.world.remove_game_object(food)

        # Add a segment to the snake
        segment = snake.add_segment()
        self.world.add_game_object(segment)

        # Update the player's score
        self.state.set_state("score", int(self.state.get_state("score")) + 1)
