## Chess Engine (Pygame)

Small drag-and-drop chess application built with Pygame. It renders an
800×800 board, enforces legal moves (including castling, en passant, and
promotion), highlights moves, and plays simple sounds.

### Features

- Legal move generation with check prevention, castling, promotion, en passant
- Drag-and-drop pieces with move previews and last-move highlight
- Multiple color themes (cycle with `T`) and board reset (`R`)
- Move and capture sounds; piece sprites bundled in `assets/`

### Requirements

- Python 3.10+ (tested with 3.12)
- Pygame (`pip install pygame`)

### Run

```bash
pip install pygame
python src/main.py
```

### Controls

- Click and drag a piece to a highlighted square to move.
- Press `T` to switch board themes.
- Press `R` to reset the game.

### Project Layout

- `src/` – game code (`main.py`, `game.py`, `board.py`, etc.)
- `assets/images/` – chess piece sprites (80px and 128px)
- `assets/sounds/` – move and capture sound effects
