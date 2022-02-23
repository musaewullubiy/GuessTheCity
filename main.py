import sqlite3

import pygame
import sys
from SupportFuncs import load_image
from UT import UMenu, ULevelsPlace, UBackButton, UButton
from Game import Game


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2, color='Gray', transparent=False)
    menu_lvl.changeMouseConstantToClick(pygame.MOUSEBUTTONDOWN)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    con = sqlite3.connect('CitiesDB.sqlite')
    cur = con.cursor()
    levels = cur.execute('SELECT * FROM Cities').fetchall()
    for i in levels:
        levels_place.addLevel(load_image(i[2]), i[0], i[0])
    UBackButton(menu_lvl, (0, 450, 50, 50), menu_lvl.close)
    menu_lvl.mainloop()


def start_the_game(lvl_name, menu):
    game = Game(lvl_name, menu)
    game.run()


def main():
    pygame.init()
    pygame.display.set_caption("Guess The City")
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    menu = UMenu(screen)
    menu.setFon(load_image('ui_images/fon.png'))
    UButton(menu, go_to_levels, 'Старт', 0)
    UButton(menu, [sys.exit], 'Выход', 1)
    pygame.display.flip()
    menu.mainloop()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        sys.exit(0)