import random


class Game:
    def __init__(self, words: list[str]) -> None:
        self.word = random.choice(words)
