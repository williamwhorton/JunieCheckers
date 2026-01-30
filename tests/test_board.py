import unittest
from checkers.board import Board
from checkers.constants import RED, BLACK, ROWS, COLS
from checkers.piece import Piece

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_initialization(self):
        # Check if pieces are placed in the correct starting positions
        # Standard American Checkers: 12 pieces for each player
        red_pieces = 0
        black_pieces = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.board[row][col]
                if piece != 0:
                    if piece.color == RED:
                        red_pieces += 1
                    elif piece.color == BLACK:
                        black_pieces += 1
        
        self.assertEqual(red_pieces, 12)
        self.assertEqual(black_pieces, 12)

    def test_move_piece(self):
        # Find a piece to move
        piece = None
        start_row, start_col = -1, -1
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.board[row][col] != 0:
                    piece = self.board.board[row][col]
                    start_row, start_col = row, col
                    break
            if piece: break
        
        target_row, target_col = 4, 4 # Just some empty spot
        self.board.move(piece, target_row, target_col)
        
        self.assertEqual(self.board.board[start_row][start_col], 0)
        self.assertEqual(self.board.board[target_row][target_col], piece)
        self.assertEqual(piece.row, target_row)
        self.assertEqual(piece.col, target_col)

    def test_get_piece(self):
        piece = self.board.get_piece(0, 1)
        self.assertEqual(self.board.board[0][1], piece)

    def test_get_valid_moves_regular_red(self):
        # Red pieces are at rows 5, 6, 7
        # A red piece at (5, 2) should be able to move to (4, 1) and (4, 3)
        piece = self.board.get_piece(5, 2)
        moves = self.board.get_valid_moves(piece)
        self.assertIn((4, 1), moves)
        self.assertIn((4, 3), moves)
        self.assertEqual(len(moves), 2)

    def test_get_valid_moves_regular_black(self):
        # Black pieces are at rows 0, 1, 2
        # A black piece at (2, 1) should be able to move to (3, 0) and (3, 2)
        piece = self.board.get_piece(2, 1)
        moves = self.board.get_valid_moves(piece)
        self.assertIn((3, 0), moves)
        self.assertIn((3, 2), moves)
        self.assertEqual(len(moves), 2)

if __name__ == '__main__':
    unittest.main()
