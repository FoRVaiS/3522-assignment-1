from typing import List, Type, Dict
from abc import ABC

import pygame

from PygameEventManager import PygameEventManager
from GameObject import GameObject
from Component import Component, RenderComponent, PositionComponent, PlayerControllerComponent


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
            position_component = entity.get_component(PositionComponent)
            render_component = entity.get_component(RenderComponent)

            if position_component and render_component:
                x, y = position_component.get_position()
                render_component.draw(self.screen, x, y)


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
                position_component = entity.get_component(PositionComponent)

                if controller and position_component:
                    if keyCode == pygame.K_w:
                        position_component.move(0 * controller.get_velocity(), -1 * controller.get_velocity())

                    if keyCode == pygame.K_s:
                        position_component.move(0 * controller.get_velocity(), 1 * controller.get_velocity())

                    if keyCode == pygame.K_a:
                        position_component.move(-1 * controller.get_velocity(), 0 * controller.get_velocity())

                    if keyCode == pygame.K_d:
                        position_component.move(1 * controller.get_velocity(), 0 * controller.get_velocity())
