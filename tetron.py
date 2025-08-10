import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0),    # Z
    (255, 105, 180),# 2-block
    (173, 216, 230) # 3-block
]

# Tetromino shapes (standard + 2-block + 3-block)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]],     # L
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[1, 1, 0],
     [0, 1, 1]],     # Z
    [[1, 1]],         # 2-block horizontal
    [[1], [1]],       # 2-block vertical
    [[1, 1, 1]],      # 3-block horizontal
    [[1], [1], [1]],  # 3-block vertical
    [[1, 0],
     [1, 1]],         # 3-block L
    [[0, 1],
     [1, 1]]          # 3-block reverse L
]

# Game grid
grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

# Score and level
score = 0
level = 5
lines_cleared_total = 0

# Tetromino class
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and grid[ny][nx] != BLACK):
                        return False
        return True

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

# Draw grid and tetromino
def draw(win, tetromino):
    win.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(win, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(win, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, tetromino.color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw score and level
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    win.blit(score_text, (10, 10))
    win.blit(level_text, (10, 40))

    pygame.display.update()

# Clear full lines
def clear_lines():
    global grid, score, level, lines_cleared_total
    new_grid = [row for row in grid if BLACK in row]
    lines_cleared = ROWS - len(new_grid)
    if lines_cleared > 0:
        lines_cleared_total += lines_cleared
        score += [0, 100, 300, 500, 800][min(lines_cleared, 4)] * level
        level = lines_cleared_total // 10 + 1
    grid = [[BLACK for _ in range(COLS)] for _ in range(lines_cleared)] + new_grid

# Main game loop
def main():
    global score, level, lines_cleared_total
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Custom Tetris")
    clock = pygame.time.Clock()
    fall_time = 0
    tetromino = Tetromino()
    running = True

    while running:
        fall_speed = max(50, 400 - (level - 1) * 30)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        if fall_time > fall_speed:
            fall_time = 0
            if tetromino.valid(dy=1):
                tetromino.y += 1
            else:
                tetromino.lock()
                clear_lines()
                tetromino = Tetromino()
                if not tetromino.valid():
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetromino.valid(dx=-1):
                    tetromino.x -= 1
                elif event.key == pygame.K_RIGHT and tetromino.valid(dx=1):
                    tetromino.x += 1
                elif event.key == pygame.K_DOWN and tetromino.valid(dy=1):
                    tetromino.y += 1
                elif event.key == pygame.K_UP:
                    tetromino.rotate()
                    if not tetromino.valid():
                        tetromino.rotate()
                        tetromino.rotate()
                        tetromino.rotate()
                elif event.key == pygame.K_SPACE:
                    while tetromino.valid(dy=1):
                        tetromino.y += 1
                    tetromino.lock()
                    clear_lines()
                    tetromino = Tetromino()
                    if not tetromino.valid():
                        running = False

        draw(win, tetromino)

    # Game Over screen
    win.fill(BLACK)
    font = pygame.font.SysFont("Arial", 36)
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
    win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
