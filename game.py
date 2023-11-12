import random

import pygame
import csv

# window setting
window_w = 1280
window_h = 900
window = pygame.display.set_mode((1280, 960))


def set_table():
    _table = []
    with open('setting/gene.csv', 'r', newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            _table.append(row)

    return _table


# table setting
table = set_table()

# clock setting
clock = pygame.time.Clock()
event_1 = pygame.USEREVENT + 1
pygame.time.set_timer(event_1, 5)


class Player(pygame.sprite.Sprite):
    serial: int = 0
    record: list[int] = [0 * i for i in range(1)]

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('image/player.png')
        self.rect = self.image.get_rect()
        self.vel = 10
        self.last_time = 0
        self.gene = []
        self.surface = pygame.image.load('image/player.png')

        # gene put
        self.serial_n: int = Player.serial
        Player.serial += 1
        self.gene = table[self.serial_n]

        self.rect.bottom = window_h
        self.rect.centerx = window_w / 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 10
        if keys[pygame.K_d]:
            self.rect.x += 10

    def out_check(self):
        if (self.rect.x < 0) or (self.rect.right > window_w):
            return True
        if pygame.sprite.spritecollide(self, Entity.enemy_group, False):
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    init_number: int = 0
    init_loc: list[int] = []
    with open('setting/enemy_loc.csv', 'r', newline='') as file:
        r = csv.reader(file)
        for row in r:
            init_loc.append(int(row[0]))

    def __init__(self, vel: int):
        super().__init__()
        self.image = random.choice([pygame.image.load('image/enemy1.jpg'), pygame.image.load('image/enemy2.jpg')])
        self.rect = self.image.get_rect()
        self.vel = vel

        self.rect.y = 0
        self.rect.x = Enemy.init_loc[Enemy.init_number]

        Enemy.init_number += 1

    def update(self):
        self.rect.y += self.vel

        if self.rect.y > window_h:
            self.__init__(self.vel)


class Entity:
    player_group = pygame.sprite.Group()
    for _ in range(1):
        # noinspection PyTypeChecker
        player_group.add(Player())

    enemy_group = pygame.sprite.Group()
    for i in range(5, 13):
        # noinspection PyTypeChecker
        enemy_group.add(Enemy(i))


def initation():
    # game system
    global window
    window = pygame.display.set_mode((window_w, window_h))

    # gene update
    global table
    table = set_table()

    # player init
    Player.serial = 0
    Player.record = [0 * i for i in range(1)]
    Entity.player_group = pygame.sprite.Group()

    for _ in range(1):
        # noinspection PyTypeChecker
        Entity.player_group.add(Player())

    # enemy init
    Enemy.init_number = 0

    Entity.enemy_group = pygame.sprite.Group()
    for i in range(5, 13):
        # noinspection PyTypeChecker
        Entity.enemy_group.add(Enemy(i))


def simulation():
    initation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == event_1:
                for player in Entity.player_group:
                    player.last_time += 1

        if len(Entity.player_group) == 0:
            running = False

        background = pygame.image.load('image/background.jpg')
        window.blit(background, background.get_rect())

        Entity.player_group.update()
        Entity.player_group.draw(window)

        Entity.enemy_group.update()
        Entity.enemy_group.draw(window)

        pygame.display.update()
        clock.tick(60)

    print(1)
    return Player.record
