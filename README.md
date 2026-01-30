# Checkers Game

A functional, Pygame-based Checkers game (American/British version) written in Python 3.13.

## Features
- Local Player vs. Player.
- Standard checkers rules including:
    - Diagonal moves.
    - Forced jumps.
    - Multi-jump support.
    - Piece promotion to Kings.
- Graphical UI with move indicators and winner display.

## Installation

1.  Ensure you have Python 3.13+ installed.
2.  Install the dependencies:
    ```bash
    pip install pygame-ce
    ```

## How to Play

Run the game using:
```bash
python main.py
```

- Click on a piece of your color (Red starts first) to see valid moves.
- Valid moves are highlighted with green circles.
- Click on a highlighted circle to move the piece.
- Jumps are mandatory.

## Project Structure
- `checkers/`: Core game logic and rendering.
    - `board.py`: Board representation and move validation.
    - `piece.py`: Piece representation.
    - `game.py`: Game state management.
    - `constants.py`: Game constants and colors.
- `tests/`: Unit tests for core logic.
- `main.py`: Entry point for the game.

## Testing
Run the tests using:
```bash
python -m unittest discover tests
```
