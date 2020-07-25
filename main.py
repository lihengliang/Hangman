import pygame
import os
import math

# set path
ROOT = os.path.dirname(__file__)
IMG_PATH = os.path.join(ROOT, 'images')

# set display
pygame.init()
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# load images
images = []
for subdir, dirs, files in os.walk(IMG_PATH):
    for file in files:
        image = pygame.image.load(os.path.join(IMG_PATH, file))
        images.append(image)

# game variables
hangman_status = 0

# button variables
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i//13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set game loop
FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    window.fill(WHITE)

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()


while run:
    clock.tick(FPS)

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - float(m_x))**2 + (y - int(m_y))**2)
                    if dis < RADIUS:
                        letter[3] = False


pygame.quit()
