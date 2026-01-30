from dataclasses import dataclass
import pygame
from checkers.constants import SQUARE_SIZE, GREY

@dataclass(frozen=True)
class Piece:
    PADDING = 15
    OUTLINE = 2

    row: int
    col: int
    color: tuple
    king: bool = False

    @property
    def x(self) -> int:
        return SQUARE_SIZE * self.col + SQUARE_SIZE // 2

    @property
    def y(self) -> int:
        return SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # Draw a simple king indicator
            pygame.draw.circle(win, (255, 215, 0), (self.x, self.y), radius // 2)

    def __repr__(self):
        return str(self.color)
