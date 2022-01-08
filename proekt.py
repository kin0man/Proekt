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
destination_image = load_image('destination.png')
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
        global all_sprites, tiles_group, player_group, box_group, destination, box, player, level_x, level_y, level
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
                        box.move(self.pos_x, self.pos_y - 2, 'up')
                        self.pos_y -= 1
                else:
                    self.pos_y -= 1
            elif event.key == pygame.K_DOWN and level[self.pos_y + 1][self.pos_x] != '#':
                if level[self.pos_y + 1][self.pos_x] == '?':
                    if level[self.pos_y + 2][self.pos_x] != '#':
                        box.move(self.pos_x, self.pos_y + 2, 'down')
                        self.pos_y += 1
                else:
                    self.pos_y += 1
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)
        if box.pos_x == destination.pos_x and box.pos_y == destination.pos_y:
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            box_group = pygame.sprite.Group()
            start_screen()
            destination, box, player, level_x, level_y, level = generate_level(load_level('map.txt'))


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
            string[pos_x] = '?'
            string2 = list(level[pos_y + 1])
            string2[pos_x] = '.'
            level[pos_y] = ''.join(string)
            level[pos_y + 1] = ''.join(string2)
        elif direction == 'down':
            string = list(level[pos_y])
            string[pos_x] = '?'
            string2 = list(level[pos_y - 1])
            string2[pos_x] = '.'
            level[pos_y] = ''.join(string)
            level[pos_y - 1] = ''.join(string2)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = box_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)


class Destination(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = destination_image
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
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                new_destination = Destination(x, y)
    return new_destination, new_box, new_player, x, y, level


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global all_sprites, tiles_group, player_group, box_group, destination, box, player, level_x, level_y, level
    flag = False
    screen.fill((0, 0, 0))
    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("Начать", True, 'purple')
    text_x = 184
    text_y = 132
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    rect = pygame.Rect(text_x - 10, text_y - 10, text_w + 20, text_h + 20)

    font1 = pygame.font.Font(None, 125)
    font1.set_italic(True)
    text1 = font1.render("Сокобан", True, 'Peru')
    text_x1 = 111
    text_y1 = 27
    screen.blit(text1, (text_x1, text_y1))

    text2 = font.render("Скины", True, 'purple')
    text_x2 = 188
    text_y2 = 232
    text_w2 = text2.get_width()
    text_h2 = text2.get_height()
    screen.blit(text2, (text_x2, text_y2))
    rect2 = pygame.Rect(text_x2 - 10, text_y2 - 10, text_w2 + 20, text_h2 + 20)

    text3 = font.render("Настройки", True, 'purple')
    text_x3 = 120
    text_y3 = 332
    text_w3 = text3.get_width()
    text_h3 = text3.get_height()
    screen.blit(text3, (text_x3, text_y3))
    rect3 = pygame.Rect(text_x3 - 10, text_y3 - 10, text_w3 + 20, text_h3 + 20)

    text4 = font.render("Об игре", True, 'purple')
    text_x4 = 168
    text_y4 = 432
    text_w4 = text4.get_width()
    text_h4 = text4.get_height()
    screen.blit(text4, (text_x4, text_y4))
    rect4 = pygame.Rect(text_x4 - 10, text_y4 - 10, text_w4 + 20, text_h4 + 20)

    text5 = font.render("Выход", True, 'purple')
    text_x5 = 181
    text_y5 = 560
    text_w5 = text5.get_width()
    text_h5 = text5.get_height()
    screen.blit(text5, (text_x5, text_y5))
    rect5 = pygame.Rect(text_x5 - 10, text_y5 - 10, text_w5 + 20, text_h5 + 20)

    pygame.draw.rect(screen, 'green', rect, 3)
    pygame.draw.rect(screen, 'green', rect2, 3)
    pygame.draw.rect(screen, 'green', rect3, 3)
    pygame.draw.rect(screen, 'green', rect4, 3)
    pygame.draw.rect(screen, 'green', rect5, 3)

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)
    while True:
        for event in pygame.event.get():
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT or pressed[0] and rect5.collidepoint(event.pos):
                terminate()
            elif event.type == pygame.KEYDOWN and flag:
                steps.play()
                player.move(event)
                all_sprites.draw(screen)
                box_group.draw(screen)
                player_group.draw(screen)
            elif pressed[0] and rect.collidepoint(event.pos):
                screen.fill('white')
                home = load_image('home.png')
                rect_h = pygame.Rect(0, 600, 50, 50)
                screen.blit(home, (0, 600))
                ret = load_image('ret.png')
                rect_r = pygame.Rect(550, 600, 50, 50)
                screen.blit(ret, (550, 600))
                pygame.draw.rect(screen, 'black', rect_h, 1)
                pygame.draw.rect(screen, 'black', rect_r, 1)
                destination, box, player, level_x, level_y, level = generate_level(load_level('map.txt'))
                all_sprites.draw(screen)
                player_group.draw(screen)
                box_group.draw(screen)
                flag = True
            elif pressed[0] and rect_h.collidepoint(event.pos):
                all_sprites = pygame.sprite.Group()
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                box_group = pygame.sprite.Group()
                start_screen()
                destination, box, player, level_x, level_y, level = generate_level(load_level('map.txt'))
                start_screen()
            elif pressed[0] and rect_r.collidepoint(event.pos):
                all_sprites = pygame.sprite.Group()
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                box_group = pygame.sprite.Group()
                destination, box, player, level_x, level_y, level = generate_level(load_level('map.txt'))
                all_sprites.draw(screen)
                box_group.draw(screen)
                player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

pygame.init()
fullname = os.path.join('data', 'fon_music.mp3')
pygame.mixer.music.load(fullname)

fullname = os.path.join('data', 'steps.mp3')
steps = pygame.mixer.Sound(fullname)

size = width, height = 600, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Сокобан')
clock = pygame.time.Clock()
start_screen()