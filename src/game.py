import random
import re

from .colors import EColor

from .classes.Exception import GameError


class Game:
    def __init__(self, words: list[str], n_tries: int = 6) -> None:
        self.word = random.choice(words)
        self.n_tries: int = n_tries
        self.tries: list[tuple[str, list[EColor]]] = []

    def is_win(self) -> bool:
        if len(self.tries) > 0 and self.tries[-1][0] == self.word:
            return True
        return False

    def is_ended(self) -> bool:
        if self.is_win() or len(self.tries) >= self.n_tries:
            return True
        return False

    def add_try(self, _try: str) -> None:
        if self.is_ended():
            raise GameError("Try to add word but game already finish")
        if len(_try) != 5:
            raise GameError("word len must be 5")

        word_number_of_letter = {
            letter: self.word.count(letter) for letter in self.word
        }

        try_number_of_letter = {}

        res: tuple[str, list[EColor | None]] = (_try, [None] * 5)

        for i, (letter_t, letter_w) in enumerate(zip(_try, self.word)):
            if letter_t == letter_w:
                try_number_of_letter[letter_t] = (
                    try_number_of_letter.get(letter_t, 0) + 1
                )
                res[1][i] = EColor.GREEN

        for i, letter in enumerate(_try):
            if res[1][i] is not None:
                continue
            w_letter_count = word_number_of_letter.get(letter, 0)
            t_letter_count = try_number_of_letter.get(letter, 0)

            if w_letter_count > t_letter_count:
                res[1][i] = EColor.YELLOW
            else:
                res[1][i] = EColor.GREY

            try_number_of_letter[letter] = (
                try_number_of_letter.get(letter, 0) + 1
            )

        if None in {c for c in res[1]}:
            raise GameError("Error during color calculation")
        self.tries.append(res)
