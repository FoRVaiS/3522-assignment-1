from typing import List, Type, Dict
from abc import ABC

import pygame

from PygameEventManager import PygameEventManager
from GameObject import GameObject
from Component import Component, RenderComponent, TransformComponent, PlayerControllerComponent, AiFollowComponent


class System(ABC):
    def __init__(self, component_types: List[Type[Component]]):
        self.component_types = component_types

    def _filter_objects(self, game_objects: List[GameObject]) -> List[GameObject]:
        filtered_entities = []

        for entity in game_objects:
            if all(isinstance(entity.get_component(component_type), component_type) for component_type in self.component_types):
                filtered_entities.append(entity)

        return filtered_entities


class RenderingSystem(System):
    def __init__(self, screen: pygame.Surface, component_types: List[Type[Component]]):
        super().__init__(component_types)
        self.screen = screen

    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            transform_component = entity.get_component(TransformComponent)
            render_component = entity.get_component(RenderComponent)

            if transform_component and render_component:
                x, y = transform_component.x, transform_component.y
                render_component.draw(self.screen, x, y)


class MovementSystem(System):
    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            transform_component = entity.get_component(TransformComponent)

            if transform_component:
                transform_component.x += transform_component.vel_x * transform_component.width
                transform_component.y += transform_component.vel_y * transform_component.height


class AiFollowSystem(System):
    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            ai_component = entity.get_component(AiFollowComponent)

            if ai_component and ai_component.target:
                follower_transform_component = entity.get_component(TransformComponent)
                target_transform_component = ai_component.target.get_component(TransformComponent)

                if follower_transform_component and target_transform_component:
                    # Get the follower coordinates
                    follower_x, follower_y = follower_transform_component.x, follower_transform_component.y

                    # Get the target coordinates
                    target_x, target_y = target_transform_component.x, target_transform_component.y

                    # Calculate the x_dir and y_dir difference between the follower and target
                    x_dir = max(min(target_x - follower_x, 1), -1)
                    y_dir = max(min(target_y - follower_y, 1), -1)

                    follower_transform_component.vel_x = x_dir
                    follower_transform_component.vel_y = y_dir


class KeyboardInputSystem(System):
    def __init__(self, event_manager: PygameEventManager, component_types: List[Type[Component]]):
        super().__init__(component_types)

        # Tracks all keys that are currently pressed
        self.keyMap: Dict[int, bool] = {}

        event_manager.subscribe(pygame.KEYDOWN, self.on_keydown)
        event_manager.subscribe(pygame.KEYUP, self.on_keyup)

    def on_keydown(self, event: pygame.event.Event) -> None:
        """
        Handle keydown events.
        """
        keyCode = event.key

        self.keyMap[keyCode] = True

    def on_keyup(self, event: pygame.event.Event) -> None:
        """
        Handle keyup events.
        """
        keyCode = event.key

        del self.keyMap[keyCode]

    def process(self, game_objects: List[GameObject]) -> None:
        for keyCode in self.keyMap.keys():
            for entity in self._filter_objects(game_objects):
                controller = entity.get_component(PlayerControllerComponent)
                transform_component = entity.get_component(TransformComponent)

                if controller and transform_component:
                    x_dir, y_dir = 0, 0

                    if keyCode == pygame.K_w:
                        y_dir += -1

                    if keyCode == pygame.K_s:
                        y_dir += 1

                    if keyCode == pygame.K_a:
                        x_dir += -1

                    if keyCode == pygame.K_d:
                        x_dir += 1

                    # Prevent the player from turning back on itself
                    if x_dir != -transform_component.vel_x or y_dir != -transform_component.vel_y:
                        transform_component.vel_x = x_dir
                        transform_component.vel_y = y_dir
