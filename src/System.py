from typing import List, Type, Dict
from abc import ABC
import random

import pygame

from PygameEventManager import PygameEventManager
from GameObject import GameObject, Food
from Component import Component, BoxSpriteComponent, CircleSpriteComponent, TransformComponent, PhysicsBodyComponent, PlayerControllerComponent, AiFollowComponent
from Grid import Grid
from World import World


class System(ABC):
    def __init__(self, component_lists: List[List[Type[Component]]]):
        self.component_lists = component_lists

    def _filter_objects(self, game_objects: List[GameObject]) -> List[GameObject]:
        filtered_entities = []

        for entity in game_objects:
            for component_list in self.component_lists:
                if all(isinstance(entity.get_component(component), component) for component in component_list):
                    filtered_entities.append(entity)

        return filtered_entities


class RenderingSystem(System):
    def __init__(self, screen: pygame.Surface, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)
        self.screen = screen

    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            transform_component = entity.get_component(TransformComponent)
            render_component = entity.get_component(BoxSpriteComponent) or entity.get_component(CircleSpriteComponent)

            if transform_component and render_component:
                x, y = transform_component.x, transform_component.y
                render_component.draw(self.screen, x, y)


class MovementSystem(System):
    def __init__(self, x_offset: int, y_offset: int, scale_factor: int, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.scale_factor = scale_factor

    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            transform_component = entity.get_component(TransformComponent)
            physics_body_component = entity.get_component(PhysicsBodyComponent)

            if transform_component and physics_body_component:
                current_cell_x = int(transform_component.x // self.scale_factor)
                current_cell_y = int(transform_component.y // self.scale_factor)

                next_cell_x = current_cell_x + physics_body_component.x_dir
                next_cell_y = current_cell_y + physics_body_component.y_dir

                transform_component.x = next_cell_x * self.scale_factor + self.x_offset
                transform_component.y = next_cell_y * self.scale_factor + self.y_offset


class AiFollowSystem(System):
    def process(self, game_objects: List[GameObject]) -> None:
        for entity in self._filter_objects(game_objects):
            ai_component = entity.get_component(AiFollowComponent)

            if ai_component and ai_component.target:
                follower_physics_body_component = entity.get_component(PhysicsBodyComponent)
                follower_transform_component = entity.get_component(TransformComponent)
                target_transform_component = ai_component.get_target().get_component(TransformComponent)

                if follower_transform_component and target_transform_component and follower_physics_body_component:
                    # Get the follower coordinates
                    follower_x, follower_y = follower_transform_component.x, follower_transform_component.y

                    # Get the target coordinates
                    target_x, target_y = target_transform_component.x, target_transform_component.y

                    # Calculate the x_dir and y_dir difference between the follower and target
                    x_dir = max(min(target_x - follower_x, 1), -1)
                    y_dir = max(min(target_y - follower_y, 1), -1)

                    follower_physics_body_component.x_dir = x_dir
                    follower_physics_body_component.y_dir = y_dir


class KeyboardInputSystem(System):
    def __init__(self, event_manager: PygameEventManager, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)

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
                physics_body_component = entity.get_component(PhysicsBodyComponent)

                if controller and physics_body_component:
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
                    if x_dir != -physics_body_component.x_dir or y_dir != -physics_body_component.y_dir:
                        physics_body_component.x_dir = x_dir
                        physics_body_component.y_dir = y_dir


class FoodSpawnSystem(System):
    def __init__(self, grid: Grid, world: World, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)
        self.grid = grid
        self.world = world

    def process(self, game_objects: List[GameObject]) -> None:
        still_has_food = False

        for entity in game_objects:
            if isinstance(entity, Food):
                still_has_food = True
                break

        if not still_has_food:
            rows = self.grid.get_num_rows()
            columns = self.grid.get_num_cols()
            cell_size = self.grid.get_cell_size()
            grid_x, grid_y = self.grid.get_x_offset(), self.grid.get_y_offset()
            grid = self.grid.get_grid()

            empty_cells = [
                (x, y)
                for x in range(columns)
                for y in range(rows)
                if grid[x][y] is None
            ]

            # Pick a random empty cell
            x, y = random.choice(empty_cells)

            # Spawn food
            food = Food(x * cell_size + grid_x, y * cell_size + grid_y)
            self.world.add_game_object(food)


class GridObjectSystem(System):
    def __init__(self, grid: Grid, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)
        self.grid = grid

    def process(self, game_objects: List[GameObject]):
        for entity in self._filter_objects(game_objects):
            transform_component = entity.get_component(TransformComponent)

            if transform_component:
                x, y = transform_component.x, transform_component.y
                cell_size = self.grid.get_cell_size()

                cell_x = int(x // cell_size)
                cell_y = int(y // cell_size)

                self.grid.add_cell(cell_x, cell_y, entity)


class CollisionSystem(System):
    def __init__(self, component_lists: List[List[Type[Component]]]):
        super().__init__(component_lists)

    def detect_x_collision(self, entTransform: GameObject, otherTransform: GameObject) -> bool:
        entX, entWidth = entTransform.x, entTransform.width
        otherX, otherWidth = otherTransform.x, otherTransform.width

        entLeft = entX
        entRight = entX + entWidth

        otherEntLeft = otherX
        otherEntRight = otherX + otherWidth

        hasLeftIntersection = entLeft <= otherEntLeft and entLeft >= otherEntLeft
        hasRightIntersection = entRight <= otherEntRight and entRight >= otherEntRight

        return hasLeftIntersection or hasRightIntersection

    def detect_y_collision(self, entTransform: TransformComponent, otherTransform: TransformComponent) -> bool:
        entY, entHeight = entTransform.y, entTransform.height
        otherY, otherHeight = otherTransform.y, otherTransform.height

        entTop = entY
        entBottom = entY + entHeight

        otherEntTop = otherY
        otherEntBottom = otherY + otherHeight

        hasTopIntersection = entTop <= otherEntTop and entTop >= otherEntTop
        hasBottomIntersection = entBottom <= otherEntBottom and entBottom >= otherEntBottom

        return hasTopIntersection or hasBottomIntersection

    def partition(self, game_objects: List[GameObject]) -> List[List[GameObject]]:
        filtered_entities = self._filter_objects(game_objects)
        filtered_entities.sort(key=lambda entity: entity.get_component(TransformComponent).x)

        # Partition all possible collisions into their own groups
        collision_groups: List[List[GameObject]] = []
        current_group: List[GameObject] = []

        for entity in filtered_entities:
            if len(current_group) > 0:
                last_entity = current_group[-1]

                entTransform = entity.get_component(TransformComponent)
                otherTransform = last_entity.get_component(TransformComponent)

                if entTransform and otherTransform:
                    if not self.detect_x_collision(entTransform, otherTransform):
                        collision_groups.append(current_group)
                        current_group = []

            current_group.append(entity)

        collision_groups.append(current_group)

        return collision_groups

    def process(self, game_objects: List[GameObject]) -> None:
        """
        Given a list of game objects, we want to partition them into a list of
        potentionally colliding groups (2D List), iterate through each group, and
        check that all possible pairs of entities are actually colliding by
        determining if they are also vertically colliding.

        In our partitioning algorithm, we already check that all entities in a
        group are colliding on the x axis, hence why we only need to check if they
        are colliding on the y axis.

        If a pair is determined to be colliding, we trigger ...?

        Given a set of 4 elements in a partition group: [0, 1, 2, 3], all possible
        combinations are:
        - [0, 1]
        - [0, 2]
        - [0, 3]
        - [1, 2]
        - [1, 3]
        - [2, 3]

        We will use two indices, a base index and a sub index.
        The base index will always start from the beginning of the list, but the sub
        index will always begin one more element ahead of the base index.

        - The base index will only increment once the sub index has reached the end
        of the list.
        - The base index will not increment past the penultimate element.
        - The sub index will iterate through the entire list, resetting to one
        index ahead of the base index once the base index has incremented.
        """
        possible_collisions = self.partition(game_objects)

        for x_group in possible_collisions:
            for base_index in range(len(x_group) - 1):
                for sub_index in range(base_index + 1, len(x_group)):
                    # Select a unique pair of entities.
                    ent = x_group[base_index]
                    other = x_group[sub_index]

                    ent_phys_body_component = ent.get_component(PhysicsBodyComponent)
                    other_phys_body_component = other.get_component(PhysicsBodyComponent)

                    ent_transform_component = ent.get_component(TransformComponent)
                    other_transform_component = other.get_component(TransformComponent)

                    # Check if the pair of entities are colliding on the y axis ...
                    if self.detect_y_collision(ent_transform_component, other_transform_component) and ent_phys_body_component and other_phys_body_component:
                        # ... and if they are, trigger their on_collision methods and pass the entity
                        # they collided with.
                        ent_phys_body_component.on_collision(other)
                        other_phys_body_component.on_collision(ent)
