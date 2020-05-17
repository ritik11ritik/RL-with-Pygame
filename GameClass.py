import pygame
from SnakeClass import Player
from FoodClass import Food

class Game:
    def __init__(self, params):
        pygame.display.set_caption("Snake RL")
        self.game_width = params['game_width']
        self.game_height = params['game_height']
        self.block_size = params['block_size']
        self.gameDisplay = pygame.display.set_mode((self.game_width, self.game_height))
        self.crash = False
        self.player = Player(self)
        self.food = Food(self, params)
        self.score = 0