import random

from .colors import EColor


class Game:
    def __init__(self, words: list[str], n_tries: int) -> None:
        self.word = random.choice(words)
        self.n_tries = n_tries
        self.tries: list[tuple[str, list[EColor]]] = []

    def add_try(self, _try: str) -> None:
        ...

    def is_win(self) -> bool:
        ...
