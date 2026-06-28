from .classes.Exception import ParsingError


def parsing(file: str) -> list[str]:
    words: list[str] = []
    with open(file) as f:
        for i, line in enumerate(f):
            word = line.removesuffix("\n").lower()
            if len(word) != 5:
                raise ParsingError(
                    f'Line {i + 1}: word "{word}" len not equal to 5'
                )
            if not word.isalpha():
                raise ParsingError(
                    f'Line {i + 1}: word "{word}" should be only alphabetic'
                )
            words.append(word)
    return words
