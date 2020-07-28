import pygame
import os
import math
from random_word import RandomWords

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
guess = []

# get random word for game
r = RandomWords()
word = r.get_random_word(minLength=6, maxLength=12, hasDictionaryDef="true")
# word = "TEST"

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
TITLE_FONT = pygame.font.SysFont('comicsans', 60)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set game loop
FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    window.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("PYTHON HANGMAN", 1, BLACK)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

    # draw word
    display_word = ""
    for char in word:
        if char in guess:
            display_word += char + " "
        else:
            display_word += "_ "
    text = LETTER_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def show_msg(msg):
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = LETTER_FONT.render(msg, 1, BLACK)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


while run:
    clock.tick(FPS)

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
                        guess.append(ltr)
                        if ltr not in word:
                            hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guess:
            won = False
            break
    if won:
        show_msg("YOU WIN")
        run = False

    if hangman_status == 6:
        show_msg("YOU LOST")
        run = False


pygame.quit()
