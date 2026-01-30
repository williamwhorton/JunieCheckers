import unittest
import pygame
from checkers.game import Game
from checkers.constants import RED, BLACK, ROWS, COLS
from checkers.piece import Piece

# Mock pygame.display.update to avoid errors in headless environment
import pygame.display
pygame.display.init()
pygame.display.set_mode((800, 800))

class TestMultiJump(unittest.TestCase):
    def setUp(self):
        self.win = pygame.display.set_mode((800, 800))
        self.game = Game(self.win)
        self.game.board.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.game.board.red_left = self.game.board.black_left = 0

    def test_forced_multi_jump(self):
        # Set up a multi-jump scenario for RED
        # RED piece at (5, 5)
        # BLACK pieces at (4, 4) and (2, 2)
        red_piece = Piece(5, 5, RED)
        black_piece1 = Piece(4, 4, BLACK)
        black_piece2 = Piece(2, 2, BLACK)
        
        self.game.board.board[5][5] = red_piece
        self.game.board.board[4][4] = black_piece1
        self.game.board.board[2][2] = black_piece2
        self.game.board.red_left = 1
        self.game.board.black_left = 2
        
        self.game.turn = RED
        
        # Select the red piece
        self.game.select(5, 5)
        self.assertIn((3, 3), self.game.valid_moves)
        
        # Perform first jump
        self.game.select(3, 3)
        
        # After first jump, it should still be RED's turn because another jump is available to (1, 1)
        self.assertEqual(self.game.turn, RED, "Turn should not change if another jump is available")
        self.assertEqual(self.game.selected, red_piece, "The same piece should remain selected")
        self.assertIn((1, 1), self.game.valid_moves, "The next jump should be in valid moves")
        self.assertEqual(len(self.game.valid_moves), 1, "Only the next jump should be available")

        # Try to select another piece or square (should be ignored or handled by select logic)
        # In our case, select(3,3) again shouldn't do anything because there is no piece there now (it moved to 3,3 though)
        # Wait, piece is AT (3,3) now.
        res = self.game.select(5,5) # Try to select empty square
        self.assertFalse(res)
        self.assertEqual(self.game.selected, red_piece)
        
        # Finish the jump
        self.game.select(1, 1)
        self.assertEqual(self.game.turn, BLACK, "Turn should change after multi-jump is finished")
        self.assertIsNone(self.game.selected)
        self.assertEqual(self.game.board.black_left, 0)

if __name__ == '__main__':
    unittest.main()
