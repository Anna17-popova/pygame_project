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
        radius = 7
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        x = random.randrange(7, width - 7)
        y = random.randrange(7, height - 7)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)


Border(2, 2, width - 2, 2)
Border(2, height - 2, width - 2, height - 2)
Border(2, 2, 2, height - 2)
Border(width - 2, 2, width - 2, height - 2)
running = True
ball = Ball()
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((200, 200, 200))
    horizontal_borders.draw(screen)
    vertical_borders.draw(screen)
    ball_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()