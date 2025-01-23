import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
        Если значение истина, то создается матрица, где каждая клетка может
        быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        return [[random.randint(0, int(randomize)) for x in range(self.cols)] for y in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x_pos, y_pos = cell[0], cell[1]
        neighbours = []
        for x, row in enumerate(self.curr_generation):
            for y, val in enumerate(row):
                if (-1 <= x - x_pos <= 1) and (-1 <= y - y_pos <= 1) and ((x, y) != (x_pos, y_pos)):
                    neighbours.append(self.curr_generation[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        next_generation = self.create_grid()
        for x, row in enumerate(next_generation):
            for y, value in enumerate(row):
                neighbours = self.get_neighbours((x, y))
                neighbours_number = sum(neighbours)
                if (neighbours_number == 2 or neighbours_number == 3) and self.curr_generation[x][y] == 1:
                    next_generation[x][y] = 1
                elif (neighbours_number < 2 or neighbours_number > 3) and self.curr_generation[x][y] == 1:
                    next_generation[x][y] = 0
                elif neighbours_number == 3 and self.curr_generation[x][y] == 0:
                    next_generation[x][y] = 1
                else:
                    next_generation[x][y] = self.curr_generation[x][y]
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations if self.max_generations else False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with filename.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    row = [int(value) for value in line]
                    grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as f:
            for row in self.curr_generation:
                f.write("".join([str(x) for x in row]) + "\n")
