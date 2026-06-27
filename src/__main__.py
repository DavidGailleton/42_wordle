"""Main entry point for the project."""

from .parsing import parsing
from .game import Game


def main() -> int:
    """Run the main program.

    Returns:
        Exit status code.
    """
    try:
        words = parsing("words.txt")
        game = Game(words)
        game.add_try("hello")
        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
