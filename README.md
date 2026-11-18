# Python Chess — Desktop Logic Game

A desktop implementation of classic Chess written in Python using the **Pygame** library. The project supports both local two-player mode (PvP) and single-player mode against an AI opponent (PvE).

## Features
* **Game Modes:** Local Multiplayer (PvP) and Player vs. AI Bot (PvE).
* **Full Chess Rules:** Legal move validation, Check, Checkmate, Stalemate, Castling (Kingside & Queenside), En Passant, and Pawn Promotion.
* **Interactive UI:** Visual highlighting of legal moves, selected pieces, and King in check.
* **AI Opponent:** Powered by the Minimax algorithm with Alpha-Beta pruning and positional evaluation.

## Project Structure
* `main.py` — Entry point, game loop, graphical user interface, and input handling.
* `board.py` — Board state management, rule validation, check/checkmate/stalemate detection.
* `pieces.py` — Object-oriented hierarchy of chess pieces (`Piece`, `Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`).
* `ai.py` — Artificial intelligence logic (Minimax algorithm and board evaluation).
* `constants.py` — Configuration settings, window dimensions, color palette, and piece weights.
* `DESIGN_DOC.md` — Full Game Design Document (GDD) and technical architecture overview.

## Installation & Run
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd Practice18
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Controls
* **Left Mouse Click:** Select a piece / Make a move.
* **R:** Restart the current match.
* **ESC:** Return to the Main Menu.