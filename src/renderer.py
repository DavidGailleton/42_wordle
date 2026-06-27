import pygame

from .game import Game


BACKGROUND_COLOR = (30, 30, 30)
OUTER_LINE_COLOR = (100, 100, 100)
CELL_COLOR = (40, 40, 40)

CELLS_PADDING_RATIO = 0.05
BORDER_PADDING_RATIO = 0.1
OUTER_LINE_RATIO = 0.03
FONT_RATIO = 0.07


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

        pannel_size = self.cell_size * self.game.n_tries + \
            self.cells_padding * (self.game.n_tries)
        self.start_y = int((self.height - pannel_size) / 2)
        self.font = pygame.font.SysFont(None, int(FONT_RATIO * self.height))

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
                    print(self.buffer)
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.buffer) == 0:
                        continue
                    self.buffer.pop()
                    print(self.buffer)

        pygame.draw.rect(
            self.screen,
            BACKGROUND_COLOR,
            (0, 0, self.width, self.height)
        )

        for i in range(self.game.n_tries):
            y = self.start_y + i * (self.cell_size + self.cells_padding)
            word = None
            if i in range(len(self.game.tries)):
                word = self.game.tries[i][1]
            elif i == len(self.game.tries):
                word = ""
                for c in self.buffer:
                    word += c
                word += ' ' * (5 - len(word))
            for j in range(5):
                x = self.border_padding + \
                    self.cell_size * j + \
                    self.cells_padding * j

                pygame.draw.rect(
                    self.screen,
                    OUTER_LINE_COLOR,
                    (x, y, self.cell_size, self.cell_size)
                )

                cell_color = CELL_COLOR
                if i in range(len(self.game.tries)):
                    cell_color = self.game.tries[i][1][j]

                pygame.draw.rect(
                    self.screen,
                    cell_color,
                    (x + self.outer_line,
                     y + self.outer_line,
                     self.cell_size - self.outer_line * 2,
                     self.cell_size - self.outer_line * 2)
                )

                if word:
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
