class GameStateManager():
    def __init__(self) -> None:
        self._state = {}

    def set_state(self, state_name: str, value) -> None:
        self._state[state_name] = value

    def has_state(self, state_name: str) -> bool:
        return state_name in self._state

    def get_state(self, state_name: str):
        return self._state.get(state_name)
