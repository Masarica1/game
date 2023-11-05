import pygame
import csv

# window setting
window_w = 1280
window_h = 960
window = pygame.display.set_mode((1280, 960))

table = []
with open('setting/gene.csv', 'r', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        table.append(row)
    pass

# clock setting
clock = pygame.time.Clock()
event_1 = pygame.USEREVENT + 1
pygame.time.set_timer(event_1, 1000)


class Player(pygame.sprite.Sprite):
    serial: int = 0
    record: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((75, 75))
        self.rect = self.image.get_rect()
        self.vel = 10
        self.last_time = 0
        self.gene = []

        # gene put
        self.serial_n: int = Player.serial
        Player.serial += 1
        self.gene = table[self.serial_n]

        self.rect.bottom = window_h
        self.rect.centerx = window_w / 2

        self.image.fill((128, 128, 128))

    def update(self):
        if self.gene.pop() == '1':
            self.rect.x += self.vel
        else:
            self.rect.x -= self.vel

        if self.out_check():
            Player.record[self.serial_n] = self.last_time
            # noinspection PyTypeChecker
            Entity.player_group.remove(self)

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
        self.image = pygame.Surface((75, 75))
        self.rect = self.image.get_rect()
        self.vel = vel

        self.image.fill((255, 0, 0))
        self.rect.y = 0
        self.rect.x = Enemy.init_loc[Enemy.init_number]

        Enemy.init_number += 1

    def update(self):
        self.rect.y += self.vel

        if self.rect.y > window_h:
            self.__init__(self.vel)


class Entity:
    player_group = pygame.sprite.Group()
    for _ in range(10):
        # noinspection PyTypeChecker
        player_group.add(Player())

    enemy_group = pygame.sprite.Group()
    for i in range(5, 13):
        # noinspection PyTypeChecker
        enemy_group.add(Enemy(i))


def init():
    Player.serial = 0
    Player.record = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    Enemy.init_number = 0
    Enemy.init_loc = []

    with open('setting/gene.csv', 'r', newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            table.append(row)
        pass

    Entity.player_group = pygame.sprite.Group()
    for _ in range(10):
        # noinspection PyTypeChecker
        Entity.player_group.add(Player())

    Entity.enemy_group = pygame.sprite.Group()
    for i in range(5, 15):
        # noinspection PyTypeChecker
        Entity.enemy_group.add(Enemy(i))


def simulation():
    pygame.init()

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

        window.fill((255, 255, 255))

        Entity.player_group.update()
        Entity.player_group.draw(window)

        Entity.enemy_group.update()
        Entity.enemy_group.draw(window)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    return Player.record
