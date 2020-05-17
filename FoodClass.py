import pygame
import random

class Food(object):
    def __init__(self, game, params):
        self.x_food = random.randrange(game.block_size, game.game_width - game.block_size, game.block_size)
        self.y_food = random.randrange(game.block_size, game.game_width - game.block_size, game.block_size)
        self.food_prev_x = params['game_width']/2
        self.food_prev_y = params['game_width']/2
        self.image = pygame.image.load('img/food2.png') 
        self.game = game
        if game.block_size != 20:
            self.image = pygame.transform.scale(self.image, (game.block_size, game.block_size))

    def food_coord(self,game,player):
        x_rand = random.randrange(game.block_size, game.game_width - game.block_size, game.block_size)
        y_rand = random.randrange(game.block_size, game.game_width - game.block_size, game.block_size)
        self.food_prev_x = self.x_food
        self.food_prev_y = self.y_food            
        self.x_food = x_rand
        self.y_food = y_rand
        if self.x_food == self.food_prev_x and self.y_food == self.food_prev_y:
            return self.food_coord(game, player)
        if[self.x_food, self.y_food] not in player.position:
            return self.x_food, self.y_food

        else:
            return self.food_coord(game,player)

    def display_food(self,x,y,game):
        self.game.gameDisplay.blit(self.image, (x,y))
