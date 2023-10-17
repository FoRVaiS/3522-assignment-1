from typing import List, Any, Tuple, Optional

from GameObject import GameObject


class Grid:
    def __init__(self, x: int, y: int, width: int, height: int, size: int):
        """
        Create a new grid.

        :param x: The x offset of the grid.
        :param y: The y offset of the grid.
        :param width: The width of the grid.
        :param height: The height of the grid.
        :param size: The size of a single cell in the grid.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._size = size
        self._grid: List[List[Optional[List[GameObject]]]] = [
            [
                None
                for y in range(height // size)
            ]
            for x in range(width // size)
        ]

    def add_cell(self, x: int, y: int, value: Any) -> None:
        """
        Add a value to a cell in the grid.

        :param x: The x position of the cell.
        :param y: The y position of the cell.
        :param value: The value to add to the cell.
        """
        if x < 0 or x >= self.get_num_cols() or y < 0 or y >= self.get_num_rows():
            raise IndexError("Cell position out of range.")

        if self._grid[x][y] is None:
            self._grid[x][y] = []
        self._grid[x][y].append(value)

    def clear_cell(self, x: int, y: int) -> None:
        """
        Clear a cell in the grid.

        :param x: The x position of the cell.
        :param y: The y position of the cell.
        """
        if self._grid[x][y]:
            self._grid[x][y] = None

    def clear_all(self) -> None:
        """
        Clear all cells in the grid.
        """
        for x in range(self.get_num_cols()):
            for y in range(self.get_num_rows()):
                self.clear_cell(x, y)

    def get_cell(self, x: int, y: int) -> Any:
        """
        Get the value of a cell in the grid.

        :param x: The x position of the cell.
        :param y: The y position of the cell.
        :return: The value of the cell.
        """
        return self._grid[x][y]

    def get_cell_pos(self, x: int, y: int) -> Tuple[int, int]:
        """
        Get the x, y position of a cell in the grid.
        """
        return x * self._size + self._x, y * self._size + self._y

    def get_num_cols(self) -> int:
        """
        Get the number of columns in the grid.

        :return: The number of columns in the grid.
        """
        return self._width // self._size

    def get_num_rows(self) -> int:
        """
        Get the number of rows in the grid.

        :return: The number of rows in the grid.
        """
        return self._height // self._size

    def get_cell_size(self) -> int:
        """
        Get the size of a cell in the grid.

        :return: The size of a cell in the grid.
        """
        return self._size

    def get_x_offset(self) -> int:
        """
        Get the x offset of the grid.

        :return: The x offset of the grid.
        """
        return self._x

    def get_y_offset(self) -> int:
        """
        Get the y offset of the grid.

        :return: The y offset of the grid.
        """
        return self._y

    def get_grid(self) -> List[List[Any]]:
        """
        Get the grid.

        :return: The grid.
        """
        return self._grid
