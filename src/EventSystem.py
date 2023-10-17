class EventSystem:
    def __init__(self, world, grid, state) -> None:
        self.world = world
        self.state = state
        self.grid = grid

    def on_eat_food(self, snake, food) -> None:
        self.world.remove_game_object(food)

        # Add a segment to the snake
        segment = snake.add_segment()
        self.world.add_game_object(segment)

        # Update the player's score
        self.state.set_state("score", int(self.state.get_state("score")) + 1)
