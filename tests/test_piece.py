from dataclasses import replace
import unittest
from checkers.piece import Piece
from checkers.constants import RED

class TestPiece(unittest.TestCase):
    def test_piece_initialization(self):
        piece = Piece(0, 0, RED)
        self.assertEqual(piece.row, 0)
        self.assertEqual(piece.col, 0)
        self.assertEqual(piece.color, RED)
        self.assertFalse(piece.king)

    def test_make_king(self):
        piece = Piece(0, 0, RED)
        piece = replace(piece, king=True)
        self.assertTrue(piece.king)

    def test_piece_move(self):
        piece = Piece(0, 0, RED)
        piece = replace(piece, row=2, col=3)
        self.assertEqual(piece.row, 2)
        self.assertEqual(piece.col, 3)

if __name__ == '__main__':
    unittest.main()
