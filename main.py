import pygame
from walls import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 700, 380

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
    def __init__(self, x, y, w, h, image_right, image_left, speed, x2, direction = True):
        super().__init__(x, y, w, h, image_right)
        self.image_right = self.image
        self.image_left = pygame.transform.scale(image_left, (w, h))
        self.speed = speed
        self.x1 = x
        self.x2 = x2
        self.direction = direction

    def move(self):
        if self.hitbox.x >= self.x2:
            self.hitbox.x = self.x2
            self.direction = False
            self.image = self.image_left
        elif self.hitbox.x <= self.x1:
            self.hitbox.x = self.x1
            self.direction = True
            self.image = self.image_right
        if self.direction:
            self.hitbox.x += self.speed
        else:
            self.hitbox.x -= self.speed

player_img = pygame.image.load('sprite1.png')
block_img = pygame.image.load('wall.png')
gold_img = pygame.image.load('treasure.png')
enemy_img = pygame.image.load('cyborg.png')
enemy_img_left = pygame.transform.flip(enemy_img, True, False)

block_size = 20
blocks = []

x, y = 0, 0

for row in lvl1:
    for block in row:
        if block == '1':
            blocks.append(Sprite(x, y, block_size, block_size, block_img))

        elif block == '2':
            treasure = Sprite(x, (y-20), 40, 40, gold_img)

        x += block_size
    x = 0
    y += block_size

font = pygame.font.SysFont('Arial', 90, True)
small_font = pygame.font.SysFont('Arial', 50, True)
lose = font.render('skill issue', True, (255, 0, 0))
win = font.render('let him cook', True, (0, 255, 0))
replay = small_font.render('press space to play again', True, (0, 0, 0))

game = True

pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

kick_sound = pygame.mixer.Sound('kick.ogg')
win_sound = pygame.mixer.Sound('win.ogg')

player = Player(20, 260, 30, 30, player_img, 3)
enemy = Enemy(60, 300, 30, 30, enemy_img, enemy_img_left, 3, 700)

finish = False
win_state = False

while game:
    window.blit(background, (0, 0))

    treasure.draw()

    for b in blocks:
        b.draw()

    if not finish:
        player.move(pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)
        player.draw()
        enemy.draw()
        enemy.move()

        for b in blocks:
            if player.hitbox.colliderect(b.hitbox):
                pygame.mixer.Sound.play(kick_sound)
                window.blit(lose, (140, 140))
                window.blit(replay, (40, 250))
                finish = True
                win_state = False

        if player.hitbox.colliderect(treasure.hitbox):
            pygame.mixer.Sound.play(win_sound)
            window.blit(win, (100, 140))
            window.blit(replay, (40, 250))
            finish = True
            win_state = True
    else:
        if win_state:
            window.blit(win, (100, 140))
        else:
            window.blit(lose, (140, 140))
        window.blit(replay, (40, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            player = Player(20, 260, 30, 30, player_img, 3)
            enemy = Enemy(60, 300, 30, 30, enemy_img, enemy_img_left, 3, 700)
            finish = False

    pygame.display.update()
    clock.tick(FPS)
