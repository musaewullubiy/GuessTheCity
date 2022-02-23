import random

import pygame
import sys
import requests
from UT import *
import sqlite3


class Game:
    def __init__(self, city_name, menu=None):
        pygame.init()
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)

        self.city_name = city_name
        self.menu = menu
        self.running = True
        self.win_flag = False

        self.all_sprites = pygame.sprite.Group()
        con = sqlite3.connect('CitiesDB.sqlite')
        cur = con.cursor()
        all = cur.execute('SELECT * FROM Cities').fetchall()
        self.city_coords = [i[1] for i in all if i[0] == self.city_name][0]

    def run(self):
        pause = self.make_me_pause()
        self.get_photo()
        mouse_sprite = SpriteMouseLocation()
        while self.running:
            pause.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.get_photo()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    pause.click_check(mouse_sprite)
            pygame.display.flip()

    def close(self):
        self.running = False

    def get_photo(self):
        coords = ','.join([str(float(i) - random.randint(0, 69) / 1000) for i in self.city_coords.split(',')])
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&z=17&l={random.choice(['map', 'sat'])}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        self.screen.blit(pygame.transform.scale(pygame.image.load('map.png'), (900, 450 * 1.5)), (0, 0))

    def make_me_pause(self):
        pause = UPauseButton(self.all_sprites, None, self.screen)
        pause.set_gen_menu([pause.menu.close, self.close])
        pause.addButton('Продолжить', pause.menu.close)
        pause.addButton('Он угадал', [pause.menu.close, self.close])
        pause.addButton('Выход', sys.exit)
        return pause


if __name__ == '__main__':
    game = Game('Волгоград', UMenu)
    game.run()