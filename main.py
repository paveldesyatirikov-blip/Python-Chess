import pygame
from constants import *
from board import Board
from ai import minimax

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess — Desktop Game")

FONT_PIECE = pygame.font.SysFont("segoeuisymbol", 68)
FONT_MENU = pygame.font.SysFont("arial", 36, bold=True)
FONT_TITLE = pygame.font.SysFont("arial", 54, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 22)

SYMBOLS = {
    ('white', 'king'): '♔', ('white', 'queen'): '♕', ('white', 'rook'): '♖',
    ('white', 'bishop'): '♗', ('white', 'knight'): '♘', ('white', 'pawn'): '♙',
    ('black', 'king'): '♚', ('black', 'queen'): '♛', ('black', 'rook'): '♜',
    ('black', 'bishop'): '♝', ('black', 'knight'): '♞', ('black', 'pawn'): '♟',
}

def draw_menu(win):
    win.fill(BG_MENU)
    title = FONT_TITLE.render("PYTHON CHESS", True, TEXT_COLOR)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

    btn_pvp = pygame.Rect(WIDTH // 2 - 175, 320, 350, 65)
    btn_pve = pygame.Rect(WIDTH // 2 - 175, 420, 350, 65)
    mouse_pos = pygame.mouse.get_pos()

    for btn, text in [(btn_pvp, "2 Players (PvP)"), (btn_pve, "Play vs Bot (PvE)")]:
        color = BTN_HOVER if btn.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(win, color, btn, border_radius=12)
        label = FONT_MENU.render(text, True, TEXT_COLOR)
        win.blit(label, (btn.centerx - label.get_width() // 2, btn.centery - label.get_height() // 2))

    hint = FONT_SMALL.render("Controls: Mouse | Restart: R | Main Menu: ESC", True, (180, 180, 180))
    win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 650))
    pygame.display.update()
    return btn_pvp, btn_pve

def draw_game(win, board, selected_piece, valid_moves, status):
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
            if selected_piece and (selected_piece.row, selected_piece.col) == (r, c):
                color = SELECTED_COLOR
            pygame.draw.rect(win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Highlight king in check
    if board.is_in_check(board.turn):
        kr, kc = board.find_king(board.turn)
        pygame.draw.rect(win, CHECK_COLOR, (kc * SQUARE_SIZE, kr * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Highlight legal moves
    for r, c in valid_moves:
        center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
        pygame.draw.circle(win, HIGHLIGHT, center, 16)

    # Draw pieces
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.grid[r][c]
            if piece:
                symbol = SYMBOLS[(piece.color, piece.name)]
                text_surf = FONT_PIECE.render(symbol, True, (20, 20, 20))
                rect = text_surf.get_rect(center=(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2))
                win.blit(text_surf, rect)

    # Game over overlay
    if status != "PLAYING":
        overlay = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        win.blit(overlay, (0, HEIGHT // 2 - 70))
        msg = FONT_MENU.render(status, True, (255, 215, 0))
        sub = FONT_SMALL.render("Press R to restart or ESC for Main Menu", True, TEXT_COLOR)
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        win.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    mode = None  # 'PVP' or 'PVE'
    board = Board()
    selected_piece = None
    valid_moves = []
    run = True

    while run:
        clock.tick(60)

        if mode is None:
            btn_pvp, btn_pve = draw_menu(WIN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_pvp.collidepoint(event.pos):
                        mode = 'PVP'
                        board = Board()
                    elif btn_pve.collidepoint(event.pos):
                        mode = 'PVE'
                        board = Board()
            continue

        status = board.get_game_status()
        draw_game(WIN, board, selected_piece, valid_moves, status)

        # AI turn (Black)
        if mode == 'PVE' and board.turn == 'black' and status == "PLAYING":
            pygame.time.delay(250)
            _, best_move = minimax(board, 2, -float('inf'), float('inf'), True)
            if best_move:
                piece_to_move, target = best_move
                board.make_move(piece_to_move, target[0], target[1])
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = Board()
                    selected_piece = None
                    valid_moves = []
                elif event.key == pygame.K_ESCAPE:
                    mode = None
                    selected_piece = None
                    valid_moves = []
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and status == "PLAYING":
                if mode == 'PVE' and board.turn == 'black':
                    continue
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                clicked_piece = board.grid[row][col]

                if selected_piece and (row, col) in valid_moves:
                    board.make_move(selected_piece, row, col)
                    selected_piece = None
                    valid_moves = []
                elif clicked_piece and clicked_piece.color == board.turn:
                    selected_piece = clicked_piece
                    valid_moves = board.get_legal_moves(selected_piece)
                else:
                    selected_piece = None
                    valid_moves = []

    pygame.quit()

if __name__ == "__main__":
    main()