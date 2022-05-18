from typing import Mapping
import pygame

from jeu import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()


#collision a faire sur tiled avec le type "col"