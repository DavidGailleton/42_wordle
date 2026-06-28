import pygame
from time import perf_counter, sleep

from .parsing import parsing
from .game import Game
from .renderer import Renderer


def main() -> int:
    """Run the main program.

    Returns:
        Exit status code.
    """
    try:
        pygame.init()
    except Exception as error:
        print(f"Error: {error}")
        return 1

    try:
        words = parsing("words.txt")
        game = Game(words, 6)
        renderer = Renderer(game)
        target_delta = 1.0 / 30

        while renderer.running:
            start = perf_counter()
            if game.is_ended():
                renderer.end_screen()
            else:
                renderer.update()
            end = perf_counter()
            if end - start < target_delta:
                elapsed = end - start
                to_sleep = target_delta - elapsed
                sleep(to_sleep)

        return 0

    except Exception as error:
        print(f"Error: {error}")
        return 1

    finally:
        pygame.quit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
