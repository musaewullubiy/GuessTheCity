from SupportFuncs import SpriteMouseLocation, load_image
import pygame
import sys
import os


class UWidget(pygame.sprite.Sprite):
    def __init__(self, menu):
        super(UWidget, self).__init__()
        self.menu = menu
        self.count = self.menu.addWidget(self)

    def pos_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.hover(True)
            return True
        else:
            self.hover(False)
            return False

    def hover(self, flag):
        pass

    def draw(self):
        pass

    def click_check(self, pos):
        pass

    def update(self):
        pass


class UButton(UWidget):
    def __init__(self, menu, func, text, num):
        super(UButton, self).__init__(menu)
        self.text = text
        self.flag = False
        self.func = func
        self.num = num
        self.font = pygame.font.Font('font/arial.ttf', 50)

    def draw(self, image_name='BigPurple.png'):
        if self.text:
            text_pg = self.font.render(self.text, True, (255, 255, 255))
            self.image = pygame.transform.scale(load_image('ui_images/' + image_name),
                                                (text_pg.get_width() + 40, text_pg.get_height() + 20))

            self.rect = self.image.get_rect()
            self.rect.x = self.menu.rect.w // 2 - self.rect.w // 2
            self.rect.y = self.menu.rect.h // 2 - self.rect.h // 2 + (text_pg.get_height() + 40) * self.num
            self.image.blit(text_pg, (20, 5))

    def hover(self, flag):
        if flag:
            self.draw(image_name='BigGreen.png')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            if type(self.func) == list:
                for i in self.func:
                    i()
            else:
                self.func()


class UMenu:
    def __init__(self, screen, general=True, color="purple", transparent=False):
        self.screen = screen
        self.general = general
        self.all_sprites = pygame.sprite.Group()
        self.rect = screen.get_rect()
        self.wids = list()
        self.color = color
        self.transparent = transparent
        self.MOUSECONSTANT = pygame.MOUSEBUTTONUP
        self.fon = False

    def mainloop(self):
        try:
            self.running = True
            mouse_sprite = SpriteMouseLocation()
            self.draw_all()
            pygame.display.flip()
            yes_flag = False
            while self.running:
                if not self.transparent:
                    self.screen.fill(self.color)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os._exit(0)
                        sys.exit(0)
                    elif event.type == self.MOUSECONSTANT:
                        if yes_flag:
                            mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                            for i in self.all_sprites:
                                i.click_check(mouse_sprite)
                            yes_flag = False
                    elif event.type == pygame.MOUSEMOTION:
                        yes_flag = True
                        mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                        for i in self.all_sprites:
                            i.pos_check(mouse_sprite)
                self.all_sprites.update()
                pygame.mouse.set_visible(True)
                if self.fon:
                    self.screen.blit(pygame.transform.scale(self.fon, (self.rect.w, self.rect.h)), (0, 0))
                self.all_sprites.draw(self.screen)
                pygame.display.flip()
        except SystemExit:
            pygame.quit()
            os._exit(0)

    def addWidget(self, wid):
        self.all_sprites.add(wid)
        self.wids.append(wid)
        return len(self.wids) - 1

    def draw_all(self):
        for wid in self.wids:
            wid.draw()

    def close(self):
        self.running = False

    def changeMouseConstantToClick(self, const):
        self.MOUSECONSTANT = const

    def setFon(self, image):
        self.fon = image


