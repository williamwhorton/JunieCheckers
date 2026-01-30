import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, BLACK
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 40)

    while run:
        clock.tick(FPS)
        
        winner = game.winner()
        if winner is not None:
            text = "RED WINS!" if winner == RED else "BLACK WINS!"
            render_text = font.render(text, True, (0, 255, 0))
            WIN.blit(render_text, (WIDTH//2 - render_text.get_width()//2, HEIGHT//2 - render_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

if __name__ == '__main__':
    main()
