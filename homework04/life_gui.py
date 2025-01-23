import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.grid = self.life.create_grid(randomize=True)

        self.button_frame = pygame.Rect(self.width // 2 - 50, 0, 104, 54)
        self.button = pygame.Rect(self.width // 2 - 48, 2, 100, 50)
        self.error_frame = pygame.Rect(self.width // 2 - 132, self.height // 2 - 7, 304, 34)
        self.error_button = pygame.Rect(self.width // 2 - 130, self.height // 2 - 5, 300, 30)

        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

        self.pause = False

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for row, j in enumerate(self.grid):
            for col, value in enumerate(j):
                x, y = row * self.cell_size, col * self.cell_size
                if value == 0:
                    pygame.draw.rect(self.screen, pygame.Color("White"), (y, x, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("Green"), (y, x, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button.collidepoint(mouse_pos):
                        self.pause = not self.pause

                    if self.pause:
                        pos_x = mouse_pos[1] // self.cell_size
                        pos_y = mouse_pos[0] // self.cell_size
                        if 0 <= pos_x < self.life.rows and 0 <= pos_y < self.life.cols:
                            self.life.curr_generation[pos_x][pos_y] = 1 - self.life.curr_generation[pos_x][pos_y]

            self.screen.fill(pygame.Color("white"))  # очистка экрана
            self.draw_grid()
            self.draw_lines()

            button_color = pygame.Color("pink")
            pygame.draw.rect(self.screen, "black", self.button_frame, border_radius=15)
            pygame.draw.rect(self.screen, button_color, self.button, border_radius=15)
            button_text = self.font.render("Pause" if not self.pause else "Resume", True, pygame.Color("black"))
            if not self.pause:
                self.screen.blit(button_text, (self.button.x + 20, self.button.y + 15))
            else:
                self.screen.blit(button_text, (self.button.x + 10, self.button.y + 15))

            # сообщения об ошибках
            if self.life.is_max_generations_exceeded:
                pygame.draw.rect(self.screen, "black", self.error_frame, border_radius=0)
                pygame.draw.rect(self.screen, "white", self.error_button, border_radius=0)
                error_msg = self.font.render("Max generations exceeded", True, pygame.Color("red"))
                self.screen.blit(error_msg, (self.width // 3, self.height // 2))
                self.pause = True
            if not self.life.is_changing:
                error_msg = self.font.render("No changes", True, pygame.Color("red"))
                self.screen.blit(error_msg, (self.width // 4, self.height // 2 + 30))

            pygame.display.flip()
            clock.tick(self.speed)

            if not self.pause:
                self.life.step()  # если не пауза, поле меняется

        pygame.quit()


life = GameOfLife((24, 50), max_generations=500)
ui = GUI(life)
ui.run()
