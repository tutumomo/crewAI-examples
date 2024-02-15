import pygame
import sys

# Initialize pygame
pygame.init()

# Set the dimensions of the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Set the dimensions of the game board
BOARD_SIZE = 10
CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Five-in-a-Row")

def draw_board():
    window.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(window, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board()
        pygame.display.update()

if __name__ == "__main__":
    main()