import pygame
from checkers.constants import RED, BLACK, SQUARE_SIZE, ROWS, COLS
from checkers.board import Board
from checkers.piece import Piece

class Game:
    win: pygame.Surface
    selected: Piece | None
    board: Board
    turn: tuple
    valid_moves: dict

    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.win, self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                # If we are in the middle of a multi-jump, we cannot deselect or select another piece
                if self.selected and self.valid_moves and any(self.valid_moves.values()):
                     return False

                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # Check if any other piece MUST jump
            if self._can_another_piece_jump(piece):
                return False
            
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _can_another_piece_jump(self, current_piece):
        # Mandatory jump: if any piece can jump, current piece can only move if it also can jump
        any_piece_can_jump = False
        piece_can_jump = False
        
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board.get_piece(r, c)
                if p != 0 and p.color == self.turn:
                    moves = self.board.get_valid_moves(p)
                    if any(s for s in moves.values() if s):
                        any_piece_can_jump = True
                        if p == current_piece:
                            piece_can_jump = True
        
        if any_piece_can_jump and not piece_can_jump:
            return True # Another piece MUST jump
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.selected = self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                # Check for multi-jump
                new_moves = self.board.get_valid_moves(self.selected)
                if any(new_moves.values()):
                    self.valid_moves = new_moves
                    return True
            
            self.selected = None
            self.change_turn()
        else:
            return False

        return True

    @staticmethod
    def draw_valid_moves(win, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(win, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED
