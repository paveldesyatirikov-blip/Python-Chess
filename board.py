import copy
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.en_passant_target = None
        self.setup_board()

    def setup_board(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_cls in enumerate(order):
            self.grid[0][col] = piece_cls('black', 0, col)
            self.grid[7][col] = piece_cls('white', 7, col)
        for col in range(8):
            self.grid[1][col] = Pawn('black', 1, col)
            self.grid[6][col] = Pawn('white', 6, col)

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if isinstance(piece, King) and piece.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        opponent = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.color == opponent:
                    if king_pos in piece.get_pseudo_moves(self.grid):
                        return True
        return False

    def get_legal_moves(self, piece):
        moves = piece.get_pseudo_moves(self.grid)

        # En passant for pawns
        if isinstance(piece, Pawn) and self.en_passant_target:
            direction = -1 if piece.color == 'white' else 1
            if piece.row + direction == self.en_passant_target[0] and abs(piece.col - self.en_passant_target[1]) == 1:
                moves.append(self.en_passant_target)

        # Castling for king
        if isinstance(piece, King) and not piece.has_moved and not self.is_in_check(piece.color):
            row = piece.row
            # Kingside castling
            rook_right = self.grid[row][7]
            if isinstance(rook_right, Rook) and not rook_right.has_moved:
                if self.grid[row][5] is None and self.grid[row][6] is None:
                    if not self._square_attacked(row, 5, piece.color) and not self._square_attacked(row, 6, piece.color):
                        moves.append((row, 6))
            # Queenside castling
            rook_left = self.grid[row][0]
            if isinstance(rook_left, Rook) and not rook_left.has_moved:
                if self.grid[row][1] is None and self.grid[row][2] is None and self.grid[row][3] is None:
                    if not self._square_attacked(row, 2, piece.color) and not self._square_attacked(row, 3, piece.color):
                        moves.append((row, 2))

        # Filter moves that leave the king in check
        legal_moves = []
        for move in moves:
            temp_board = copy.deepcopy(self)
            temp_piece = temp_board.grid[piece.row][piece.col]
            temp_board._execute_move(temp_piece, move[0], move[1])
            if not temp_board.is_in_check(piece.color):
                legal_moves.append(move)
        return legal_moves

    def _square_attacked(self, r, c, color):
        opponent = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == opponent:
                    if (r, c) in piece.get_pseudo_moves(self.grid):
                        return True
        return False

    def _execute_move(self, piece, to_row, to_col):
        from_row, from_col = piece.row, piece.col

        # Handle en passant capture
        if isinstance(piece, Pawn) and (to_row, to_col) == self.en_passant_target:
            self.grid[from_row][to_col] = None

        # Update en passant target square
        if isinstance(piece, Pawn) and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        else:
            self.en_passant_target = None

        # Handle castling rook movement
        if isinstance(piece, King) and abs(to_col - from_col) == 2:
            if to_col == 6:
                rook = self.grid[from_row][7]
                self.grid[from_row][5] = rook
                self.grid[from_row][7] = None
                rook.col = 5
                rook.has_moved = True
            elif to_col == 2:
                rook = self.grid[from_row][0]
                self.grid[from_row][3] = rook
                self.grid[from_row][0] = None
                rook.col = 3
                rook.has_moved = True

        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        piece.row, piece.col = to_row, to_col
        piece.has_moved = True

        # Pawn promotion to Queen
        if isinstance(piece, Pawn) and (to_row == 0 or to_row == 7):
            self.grid[to_row][to_col] = Queen(piece.color, to_row, to_col)

    def make_move(self, piece, to_row, to_col):
        if (to_row, to_col) in self.get_legal_moves(piece):
            self._execute_move(piece, to_row, to_col)
            self.turn = 'black' if self.turn == 'white' else 'white'
            return True
        return False

    def get_game_status(self):
        has_moves = False
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.color == self.turn:
                    if len(self.get_legal_moves(piece)) > 0:
                        has_moves = True
                        break
            if has_moves:
                break

        if not has_moves:
            if self.is_in_check(self.turn):
                winner = 'White' if self.turn == 'black' else 'Black'
                return f"CHECKMATE! {winner} wins!"
            return "STALEMATE! Draw!"
        return "PLAYING"