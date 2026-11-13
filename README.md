# Wordle

A Wordle clone in Python with pygame. A 42 Lyon team project with Victor Quetier (gossan).

## The game

- A random five-letter word is picked from `words.txt` (12,972 English words)
- You have six tries. Type letters, `Backspace` to erase, `Enter` to submit
- A try is accepted only if it is in the word list
- Each letter is colored green (right place), yellow (in the word, wrong place) or grey. Repeated letters are counted the way the original game does
- At the end, `Enter` starts a new game and `Esc` quits

## Run

Needs [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer.

```sh
make install   # uv sync
make run
```

## Development

```sh
make lint      # flake8 + mypy
make test      # pytest
```

| File | Role |
|---|---|
| `src/game.py` | Game state and the coloring of a try |
| `src/renderer.py` | pygame window, keyboard input, end screen |
| `src/parsing.py` | Loads and checks the word list |
