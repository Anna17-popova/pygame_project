import pygame
import sys
import os
import random


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
snake_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
clock = pygame.time.Clock()
SPEED = 10
SCORE = 0


def terminate():
    pygame.quit()
    sys.exit()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, ball_sprites)
        self.radius = 7
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        self.x = random.randrange(7, width - 7)
        self.y = random.randrange(7, height - 7)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)

    def change_position(self):
        self.x = random.randrange(7, width - 7)
        self.y = random.randrange(7, height - 7)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, snake_sprites)
        x, y = 100, 100
        self.position = [x, y]
        self.width, self.height = 10, 10
        self.body = [(x, y), (x + self.width + 1, y),
                     (x + 2 * self.width + 2 * 1, y)]
        self.direction = 'left'
        for cube in self.body:
            pygame.draw.rect(screen, 'green', (cube[0], cube[1], self.width, self.height))
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'green', (100, 100, 10, 10))

    def update(self):
        if self.direction == 'left':
            self.position[0] -= SPEED
        elif self.direction == 'right':
            self.position[0] += SPEED
        elif self.direction == 'down':
            self.position[1] += SPEED
        elif self.direction == 'up':
            self.position[1] -= SPEED
        self.body.insert(0, (self.position[0], self.position[1]))
        if pygame.sprite.spritecollideany(self, ball_sprites):
            ball.change_position()
            global SCORE
            SCORE += 1
        else:
            self.body.pop()


Border(2, 2, width - 2, 2)
Border(2, height - 2, width - 2, height - 2)
Border(2, 2, 2, height - 2)
Border(width - 2, 2, width - 2, height - 2)
running = True
snake = Snake()
ball = Ball()
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_DOWN]:
            if snake.direction in 'rightleft':
                snake.direction = 'down'
        if keys[pygame.K_UP]:
            if snake.direction in 'rightleft':
                snake.direction = 'up'
        if keys[pygame.K_RIGHT]:
            if snake.direction in 'updown':
                snake.move = 'right'
        if keys[pygame.K_LEFT]:
            if snake.direction in 'updown':
                snake.direction = 'left'
    screen.fill((200, 200, 200))
    #horizontal_borders.draw(screen)
    #vertical_borders.draw(screen)
    #snake_sprites.update()
    snake_sprites.draw(screen)
    #ball_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()