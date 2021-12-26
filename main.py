import sys
import pygame
import os


FPS = 50
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')
box_image = load_image('move_box.png')
tile_width = tile_height = 50


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and level[self.pos_y][self.pos_x - 1] != '#':
                if level[self.pos_y][self.pos_x - 1] == '?':
                    if level[self.pos_y][self.pos_x - 2] != '#':
                        box.move(self.pos_x - 2, self.pos_y, 'left')
                        self.pos_x -= 1
                else:
                    self.pos_x -= 1
            elif event.key == pygame.K_RIGHT and level[self.pos_y][self.pos_x + 1] != '#':
                if level[self.pos_y][self.pos_x + 1] == '?':
                    if level[self.pos_y][self.pos_x + 2] != '#':
                        box.move(self.pos_x + 2, self.pos_y, 'right')
                        self.pos_x += 1
                else:
                    self.pos_x += 1
            elif event.key == pygame.K_UP and level[self.pos_y - 1][self.pos_x] != '#':
                if level[self.pos_y - 1][self.pos_x] == '?':
                    if level[self.pos_y - 2][self.pos_x] != '#':
                        box.move(self.pos_x + 2, self.pos_y, 'right')
                        self.pos_y -= 1
                else:
                    self.pos_y -= 1
            elif event.key == pygame.K_DOWN and level[self.pos_y + 1][self.pos_x] != '#':
                self.pos_y += 1
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = box_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)

    def move(self, pos_x, pos_y, direction):
        string = list(level[pos_y])
        if direction == 'left':
            string[pos_x + 1] = '.'
            string[pos_x] = '?'
            level[pos_y] = ''.join(string)
        elif direction == 'right':
            string[pos_x - 1] = '.'
            string[pos_x] = '?'
            level[pos_y] = ''.join(string)
        elif direction == 'up':
            string = list(level[pos_y])
            string[pos_x + 1] = '.'
            string[pos_x] = '?'
            level[pos_y] = ''.join(string)
        elif direction == 'down':
            string = list(level[pos_y])
            string[pos_x + 1] = '.'
            string[pos_x] = '?'
            level[pos_y] = ''.join(string)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = box_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)


def generate_level(level):
    new_box, new_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                new_box = Box(x, y)
    return new_box, new_player, x, y, level


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    flag = False
    screen.fill((0, 0, 0))
    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("Начать", True, (100, 255, 100))
    text_x = 184
    text_y = 50
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    rect = pygame.Rect(text_x - 10, text_y - 10, text_w + 20, text_h + 20)

    text2 = font.render("Скины", True, (100, 255, 100))
    text_x2 = 184
    text_y2 = 150
    text_w2 = text2.get_width()
    text_h2 = text2.get_height()
    screen.blit(text2, (text_x2, text_y2))
    rect2 = pygame.Rect(text_x2 - 10, text_y2 - 10, text_w2 + 20, text_h2 + 20)

    text3 = font.render("Настройки", True, (100, 255, 100))
    text_x3 = 184
    text_y3 = 250
    text_w3 = text3.get_width()
    text_h3 = text3.get_height()
    screen.blit(text3, (text_x3, text_y3))
    rect3 = pygame.Rect(text_x3 - 10, text_y3 - 10, text_w3 + 20, text_h3 + 20)

    text4 = font.render("Об игре", True, (100, 255, 100))
    text_x4 = 184
    text_y4 = 350
    text_w4 = text4.get_width()
    text_h4 = text4.get_height()
    screen.blit(text4, (text_x4, text_y4))
    rect4 = pygame.Rect(text_x4 - 10, text_y4 - 10, text_w4 + 20, text_h4 + 20)

    text5 = font.render("Выход", True, (100, 255, 100))
    text_x5 = 184
    text_y5 = 450
    text_w5 = text5.get_width()
    text_h5 = text5.get_height()
    screen.blit(text5, (text_x5, text_y5))
    rect5 = pygame.Rect(text_x5 - 10, text_y5 - 10, text_w5 + 20, text_h5 + 20)

    pygame.draw.rect(screen, 'green', rect, 1)
    pygame.draw.rect(screen, 'green', rect2, 1)
    pygame.draw.rect(screen, 'green', rect3, 1)
    pygame.draw.rect(screen, 'green', rect4, 1)
    pygame.draw.rect(screen, 'green', rect5, 1)
    while True:
        for event in pygame.event.get():
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT or pressed[0] and rect5.collidepoint(event.pos):
                terminate()
            elif event.type == pygame.KEYDOWN and flag:
                player.move(event)
                all_sprites.draw(screen)
                player_group.draw(screen)
                box_group.draw(screen)
            elif pressed[0] and rect.collidepoint(event.pos):
                all_sprites.draw(screen)
                player_group.draw(screen)
                box_group.draw(screen)
                flag = True
        pygame.display.flip()
        clock.tick(FPS)

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Сокобан')
clock = pygame.time.Clock()
box, player, level_x, level_y, level = generate_level(load_level('map.txt'))
start_screen()