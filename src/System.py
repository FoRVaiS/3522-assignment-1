from typing import List, Type
from abc import ABC

import pygame

from GameObject import GameObject
from Component import Component, RenderComponent, PositionComponent


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
