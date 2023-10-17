from typing import Dict, Type, TypeVar, Optional, List
from abc import ABC

# Types
from Component import Component, TransformComponent, PhysicsBodyComponent, AiFollowComponent, BoxSpriteComponent, CircleSpriteComponent

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

        self.transform_component = TransformComponent(x, y, width - 1, height - 1)
        self.add_component(self.transform_component)

        self.physics_body_component = PhysicsBodyComponent()
        self.add_component(self.physics_body_component)


class Snake(Entity):
    def __init__(self, x: int, y: int, length: int) -> None:
        super().__init__(x, y, 31, 31)
        self.sprite_component = BoxSpriteComponent(self.transform_component.width, self.transform_component.height, color=(255, 255, 255), outline=True)
        self.add_component(self.sprite_component)

        self._segments = [self]
        self._tail = self

        for i in range(length):
            self.add_segment()

    def add_segment(self) -> 'Snake':
        x = self._tail.transform_component.x
        y = self._tail.transform_component.y

        segment = Snake(x, y, 0)
        segment.add_component(AiFollowComponent(self._tail))

        self._segments.append(segment)
        self._tail = segment

        return segment

    def get_segments(self) -> List['Snake']:
        return self._segments


class Food(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 32, 32)
        self.sprite_component = CircleSpriteComponent(radius=8, color=(255, 0, 0))
        self.add_component(self.sprite_component)


class Wall(Entity):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.sprite_component = BoxSpriteComponent(self.transform_component.width, self.transform_component.height, color=(50, 50, 50), outline=False)
        self.add_component(self.sprite_component)
