import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание поля
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

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
        return [[random.randint(0, int(randomize)) for x in range(self.cell_width)] for y in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row, j in enumerate(self.grid):
            for col, value in enumerate(j):
                x, y = row * self.cell_size, col * self.cell_size
                if value == 0:
                    pygame.draw.rect(self.screen, pygame.Color("White"), (y, x, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("Green"), (y, x, self.cell_size, self.cell_size))

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
        for x in range(x_pos - 1, x_pos + 2):
            for y in range(y_pos - 1, y_pos + 2):
                if 0 <= x <= self.cell_height - 1 and 0 <= y <= self.cell_width - 1 and (x, y) != (x_pos, y_pos):
                    neighbours.append(self.grid[x][y])
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
                if (neighbours_number == 2 or neighbours_number == 3) and self.grid[x][y] == 1:
                    next_generation[x][y] = 1
                elif (neighbours_number < 2 or neighbours_number > 3) and self.grid[x][y] == 1:
                    next_generation[x][y] = 0
                elif neighbours_number == 3 and self.grid[x][y] == 0:
                    next_generation[x][y] = 1
                else:
                    next_generation[x][y] = self.grid[x][y]
        return next_generation


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
