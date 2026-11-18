class Piece:
    def __init__(self, color, name, row, col):
        self.color = color  # 'white' or 'black'
        self.name = name
        self.row = row
        self.col = col
        self.has_moved = False

    def get_pseudo_moves(self, board):
        return []

    def _slide_moves(self, board, directions):
        moves = []
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'pawn', row, col)

    def get_pseudo_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Move forward 1 square
        if 0 <= self.row + direction < 8 and board[self.row + direction][self.col] is None:
            moves.append((self.row + direction, self.col))
            # Move forward 2 squares from start
            if self.row == start_row and board[self.row + 2 * direction][self.col] is None:
                moves.append((self.row + 2 * direction, self.col))

        # Diagonal captures
        for dc in (-1, 1):
            r, c = self.row + direction, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is not None and target.color != self.color:
                    moves.append((r, c))
        return moves


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'rook', row, col)

    def get_pseudo_moves(self, board):
        return self._slide_moves(board, [(-1, 0), (1, 0), (0, -1), (0, 1)])


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'bishop', row, col)

    def get_pseudo_moves(self, board):
        return self._slide_moves(board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'queen', row, col)

    def get_pseudo_moves(self, board):
        return self._slide_moves(board, [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'knight', row, col)

    def get_pseudo_moves(self, board):
        moves = []
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, 'king', row, col)

    def get_pseudo_moves(self, board):
        moves = []
        steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in steps:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves