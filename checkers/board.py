from dataclasses import replace
import pygame
from checkers.constants import BLACK, RED, ROWS, COLS, SQUARE_SIZE, WHITE
from checkers.piece import Piece

class Board:
    board: tuple[tuple[Piece | int, ...], ...]
    red_left: int
    black_left: int

    def __init__(self):
        self.red_left = self.black_left = 12
        self.board = self.create_board(self)

    @staticmethod
    def draw_squares(win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def create_board(self) -> tuple[tuple[Piece | int, ...], ...]:
        board = []
        for row in range(ROWS):
            current_row = []
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        current_row.append(Piece(row, col, BLACK))
                    elif row > 4:
                        current_row.append(Piece(row, col, RED))
                    else:
                        current_row.append(0)
                else:
                    current_row.append(0)
            board.append(tuple(current_row))
        return tuple(board)

    def move(self, piece: Piece, row: int, col: int):
        # Create new piece with updated position
        new_piece = replace(piece, row=row, col=col)
        
        # Promotion logic
        if (row == ROWS - 1 or row == 0) and not new_piece.king:
            new_piece = replace(new_piece, king=True)

        # Update board tuple
        new_board = [list(r) for r in self.board]
        new_board[piece.row][piece.col] = 0
        new_board[row][col] = new_piece
        self.board = tuple(tuple(r) for r in new_board)
        
        return new_piece

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces: tuple[Piece, ...]):
        new_board = [list(r) for r in self.board]
        for piece in pieces:
            new_board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_left -= 1
            else:
                self.black_left -= 1
        self.board = tuple(tuple(r) for r in new_board)

    def winner(self):
        if self.red_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return RED
        
        return None

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece: Piece) -> dict[tuple[int, int], tuple[Piece, ...]]:
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, left, direction=-1))
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, right, direction=1))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, left, direction=-1))
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, right, direction=1))
    
        # Forced jumps logic
        any_jumps = any(skipped for move, skipped in moves.items())
        if any_jumps:
            # Filter to keep only moves that skip a piece
            moves = {move: skipped for move, skipped in moves.items() if skipped}

        return moves

    def _traverse(self, start, stop, step, color, col, direction, skipped: tuple[Piece, ...] = ()) -> dict[tuple[int, int], tuple[Piece, ...]]:
        """
        direction: -1 for left, 1 for right
        """
        moves = {}
        last = ()
        for r in range(start, stop, step):
            if direction == -1 and col < 0:
                break
            if direction == 1 and col >= COLS:
                break
            
            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = skipped + last
                else:
                    moves[(r, col)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse(r+step, row, step, color, col-1, -1, skipped=skipped+last))
                    moves.update(self._traverse(r+step, row, step, color, col+1, 1, skipped=skipped+last))
                break
            elif current.color == color:
                break
            else:
                last = (current,)

            col += direction
        
        return moves