class ULevelsPlace(UWidget):
    def __init__(self, menu, func):
        super(ULevelsPlace, self).__init__(menu)
        self.checked = 0
        self.lvl_name = 'circle'
        self.levels = list()
        self.rows = 3
        self.cols = 3
        self.width = self.menu.rect.w
        self.height = self.menu.rect.h
        self.func = func
        self.update_func = False
        self.font = pygame.font.Font('font/arial.ttf', 20)

    def addLevel(self, image, text, name):
        self.levels.append((image, name, text))

    def draw(self):
        self.image = pygame.Surface((self.width, self.height - 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color('gray'), (0, 0, self.width, self.height))
        part_x = 10 if len(self.levels) == 0 else (self.rect.w - self.rows * 10 - 10) // self.rows
        self.cell_size_x = part_x
        self.cell_size_y = (self.rect.h - 10) // self.cols
        count = 0
        for i in range(self.rows):
            for j in range(1, self.cols + 1):
                if len(self.levels) > count:
                    image_lvl = self.levels[count][0]
                    text = self.levels[count][2]
                    self.image.blit(pygame.transform.scale(load_image('ui_images/back_image.png', -1),
                                                           (part_x, (self.rect.h - 10) // self.cols)),
                                    ((10 * j + part_x * (j - 1), 10 + (i * self.rect.h + 10) // self.cols - 10)))
                    image_lvl = pygame.transform.scale(image_lvl, (part_x, (self.rect.h - 120) // self.cols))
                    self.image.blit(image_lvl,
                                    (10 * j + part_x * (j - 1),
                                     10 + (i * self.rect.h + 10) // self.cols))

                    text_pg = self.font.render(text, True, (255, 255, 255))
                    self.image.blit(text_pg, (10 + 10 * (j + 1) + part_x * (j - 1),
                                              (((i + 1) * self.rect.h) // self.cols) - text_pg.get_height() - 5))
                    count += 1

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            cell_x = (pos.rect.x - 10) // self.cell_size_x
            cell_y = (pos.rect.y - 10) // self.cell_size_y
            if cell_x < 0 or cell_x >= self.rows or cell_y < 0 or cell_y >= self.cols:
                return
            self.func(self.levels[(cell_y * self.rows) + cell_x][1], self.menu)

    def change_size(self, width, height):
        self.width = width
        self.height = height

    def add_update_levels(self, func):
        self.update_func = func

    def update(self):
        if self.update_func:
            self.levels = list()
            self.update_func(self)
            self.draw()


class UMusicButton(UWidget):
    def __init__(self, menu, funcs):
        super(UMusicButton, self).__init__(menu)
        self.music_is = False
        self.funcs = funcs

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image(r'ui_images\ButtonsStyle10_05.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.menu.rect.h - self.rect.h - 10
        self.music_stat_draw()

    def hover(self, flag):
        if flag:
            self.draw(color='gray')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.music_is = not self.music_is
            self.do_music()
        self.music_stat_draw()

    def music_stat_draw(self):
        if self.music_is:
            pygame.draw.line(self.image, pygame.Color('red'), (100, 0), (0, 100), 10)

    def do_music(self):
        if self.music_is:
            self.funcs[1]()
        else:
            self.funcs[0]()
            self.draw()


class UBackButton(UWidget):
    def __init__(self, menu, pos, gen_menu):
        super(UBackButton, self).__init__(menu)
        self.pos = pos
        self.gen_menu = gen_menu

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image(r'ui_images\ButtonsStyle1_04.png', -1),
                                            (self.pos[2], self.pos[3]))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'black', self.pos)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            if type(self.gen_menu) == list:
                for i in self.gen_menu:
                    i()
            else:
                self.gen_menu()


class ULabel(UWidget):
    def __init__(self, menu, text, pos, color):
        super(ULabel, self).__init__(menu)
        self.text = text
        self.pos = pos
        self.color = color
        self.font = pygame.font.Font('font/arial.ttf', 30)

    def draw(self):
        self.image = pygame.Surface((self.menu.rect.w, self.menu.rect.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        text_pg = self.font.render(self.text, True, self.color)
        self.image.blit(text_pg, (self.pos[0] - text_pg.get_width() // 2, self.pos[1] - text_pg.get_height() // 2))


class UPauseMenu(UWidget):
    def __init__(self, menu):
        super(UPauseMenu, self).__init__(menu)
        self.buttons = list()
        self.labels = list()
        self.fon = False

    def draw(self):
        if self.fon:
            self.image = load_image('ui_images/BigPurple.png')
        else:
            self.image = pygame.Surface((300, 100 * len(self.buttons) + 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.menu.rect.w // 2 - self.rect.w // 2
        self.rect.y = self.menu.rect.h // 2 - self.rect.h // 2

    def addButton(self, text, func):
        btn = UButton(self.menu, func, text, len(self.buttons))
        self.buttons.append(btn)

    def addLabel(self, text, pos, color):
        label = ULabel(self.menu, text, pos, color)
        self.labels.append(label)


class UPauseButton(pygame.sprite.Sprite):
    def __init__(self, group, gen_menu, screen):
        super(UPauseButton, self).__init__(group)
        self.gen_menu = gen_menu
        self.screen = screen
        self.draw()
        self.buttons = list()
        self.menu = UMenu(self.screen, transparent=True)

    def draw(self):
        self.image = pygame.transform.scale(load_image(r'ui_images\ButtonsStyle10_02.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (0, 0))

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.go_to_pause()
            return True

    def go_to_pause(self):
        pygame.mixer.Channel(0).pause()
        ps_menu = UPauseMenu(self.menu)
        for text, func in self.buttons:
            ps_menu.addButton(text, func)
        pygame.mouse.set_visible(True)
        self.menu.mainloop()

    def addButton(self, text, func):
        self.buttons.append((text, func))

    def set_gen_menu(self, gen_menu):
        self.gen_menu = gen_menu


class UFinalWindow(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super(UFinalWindow, self).__init__(group)
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.buttons = list()
        self.labels = list()
        self.screen = screen
        self.menu = UMenu(self.screen, color='gray')

    def addButton(self, text, func):
        self.buttons.append((text, func))

    def addLabel(self, text, pos, color):
        self.labels.append((text, pos, color))

    def go(self):
        ps_menu = UPauseMenu(self.menu)
        for text, func in self.buttons:
            ps_menu.addButton(text, func)
        for text, pos, color in self.labels:
            ps_menu.addLabel(text, pos, color)
        pygame.mouse.set_visible(True)
        self.menu.changeMouseConstantToClick(pygame.MOUSEBUTTONDOWN)
        self.menu.mainloop()
