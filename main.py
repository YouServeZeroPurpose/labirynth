import pygame
from walls import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 700, 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Лабіринт')

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (window_width, window_height))

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.hitbox = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self, a, d, s, w):
        keys = pygame.key.get_pressed()
        if keys[a]:
            self.hitbox.x -= self.speed
        if keys[d]:
            self.hitbox.x += self.speed
        if keys[s]:
            self.hitbox.y += self.speed
        if keys[w]:
            self.hitbox.y -= self.speed

        self.hitbox.x = max(0, min(self.hitbox.x, window_width - self.hitbox.width))
        self.hitbox.y = max(0, min(self.hitbox.y, window_height - self.hitbox.height))

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self, a, d, s, w):
        keys = pygame.key.get_pressed()
        if keys[a]:
            self.hitbox.x -= self.speed
        if keys[d]:
            self.hitbox.x += self.speed
        if keys[s]:
            self.hitbox.y += self.speed
        if keys[w]:
            self.hitbox.y -= self.speed

        self.hitbox.x = max(0, min(self.hitbox.x, window_width - self.hitbox.width))
        self.hitbox.y = max(0, min(self.hitbox.y, window_height - self.hitbox.height))

blocks = []
block_size = 25

for row in lvl1:
    for block in row:
        if block == '1':
            blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
            block_x += block_size
        block_x = 0
        block_y += block_size


player = Player(0, 0, 50, 50, pygame.image.load('sprite1.png'), 5)

game = True

pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

while game:
    window.blit(background, (0, 0))

    for b in blocks:
        b.draw()
    player.move(pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)
    player.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.update()
    clock.tick(FPS)