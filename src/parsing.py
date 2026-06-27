from .classes.Exception import ParsingError


def parsing(file: str) -> list[str]:
    words: list[str] = []
    with open(file) as f:
        for i, line in enumerate(f):
            word = line.removesuffix("\n")
            if len(word) != 5:
                raise ParsingError(
                    f'Line {i}: word "{word}" len not equal to 5'
                )
            words.append(word)
    return words
