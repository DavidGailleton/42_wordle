"""Main entry point for the project."""

from .parsing import parsing


def main() -> int:
    """Run the main program.

    Returns:
        Exit status code.
    """
    try:
        print(parsing("words.txt"))
        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
