import pygame
import sys
import os
import random

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
SPEED = 16
SCORE = 0
FPS = 10

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print("Cannot load image:", name)
        raise SystemExit(e)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Snake", "",
                  "made by Anna,",
                  "with Pasha's help"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 85
    for line in intro_text:
        string_rendered = font.render(line, True, (154, 48, 1))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def gameover():
    intro_text = ["GAME OVER!",
                  f"Score: {SCORE}"]

    fon = pygame.transform.scale(load_image('screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 180
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


class Ball:
    def __init__(self):
        self.radius = 7
        self.x = random.randrange(20, WIDTH - 20)
        self.y = random.randrange(20, HEIGHT - 20)

    def change_position(self):
        self.x = random.randrange(20, WIDTH - 20)
        self.y = random.randrange(20, HEIGHT - 20)

    def draw(self):
        pygame.draw.circle(screen, pygame.Color("red"),
                           (self.x + self.radius, self.y + self.radius), self.radius)


class Snake:
    def __init__(self):
        x, y = random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100)
        self.position = [x, y]
        self.width, self.height = 14, 14
        self.body = [(x, y), (x + self.width, y),
                     (x + 2 * self.width, y)]
        self.direction = 'left'
        self.moving = True

    def move(self):
        if self.moving:
            if self.direction == 'left':
                self.position[0] -= SPEED
            elif self.direction == 'right':
                self.position[0] += SPEED
            elif self.direction == 'down':
                self.position[1] += SPEED
            elif self.direction == 'up':
                self.position[1] -= SPEED

    def draw(self):
        if self.moving:
            self.body.insert(0, (self.position[0], self.position[1]))
            if ball.x - 2 <= self.position[0] <= ball.x + ball.radius * 2 + 2 \
                    and ball.y - 2 <= self.position[1] <= ball.y + ball.radius * 2 + 2:
                ball.change_position()
                global SCORE
                SCORE += 1
            else:
                self.body.pop()
        for cube in self.body:
            pygame.draw.rect(screen, 'blue', (cube[0], cube[1], self.width, self.height))

    def crashed(self):
        if self.position[0] <= 2 or self.position[0] >= WIDTH - 6 \
                or self.position[1] <= 4 or self.position[1] >= HEIGHT - 6:
            gameover()
        for cube in self.body[1:]:
            if self.position[0] == cube[0] and self.position[1] == cube[1]:
                gameover()


start_screen()

running = True
snake = Snake()
ball = Ball()

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_DOWN] and snake.moving:
            if snake.direction in 'rightleft':
                snake.direction = 'down'
        if keys[pygame.K_UP] and snake.moving:
            if snake.direction in 'rightleft':
                snake.direction = 'up'
        if keys[pygame.K_RIGHT] and snake.moving:
            if snake.direction in 'updown':
                snake.direction = 'right'
        if keys[pygame.K_LEFT] and snake.moving:
            if snake.direction in 'updown':
                snake.direction = 'left'
        if keys[pygame.K_SPACE]:
            snake.moving = not snake.moving
    screen.fill((200, 200, 200))
    pygame.draw.line(screen, 'black', (5, 5), (WIDTH - 5, 5), width=2)
    pygame.draw.line(screen, 'black', (5, HEIGHT - 5), (WIDTH - 5, HEIGHT - 5), width=2)
    pygame.draw.line(screen, 'black', (5, 5), (5, HEIGHT - 5), width=2)
    pygame.draw.line(screen, 'black', (WIDTH - 5, 5), (WIDTH - 5, HEIGHT - 5), width=2)
    ball.draw()
    snake.move()
    snake.draw()
    snake.crashed()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
