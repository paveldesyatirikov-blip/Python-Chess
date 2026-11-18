# Game Design Document (GDD): Python Chess

## 1. Project Overview
* **Title:** Python Chess
* **Genre:** Desktop Logic / Strategy Board Game
* **Technology Stack:** Python 3.x, Pygame
* **Target Audience:** Chess beginners learning piece movements via visual hints, board game enthusiasts looking for an offline desktop match, and students studying OOP and game AI algorithms.

## 2. Gameplay & Core Mechanics
The game replicates standard international chess rules on an 8×8 grid:
* **Turn Management:** Automatic alternation between White and Black turns.
* **Move Validation:** Pseudo-legal moves are filtered through a deep-copy simulation to guarantee that no move leaves the player's own King in check.
* **Special Rules:**
  * *Castling:* Supported on both kingside and queenside when neither the King nor the Rook has moved and squares are clear and unattacked.
  * *En Passant:* Tracked dynamically after a two-square pawn advance.
  * *Pawn Promotion:* Automatic promotion to a Queen upon reaching the opposite back rank.
* **End-Game Conditions:** Automatic detection of **Checkmate** (win/loss) and **Stalemate** (draw).

## 3. System Architecture (OOP Design)
The codebase is modularized for maintainability and clean separation of concerns:
* **Base Class `Piece` (`pieces.py`):** Stores color, position (`row`, `col`), and movement state (`has_moved`). Provides shared sliding raycast logic (`_slide_moves`) for long-range pieces.
* **Derived Piece Classes (`Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`):** Inherit from `Piece` and override `get_pseudo_moves()` to implement specific movement patterns.
* **`Board` Class (`board.py`):** Manages the 8×8 matrix (`self.grid`), executes moves, tracks special states, and determines game status (`PLAYING`, `CHECKMATE`, `STALEMATE`).
* **UI & Event Loop (`main.py`):** Decouples rendering (`draw_menu`, `draw_game`) from business logic.

## 4. Artificial Intelligence Design (`ai.py`)
In PvE mode, the computer plays as Black using a decision-tree search:
* **Algorithm:** Minimax with Alpha-Beta pruning (search depth = 2 plies) to optimize calculation speed while predicting player responses.
* **Evaluation Function (`evaluate_board`):** Assigns material weights (`Pawn = 10`, `Knight/Bishop = 30`, `Rook = 50`, `Queen = 90`, `King = 900`) and adds a positional bonus (`+2`) for controlling the central squares of the board.

## 5. User Interface (UI/UX)
* **Main Menu:** Clean entry screen allowing instant selection between **2 Players (PvP)** and **Play vs Bot (PvE)**.
* **Visual Feedback:**
  * Yellow highlight for the currently selected piece.
  * Green dot indicators for all legal destination squares.
  * Red square alert when a King is in check.
* **Quick Controls:** Keyboard shortcuts (`R` for instant reset, `ESC` to switch modes) and a semi-transparent end-game banner displaying match results.

## 6. Testing & Verification
The application was tested against edge cases including:
* Pinning pieces (preventing moves that expose the King to an attack).
* Escaping check via blocking, capturing the attacker, or moving the King.
* Executing castling, en passant captures, and pawn promotions without state corruption.
* AI stability and response time during mid-game complexity.