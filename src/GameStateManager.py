class GameStateManager():
    def __init__(self) -> None:
        """
        Create a new GameStateManager.

        The GameStateManager is responsible for tracking state of the game.
        """
        self._state = {}

    def set_state(self, state_name: str, value) -> None:
        """
        Set a state value.

        :param state_name: The name of the state to set.
        :param value: The value to set the state to.
        """
        self._state[state_name] = value

    def has_state(self, state_name: str) -> bool:
        """
        Check if a state exists.

        :param state_name: The name of the state to check.
        :return: True if the state exists, otherwise False.
        """
        return state_name in self._state

    def get_state(self, state_name: str):
        """
        Get a state value.

        :param state_name: The name of the state to get.
        :return: The value of the state.
        """
        return self._state.get(state_name)
