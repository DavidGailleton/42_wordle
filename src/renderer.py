import pygame

from .game import Game
from .colors import EColor

CELLS_PADDING_RATIO = 0.05
BORDER_PADDING_RATIO = 0.1
OUTER_LINE_RATIO = 0.03
FONT_RATIO = 0.07
END_SCREEN_PADDING_RATIO = 0.1


class Renderer:
    def __init__(self, game: Game):
        self.game = game
        self.running = True
        self.buffer: list[str] = []
        _, screen_h = pygame.display.get_desktop_sizes()[0]
        self.height = int(screen_h * 0.8)
        self.width = int(self.height * (9 / 16))
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.cells_padding = int(self.width * CELLS_PADDING_RATIO)
        self.border_padding = int(self.width * BORDER_PADDING_RATIO)
        self.cell_size = int((self.width - self.border_padding * 2
                              - self.cells_padding * 4) / 5)
        self.outer_line = int(self.cell_size * OUTER_LINE_RATIO)

        self.end_screen_padding = END_SCREEN_PADDING_RATIO * self.height
        pannel_size = self.cell_size * self.game.n_tries + \
            self.cells_padding * (self.game.n_tries)
        self.start_y = int((self.height - pannel_size) / 2)
        self.font = pygame.font.SysFont(None, int(FONT_RATIO * self.height))
        self.red_percent = 0

    def end_screen(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.reset_game()
                self.buffer = []
                return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(overlay, (18, 18, 19, 50),
                         (0, 0, self.width, self.height))

        self.screen.blit(overlay, (0, 0))

        to_draw = ("You lost !", EColor.RED.value)
        if self.game.is_win():
            to_draw = ("You won !", EColor.GREEN.value)

        text = self.font.render(
            to_draw[0],
            True,
            to_draw[1]
        )
        cx = self.width // 2
        cy = int(self.height // 2.5) - self.end_screen_padding // 2
        rect = text.get_rect(center=(cx, cy))
        self.screen.blit(text, rect)

        text = self.font.render(
            f"The word was {self.game.word}.",
            True,
            (255, 255, 255)
        )
        cx = self.width // 2
        cy = int(self.height // 2.5) + self.end_screen_padding // 2
        rect = text.get_rect(center=(cx, cy))
        self.screen.blit(text, rect)

        text = self.font.render(
            "Restart [ENTER]",
            True,
            (255, 255, 255)
        )
        cx = self.width // 2
        cy = self.height // 4 * 3
        rect = text.get_rect(center=(cx, cy))
        self.screen.blit(text, rect)

        pygame.display.flip()

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.unicode and event.unicode.isalpha():
                    if not len(self.buffer) < 5:
                        continue
                    self.buffer.append(event.unicode.lower())

                elif event.key == pygame.K_BACKSPACE:
                    if len(self.buffer) == 0:
                        continue
                    self.buffer.pop()

                elif event.key == pygame.K_RETURN and len(self.buffer) == 5:
                    _try = ""
                    for c in self.buffer:
                        _try += c
                    if self.game.add_try(_try):
                        self.buffer = []
                    else:
                        self.red_percent = 100

        pygame.draw.rect(
            self.screen,
            EColor.BACKGROUND.value,
            (0, 0, self.width, self.height)
        )

        for i in range(self.game.n_tries):
            y = self.start_y + i * (self.cell_size + self.cells_padding)
            word: str | None = None
            outer_line = True
            if i in range(len(self.game.tries)):
                word = self.game.tries[i][0]
                outer_line = False
            elif i == len(self.game.tries):
                word = ""
                for c in self.buffer:
                    word += c
                word += ' ' * (5 - len(word))
            for j in range(5):
                x = self.border_padding + \
                    self.cell_size * j + \
                    self.cells_padding * j

                if outer_line:
                    pygame.draw.rect(
                        self.screen,
                        EColor.OUTER_LINE.value,
                        (x, y, self.cell_size, self.cell_size)
                    )

                cell_color = EColor.CELL.value
                if i in range(len(self.game.tries)):
                    cell_color = self.game.tries[i][1][j].value

                if i == len(self.game.tries):
                    cell_color = (
                        cell_color[0] * (100 - self.red_percent) / 100
                        + EColor.RED.value[0] * self.red_percent / 100,
                        cell_color[1] * (100 - self.red_percent) / 100
                        + EColor.RED.value[1] * self.red_percent / 100,
                        cell_color[2] * (100 - self.red_percent) / 100
                        + EColor.RED.value[2] * self.red_percent / 100,
                    )

                self.red_percent = max(0, self.red_percent - 1)

                if outer_line:
                    pygame.draw.rect(
                        self.screen,
                        cell_color,
                        (x + self.outer_line,
                         y + self.outer_line,
                         self.cell_size - self.outer_line * 2,
                         self.cell_size - self.outer_line * 2)
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        cell_color,
                        (x, y, self.cell_size, self.cell_size)
                    )

                if word is not None and len(word):
                    text = self.font.render(
                        word[j],
                        True,
                        (255, 255, 255)
                    )
                    cx = x + self.cell_size // 2
                    cy = y + self.cell_size // 2
                    rect = text.get_rect(center=(cx, cy))
                    self.screen.blit(text, rect)

        pygame.display.flip()
