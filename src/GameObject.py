from typing import Dict, Type, TypeVar, Optional, List
from abc import ABC

# Types
from Component import Component, TransformComponent, RenderComponent, AiFollowComponent

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
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.components: Dict[Type[Component], Component] = {}

        self.transform_component = TransformComponent(x, y, width, height)
        self.render_component = RenderComponent(width, height)

        self.add_component(self.transform_component)
        self.add_component(self.render_component)


class Snake(Entity):
    def __init__(self, length: int) -> None:
        super().__init__(0, 0, 32, 32)

        self._segments = [self]
        self._tail = self

        for i in range(length):
            self.add_segment()

    def add_segment(self) -> Entity:
        x, y = self._tail.transform_component.x, self._tail.transform_component.y
        width, height = self._tail.transform_component.width, self._tail.transform_component.height

        segment = Entity(x, y, width, height)
        segment.add_component(AiFollowComponent(self._tail))

        self._segments.append(segment)
        self._tail = segment

        return segment

    def get_segments(self) -> List[Entity]:
        return self._segments
