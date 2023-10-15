from typing import Dict, Type, TypeVar, Optional
from abc import ABC

# Types
from Component import Component, PositionComponent, RenderComponent

ComponentType = TypeVar("ComponentType", bound=Component)


class GameObject(ABC):
    def __init__(self, x: int, y: int) -> None:
        self.components: Dict[Type[Component], Component] = {}

    def add_component(self, component: Component) -> None:
        self.components[type(component)] = component

    def get_component(self, component: Type[ComponentType]) -> Optional[ComponentType]:
        _component = self.components.get(component)

        # This is a hack to get around the fact that mypy doesn't behave well
        # with this particular generic use-case:
        # Incompatible return value type (got "Component | None", expected
        # "ComponentType | None")
        if _component and isinstance(_component, component):
            return _component

        return None

    def remove_component(self, component: Type[Component]) -> None:
        if component in self.components:
            del self.components[component]


class Entity(GameObject):
    def __init__(self, x: int, y: int) -> None:
        self.components: Dict[Type[Component], Component] = {}

        self.position_component = PositionComponent(x, y)
        self.render_component = RenderComponent(32, 32)

        self.add_component(self.position_component)
        self.add_component(self.render_component)
