import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    ch = "1"
                else:
                    ch = "0"
                screen.addch(ch)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        running = True
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            if self.life.is_max_generations_exceeded:
                screen.addstr(0, 0, "Max generation has been exceeded. Press q to exit.")
                screen.refresh()
            if self.life.is_changing:
                screen.addstr(0, 0, "Nothing is changing. Press q to exit.")
                screen.refresh()

            key = screen.getch()
            if key == ord("q"):
                running = False
                break
        curses.endwin()
