from GameObject import Food
import random


class EventSystem:
    def __init__(self, world, state) -> None:
        self.world = world
        self.state = state

    def on_eat_food(self, game_object) -> None:
        self.world.remove_game_object(game_object)

        x = random.randrange(0, 400, 32)

        # Spawn more food
        food = Food(x, x)
        self.world.add_game_object(food)

        # Update the player's score
        self.state.set_state("score", int(self.state.get_state("score")) + 1)
