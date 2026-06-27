import random
from colorama import Back, Fore, Style


class Game:
    def __init__(self, words: list[str]) -> None:
        self.word = random.choice(words)
        self.tries: list[str] = []
