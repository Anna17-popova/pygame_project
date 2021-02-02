import pygame
import sys
import os
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
sound = pygame.mixer.Sound('game_over.wav')
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
SCORE = 0
FPS = 5


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


def data():
    with open('results.txt', 'a', encoding='utf8') as f:
        f.write(f"Ваш счёт в игре составил {SCORE}.\n")
        f.write("------------------------------------\n")


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()
image = load_image('arrow.png')
cursor = pygame.sprite.Sprite(all_sprites)
cursor.image = image
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)


def start_screen():
    intro_text = ["Snake", "",
                  "made by Anna,",
                  "with Pasha's help"]
    button = 'START'
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    font1 = pygame.font.Font(None, 20)
    rendered = font1.render(button, True, (255, 0, 0))
    rect = rendered.get_rect()
    rect.y = 40
    rect.x = 300
    screen.blit(rendered, rect)
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
            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (rect.x <= event.pos[0] <= rect.x + 150) and (rect.y <= event.pos[1] <= rect.y + 50):
                    return

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
        font1 = pygame.font.Font(None, 50)
        rendered = font1.render(button, True, (154, 48, 1))
        rect = rendered.get_rect()
        rect.y = 150
        rect.x = 190
        pygame.draw.rect(screen, (154, 48, 1), (rect.x - 5, rect.y - 5, 120, 50), width=2)
        screen.blit(rendered, rect)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def gameover(f):
    pygame.mixer.music.stop()
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
    pygame.display.flip()
    sound.play()
    pygame.time.delay(3500)
    data()
    pygame.quit()
    sys.exit()


class Ball:
    def __init__(self):
        self.radius = 5
        self.x = random.randrange(20, WIDTH - 20)
        self.y = random.randrange(20, HEIGHT - 20)

    def change_position(self):
        self.x = random.randrange(20, WIDTH - 20)
        self.y = random.randrange(20, HEIGHT - 20)

    def draw(self):
        pygame.draw.circle(screen, pygame.Color("red"),
                           (self.x, self.y), self.radius)


class Snake:
    def __init__(self):
        x, y = random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100)
        self.position = [x, y]
        self.width, self.height = 10, 10
        self.body = [(x, y), (x + self.width, y),
                     (x + 2 * self.width, y)]
        self.direction = 'left'
        self.moving = True
        self.changed = False
        self.speed = 12
        self.flag = False

    def move(self):
        if self.moving:
            if self.direction == 'left':
                self.position[0] -= self.speed
            elif self.direction == 'right':
                self.position[0] += self.speed
            elif self.direction == 'down':
                self.position[1] += self.speed
            elif self.direction == 'up':
                self.position[1] -= self.speed

    def draw(self):
        if self.moving:
            self.body.insert(0, (self.position[0], self.position[1]))
            if (ball.x - ball.radius <= self.position[0] <= ball.x + ball.radius or ball.x - ball.radius <=
                self.position[0] + self.width <= ball.x + ball.radius) \
                    and (ball.y - 5 <= self.position[1] <= ball.y + 5
                         or ball.y - 5 <= self.position[1] + self.height <= ball.y + 5):
                ball.change_position()
                global SCORE
                SCORE += 1
                self.changed = True
            else:
                self.body.pop()
                self.changed = False
        for cube in self.body:
            pygame.draw.rect(screen, 'blue', (cube[0], cube[1], self.width, self.height))

    def crashed(self):
        for cube in self.body[1:]:
            if (cube[0] == self.position[0]) and (cube[1] == self.position[1]):
                self.flag = True
                break
        if (self.position[0] <= 2 or self.position[0] > WIDTH - 5
            or self.position[1] <= 5 or self.position[1] >= HEIGHT - 5) or self.flag:
            gameover(False)

    def acceleration(self):
        if self.changed and SCORE % 3 == 0:
            global FPS
            FPS += 3


start_screen()
running = True
snake = Snake()
ball = Ball()
pygame.mixer.music.play(-1)
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
    snake.acceleration()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
