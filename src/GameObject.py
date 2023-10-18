from typing import Dict, Type, TypeVar, Optional, List
from abc import ABC

# Types
from Component import Component, TransformComponent, PhysicsBodyComponent, AiFollowComponent, BoxSpriteComponent, CircleSpriteComponent

ComponentType = TypeVar("ComponentType", bound=Component)


class GameObject(ABC):
    def __init__(self) -> None:
        """
        Create a new game object.
        """
        self._components: Dict[Type[Component], Component] = {}

    def add_component(self, component: Component) -> None:
        """
        Add a component to the game object.

        :param component: The component to add.
        """
        self._components[type(component)] = component

    def get_component(self, component: Type[ComponentType]) -> Optional[ComponentType]:
        """
        Get a component from the game object.

        :param component: The type of component to get.
        :return: The component if it exists, otherwise None.
        """
        _component = self._components.get(component)

        # This is a hack to get around the fact that mypy doesn't behave well
        # with this particular generic use-case:
        # Incompatible return value type (got "Component | None", expected
        # "ComponentType | None")
        if _component and isinstance(_component, component):
            return _component

        return None

    def remove_component(self, component: Type[Component]) -> None:
        """
        Remove a component from the game object.

        :param component: The type of component to remove.
        """
        if component in self._components:
            del self._components[component]


class Entity(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create a new entity.

        Every entity, by default, has a transform component and a physics body.

        :param x: The x position of the entity.
        :param y: The y position of the entity.
        :param width: The width of the entity.
        :param height: The height of the entity.
        """
        self._components: Dict[Type[Component], Component] = {}

        self._transform_component = TransformComponent(x, y, width - 1, height - 1)
        self.add_component(self._transform_component)

        self._physics_body_component = PhysicsBodyComponent()
        self.add_component(self._physics_body_component)


class Snake(Entity):
    def __init__(self, x: int, y: int, length: int) -> None:
        """
        Create a new snake.

        :param x: The x position of the snake.
        :param y: The y position of the snake.
        :param length: The default length of the snake.
        """
        super().__init__(x, y, 31, 31)
        self._sprite_component = BoxSpriteComponent(self._transform_component.width, self._transform_component._height, color=(255, 255, 255), outline=True)
        self.add_component(self._sprite_component)

        self._segments = [self]
        self._tail = self

        for i in range(length):
            self.add_segment()

    def add_segment(self) -> 'Snake':
        """
        Add a segment to the snake.

        :return: The new segment.
        """
        x = self._tail._transform_component.x
        y = self._tail._transform_component.y

        segment = Snake(x, y, 0)
        segment.add_component(AiFollowComponent(self._tail))

        self._segments.append(segment)
        self._tail = segment

        return segment

    def get_segments(self) -> List['Snake']:
        """
        Get the segments of the snake.

        :return: The segments of the snake.
        """
        return self._segments


class Food(Entity):
    def __init__(self, x: int, y: int) -> None:
        """
        Create new food.

        :param x: The x position of the food.
        :param y: The y position of the food.
        """
        super().__init__(x, y, 32, 32)
        self._sprite_component = CircleSpriteComponent(radius=8, color=(255, 0, 0))
        self.add_component(self._sprite_component)


class Wall(Entity):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create a new wall.

        :param x: The x position of the wall.
        :param y: The y position of the wall.
        :param width: The width of the wall.
        :param height: The height of the wall.
        """
        super().__init__(x, y, width, height)
        self._sprite_component = BoxSpriteComponent(self._transform_component.width, self._transform_component._height, color=(50, 50, 50), outline=False)
        self.add_component(self._sprite_component)
