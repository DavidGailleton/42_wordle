"""Main entry point for the project."""

from .parsing import parsing
from .game import Game
from .renderer import Renderer


def main() -> int:
    """Run the main program.

    Returns:
        Exit status code.
    """
    try:
        words = parsing("words.txt")
        game = Game(words, {"tries": 6})
        renderer = Renderer(game)
        while True:
            inputs = input_handler.get()
            game.update(inputs)
            renderer.update()
        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
