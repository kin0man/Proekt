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
player_image = load_image('TV.png')
box_image = load_image('move_box.png')
destination_image = load_image('destination.png')
tile_width = tile_height = 50

destinations = []
boxes = []
boxes_coords = []

sound = 'sound_on.png'


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
            tile_width * self.pos_x, tile_height * self.pos_y)

    def move(self, event):
        global all_sprites, tiles_group, player_group, box_group, player, level_x, level_y, level, boxes, boxes_coords
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and level[self.pos_y][self.pos_x - 1] != '#' and not \
                    (level[self.pos_y][self.pos_x - 1] == '?' and level[self.pos_y][self.pos_x - 2] == '?'):
                if level[self.pos_y][self.pos_x - 1] == '?':
                    if level[self.pos_y][self.pos_x - 2] != '#':
                        boxes[boxes_coords.index((self.pos_x - 1, self.pos_y))].move(self.pos_x - 2, self.pos_y, 'left')
                        boxes_coords[boxes_coords.index((self.pos_x - 1, self.pos_y))] = (self.pos_x - 2, self.pos_y)
                        self.pos_x -= 1
                else:
                    self.pos_x -= 1
            elif event.key == pygame.K_RIGHT and level[self.pos_y][self.pos_x + 1] != '#' and not \
                    (level[self.pos_y][self.pos_x + 1] == '?' and level[self.pos_y][self.pos_x + 2] == '?'):
                if level[self.pos_y][self.pos_x + 1] == '?':
                    if level[self.pos_y][self.pos_x + 2] != '#':
                        boxes[boxes_coords.index((self.pos_x + 1, self.pos_y))].move(self.pos_x + 2, self.pos_y,
                                                                                     'right')
                        boxes_coords[boxes_coords.index((self.pos_x + 1, self.pos_y))] = (self.pos_x + 2, self.pos_y)
                        self.pos_x += 1
                else:
                    self.pos_x += 1
            elif event.key == pygame.K_UP and level[self.pos_y - 1][self.pos_x] != '#' and not \
                    (level[self.pos_y - 1][self.pos_x] == '?' and level[self.pos_y - 2][self.pos_x] == '?'):
                if level[self.pos_y - 1][self.pos_x] == '?':
                    if level[self.pos_y - 2][self.pos_x] != '#':
                        boxes[boxes_coords.index((self.pos_x, self.pos_y - 1))].move(self.pos_x, self.pos_y - 2, 'up')
                        boxes_coords[boxes_coords.index((self.pos_x, self.pos_y - 1))] = (self.pos_x, self.pos_y - 2)
                        self.pos_y -= 1
                else:
                    self.pos_y -= 1
            elif event.key == pygame.K_DOWN and level[self.pos_y + 1][self.pos_x] != '#' and not \
                    (level[self.pos_y + 1][self.pos_x] == '?' and level[self.pos_y + 2][self.pos_x] == '?'):
                if level[self.pos_y + 1][self.pos_x] == '?':
                    if level[self.pos_y + 2][self.pos_x] != '#':
                        boxes[boxes_coords.index((self.pos_x, self.pos_y + 1))].move(self.pos_x, self.pos_y + 2, 'down')
                        boxes_coords[boxes_coords.index((self.pos_x, self.pos_y + 1))] = (self.pos_x, self.pos_y + 2)
                        self.pos_y += 1
                else:
                    self.pos_y += 1
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        boxes_coords.append((pos_x, pos_y))
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
        destinations.append((pos_x, pos_y))
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
                boxes.append(Box(x, y))
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                Destination(x, y)
    return new_player, x, y, level


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global all_sprites, tiles_group, player_group, box_group, player, box_image, \
        level_x, level_y, level, boxes, boxes_coords, destinations, sound, tile_images, player_image, Music
    flag_game = False
    flag_endgame = False
    flag_levels = False
    flag_rules = False
    flag_main_menu = True
    flag_skins = False
    flag_music = False
    flag_name_map = 0
    fon = load_image('fon.png')
    screen.blit(fon, (0, 0))

    screen.blit(load_image('title.png'), (0, -10))

    screen.blit(load_image('start.png'), (200, 145))
    rect = pygame.Rect(200, 145, 201, 66)

    screen.blit(load_image('music.png'), (194, 220))
    rect2 = pygame.Rect(194, 220, 212, 76)

    screen.blit(load_image('skins.png'), (198, 295))
    rect3 = pygame.Rect(198, 295, 184, 69)

    screen.blit(load_image('info.png'), (193, 370))
    rect4 = pygame.Rect(193, 370, 215, 83)

    screen.blit(load_image('exit.png'), (209, 445))
    rect5 = pygame.Rect(209, 445, 183, 76)

    screen.blit(load_image(sound), (1, 579))
    rect_sound = pygame.Rect(1, 579, 70, 70)

    boxes = []
    boxes_coords = []
    destinations = []
    if Music == 'tin' and sound == 'sound_on.png':
        fullname = os.path.join('data', 'main_tb_music.mp3')
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    while True:
        for event in pygame.event.get():
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT or pressed[0] and rect5.collidepoint(event.pos) and flag_main_menu:
                terminate()
            elif event.type == pygame.KEYDOWN and flag_game:
                steps.play()
                player.move(event)
                all_sprites.draw(screen)
                box_group.draw(screen)
                player_group.draw(screen)
                if sorted(boxes_coords) == sorted(destinations):
                    screen.blit(load_image('end_game.jpg'), (0, 0))
                    screen.blit(load_image('back.png'), (176, 480))
                    screen.blit(load_image('congrats.png'), (6, 60))
                    flag_game = False
                    flag_endgame = True
                    rect_endgame = pygame.Rect(176, 480, 248, 111)
            if pressed[0] and rect_sound.collidepoint(event.pos) and flag_main_menu:
                if sound == 'sound_on.png':
                    sound = 'sound_off.png'
                    pygame.mixer.music.set_volume(0)
                else:
                    sound = 'sound_on.png'
                    pygame.mixer.music.set_volume(0.15)
                start_screen()
                screen.blit(load_image(sound), (1, 579))
            if flag_music:
                if pressed[0] and rect_def.collidepoint(event.pos):
                    if sound == 'sound_on.png':
                        Music = 'def'
                        fullname = os.path.join('data', 'fon_music.mp3')
                        pygame.mixer.music.load(fullname)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.15)
                if pressed[0] and rect_tin.collidepoint(event.pos):
                    if sound == 'sound_on.png':
                        Music = 'tin'
                        fullname = os.path.join('data', 'main_tb_music.mp3')
                        pygame.mixer.music.load(fullname)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.4)
                if pressed[0] and rect_eve.collidepoint(event.pos):
                    Music = 'eve'
                if pressed[0] and rect_cyb.collidepoint(event.pos):
                    Music = 'cyb'
                if pressed[0] and rect_lof.collidepoint(event.pos):
                    Music = 'lof'
                if pressed[0] and rect_mix.collidepoint(event.pos):
                    Music = 'mix'
                if pressed[0] and rect_har.collidepoint(event.pos):
                    Music = 'har'
            if flag_levels:
                if pressed[0] and rect_level1.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('box.png'),
                        'empty': load_image('grass.png')
                    }
                    box_image = load_image('move_box.png')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('1_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map1.txt'))
                    flag_name_map = 1
                elif pressed[0] and rect_level2.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('box.png'),
                        'empty': load_image('grass.png')
                    }
                    box_image = load_image('move_box.png')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('2_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map2.txt'))
                    flag_name_map = 2
                elif pressed[0] and rect_level3.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('stena.png'),
                        'empty': load_image('pol.png')
                    }
                    box_image = load_image('move_box.png')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('3_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map3.txt'))
                    flag_name_map = 3
                elif pressed[0] and rect_level4.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('stena.png'),
                        'empty': load_image('pol.png')
                    }
                    box_image = load_image('move_box.png')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('4_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map4.txt'))
                    flag_name_map = 4
                elif pressed[0] and rect_level5.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('sand_wall.png'),
                        'empty': load_image('sand.jpg')
                    }
                    box_image = load_image('sand_box.jpg')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('5_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map5.txt'))
                    flag_name_map = 5
                elif pressed[0] and rect_level6.collidepoint(event.pos):
                    tile_images = {
                        'wall': load_image('ice.png'),
                        'empty': load_image('snow.jpg')
                    }
                    box_image = load_image('snow_box.png')
                    screen.fill((41, 49, 51))
                    screen.blit(load_image('6_level.png'), (234, 600))
                    player, level_x, level_y, level = generate_level(load_level('map6.txt'))
                    flag_name_map = 6
                if pressed[0] and (rect_level1.collidepoint(event.pos) or rect_level2.collidepoint(event.pos) or \
                                   rect_level3.collidepoint(event.pos) or rect_level4.collidepoint(event.pos) or \
                                   rect_level5.collidepoint(event.pos) or rect_level6.collidepoint(event.pos)):
                    home = load_image('home.png')
                    rect_h = pygame.Rect(0, 600, 50, 50)
                    screen.blit(home, (0, 600))
                    ret = load_image('ret.png')
                    rect_r = pygame.Rect(550, 600, 50, 50)
                    screen.blit(ret, (550, 600))
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    box_group.draw(screen)
                    flag_game = True
                    flag_levels = False
            if pressed[0] and flag_main_menu and rect.collidepoint(event.pos):
                if Music == 'tin' and sound == 'sound_on.png':
                    fullname = os.path.join('data', 'levels_tb_music.mp3')
                    pygame.mixer.music.load(fullname)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.4)

                screen.blit(fon, (0, 0))
                screen.blit(load_image('levels.png'), (0, 0))
                screen.blit(load_image('level_1.png'), (60, 150))
                screen.blit(load_image('level_2.png'), (230, 150))
                screen.blit(load_image('level_3.png'), (400, 150))
                screen.blit(load_image('level_4.png'), (60, 350))
                screen.blit(load_image('level_5.png'), (230, 350))
                screen.blit(load_image('level_6.png'), (400, 350))
                screen.blit(load_image('home_2.png'), (243, 535))
                rect_h1 = pygame.Rect(243, 535, 115, 115)
                rect_level1 = pygame.Rect(60, 150, 140, 140)
                rect_level2 = pygame.Rect(230, 150, 140, 140)
                rect_level3 = pygame.Rect(400, 150, 140, 140)
                rect_level4 = pygame.Rect(60, 350, 140, 140)
                rect_level5 = pygame.Rect(230, 350, 140, 140)
                rect_level6 = pygame.Rect(400, 350, 140, 140)
                flag_levels = True
                flag_main_menu = False
            if pressed[0] and rect4.collidepoint(event.pos) and flag_main_menu:
                if Music == 'tin' and sound == 'sound_on.png':
                    fullname = os.path.join('data', 'info_and_skins_tb_music.mp3')
                    pygame.mixer.music.load(fullname)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.25)

                screen.blit(fon, (0, 0))
                screen.blit(load_image('rules_1.png'), (0, 0))
                screen.blit(load_image('rules.png'), (0, 50))
                screen.blit(load_image('rules_2.png'), (0, 225))
                screen.blit(load_image('rules_3.png'), (0, 325))
                screen.blit(load_image('home_2.png'), (243, 535))
                rect_h1 = pygame.Rect(243, 535, 115, 115)
                flag_rules = True
                flag_main_menu = False
            if pressed[0] and rect3.collidepoint(event.pos) and flag_main_menu:
                if Music == 'tin' and sound == 'sound_on.png':
                    fullname = os.path.join('data', 'info_and_skins_tb_music.mp3')
                    pygame.mixer.music.load(fullname)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.25)

                flag_main_menu = False
                flag_skins = True
                screen.blit(fon, (0, 0))
                screen.blit(load_image('home_2.png'), (243, 535))
                rect_h1 = pygame.Rect(243, 535, 115, 115)
                screen.blit(load_image('skins_1.png'), (171, 20))
                for i in range(5):
                    screen.blit(load_image('ramka.png'), (50 + 100 * i, 275))
                screen.blit(load_image('TV_100.png'), (56, 280))
                rect_TV = pygame.Rect(56, 280, 100, 100)
                screen.blit(load_image('pinguin_100.png'), (158, 280))
                rect_pinguin = pygame.Rect(150, 275, 100, 100)
                screen.blit(load_image('akatsuki_100.png'), (248, 275))
                rect_akatsuki = pygame.Rect(250, 275, 100, 100)
                screen.blit(load_image('ironman_100.png'), (360, 285))
                rect_ironman = pygame.Rect(350, 275, 100, 100)
                screen.blit(load_image('spider-man_100.png'), (455, 285))
                rect_spiderman = pygame.Rect(450, 275, 100, 100)
            if pressed[0] and rect2.collidepoint(event.pos) and flag_main_menu:
                flag_main_menu = False
                flag_music = True
                screen.blit(fon, (0, 0))
                screen.blit(load_image('home_2.png'), (243, 535))
                rect_h1 = pygame.Rect(243, 535, 115, 115)
                screen.blit(load_image('music_title.png'), (0, -20))

                screen.blit(load_image('default.png'), (222, 120))
                rect_def = pygame.Rect(222, 120, 156, 50)
                screen.blit(load_image('tiny_bunny.png'), (209, 180))
                rect_tin = pygame.Rect(209, 180, 183, 50)
                screen.blit(load_image('lofi.png'), (250, 240))
                rect_lof = pygame.Rect(250, 240, 101, 50)
                screen.blit(load_image('mix.png'), (268, 300))
                rect_mix = pygame.Rect(268, 300, 64, 50)
                screen.blit(load_image('harry_potter.png'), (225, 360))
                rect_har = pygame.Rect(225, 360, 150, 50)
                screen.blit(load_image('everlasting_summer.png'), (205, 420))
                rect_eve = pygame.Rect(205, 420, 190, 50)
                screen.blit(load_image('cyberpunk.png'), (161, 480))
                rect_cyb = pygame.Rect(161, 480, 278, 50)
            if flag_game:
                if pressed[0] and rect_h.collidepoint(event.pos):
                    all_sprites = pygame.sprite.Group()
                    tiles_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
                    start_screen()
                elif pressed[0] and rect_r.collidepoint(event.pos):
                    all_sprites = pygame.sprite.Group()
                    tiles_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
                    boxes = []
                    boxes_coords = []
                    destinations = []
                    player, level_x, level_y, level = \
                        generate_level(load_level(f'map{flag_name_map}.txt'))
                    all_sprites.draw(screen)
                    box_group.draw(screen)
                    player_group.draw(screen)
            if flag_skins:
                if pressed[0] and rect_TV.collidepoint(event.pos):
                    player_image = load_image('TV.png')
                elif pressed[0] and rect_pinguin.collidepoint(event.pos):
                    player_image = load_image('pinguin.png')
                elif pressed[0] and rect_akatsuki.collidepoint(event.pos):
                    player_image = load_image('akatsuki.png')
                elif pressed[0] and rect_ironman.collidepoint(event.pos):
                    player_image = load_image('ironman.png')
                elif pressed[0] and rect_spiderman.collidepoint(event.pos):
                    player_image = load_image('spider-man.png')

            if flag_rules or flag_levels or flag_music or flag_skins:
                if pressed[0] and rect_h1.collidepoint(event.pos):
                    all_sprites = pygame.sprite.Group()
                    tiles_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
                    start_screen()
            if flag_endgame:
                if pressed[0] and rect_endgame.collidepoint(event.pos):
                    screen.blit(fon, (0, 0))
                    screen.blit(load_image('levels.png'), (0, 0))
                    screen.blit(load_image('level_1.png'), (60, 150))
                    screen.blit(load_image('level_2.png'), (230, 150))
                    screen.blit(load_image('level_3.png'), (400, 150))
                    screen.blit(load_image('level_4.png'), (60, 350))
                    screen.blit(load_image('level_5.png'), (230, 350))
                    screen.blit(load_image('level_6.png'), (400, 350))
                    screen.blit(load_image('home_2.png'), (243, 535))
                    rect_h1 = pygame.Rect(243, 535, 115, 115)
                    rect_level1 = pygame.Rect(60, 150, 140, 140)
                    rect_level2 = pygame.Rect(230, 150, 140, 140)
                    rect_level3 = pygame.Rect(400, 150, 140, 140)
                    rect_level4 = pygame.Rect(60, 350, 140, 140)
                    rect_level5 = pygame.Rect(230, 350, 140, 140)
                    rect_level6 = pygame.Rect(400, 350, 140, 140)
                    flag_levels = True
                    flag_endgame = False
                    all_sprites = pygame.sprite.Group()
                    tiles_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
Music = 'fon_music.mp3'
fullname = os.path.join('data', Music)
Music = 'def'
pygame.mixer.music.load(fullname)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)

fullname = os.path.join('data', 'steps.mp3')
steps = pygame.mixer.Sound(fullname)
steps.set_volume(0.15)

size = width, height = 600, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Сокобан')
clock = pygame.time.Clock()
start_screen()