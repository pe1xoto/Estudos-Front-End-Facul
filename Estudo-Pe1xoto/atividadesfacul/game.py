import pygame
import random

# Configuraç�es do jogo
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10

# Cores
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Ciano
    (0, 0, 255),    # Azul
    (255, 127, 0),  # Laranja
    (255, 255, 0),  # Amarelo
    (0, 255, 0),    # Verde
    (255, 0, 255),  # Roxo
    (255, 0, 0),    # Vermelho
]

# Formas dos blocos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

# Funç�es auxiliares
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))

def draw_grid(surface, grid):
    sx = WIDTH // 2 - GRID_WIDTH * CELL_SIZE // 2
    sy = HEIGHT - GRID_HEIGHT * CELL_SIZE
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (sx + j * CELL_SIZE, sy + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
    pygame.draw.rect(surface, (255, 0, 0), (sx, sy, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 5)

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

# Classe para peças
class Piece:
    def _init_(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

# Variáveis do jogo
grid = create_grid()
locked_positions = {}
fall_time = 0
fall_speed = 0.27
current_piece = get_shape()
next_piece = get_shape()
clock = pygame.time.Clock()
fall_speed_increase = 0.02
score = 0

# Loop principal do jogo
run = True
while run:
    grid = create_grid(locked_positions)
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        current_piece.y += 1
        if not valid_space(current_piece, grid) and current_piece.y > 0:
            current_piece.y -= 1
            change_piece = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
            elif event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif event.key == pygame.K_DOWN:
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            elif event.key == pygame.K_UP:
                current_piece.rotation += 1
                if not valid_space(current_piece, grid):
                    current_piece.rotation -=