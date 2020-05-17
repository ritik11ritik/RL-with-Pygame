import pygame
import numpy as np

class Player(object):
    def __init__(self,game):
        self.clock = pygame.time.Clock()
        x = game.game_width/2
        y = game.game_width/2
        self.x = x
        self.y = y
        self.position = []
        self.position.append([self.x, self.y])
        self.food = 1
        self.eaten = False
        self.image = pygame.image.load('img/snakebody.png')
        self.img = pygame.image.load('img/SnakeHead.png')
        self.head = self.img
        self.x_change = game.block_size
        self.y_change = 0
        self.head_distance1 = 200
        self.head_distance2 = 200
        self.head_distance3 = 200
        if game.block_size != 20:
            self.img = pygame.transform.scale(self.img, (game.block_size, game.block_size))
            self.image = pygame.transform.scale(self.image, (game.block_size, game.block_size))
        

    def update_position(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 1:
                for i in range(0, self.food - 1):
                    self.position[i][0], self.position[i][1] = self.position[i+1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, move, x, y, game, food, agent):
        move_array = [self.x_change, self.y_change]

        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food += 1

        if np.array_equal(move, [1,0,0]):
            move_array = self.x_change, self.y_change

        elif np.array_equal(move, [0,1,0]) and self.y_change == 0:
            move_array = [0, self.x_change]
       
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            move_array = [-self.y_change, 0]
       
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            move_array = [0, -self.x_change]
       
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            move_array = [self.y_change, 0]

        self.x_change,self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change
    
        if self.x < game.block_size \
                or self.x >= game.game_width - game.block_size \
                or self.y < game.block_size \
                or self.y >= game.game_width - game.block_size \
                or [self.x,self.y] in self.position[:-1]:
            game.crash = True
        self.eat(self,food,game)
        self.update_position(self.x,self.y)
        
        if self.x_change > 0: #Moving in +x direction (Right)
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size):
                count = 0
                for j in range(0,self.food-2):
                    if ((self.position[-1][0]) + (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance1 = abs(i) #Distance straight
                        count = 1
                        break
                if count == 1:
                    break
                if (self.position[-1][0])+i == game.game_width - game.block_size:
                    self.head_distance1 = abs(i)
                
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] + (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance2 = abs(i) #Distance Right
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]+i == game.game_width - game.block_size:
                    self.head_distance2 = abs(i)
                    
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] - (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance3 = abs(i) #Distance Left
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]-i == 0:
                    self.head_distance3 = abs(i)
                
        if self.x_change < 0: #Moving in -x direction (Left)
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size):
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][0] - (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance1 = abs(i) #Distance straight                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][0]-i == 0:
                    self.head_distance1 = abs(i)
                
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] - (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance2 = abs(i) #Distance Right                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]-i == 0:
                    self.head_distance2 = abs(i)
                    
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] + (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance3 = abs(i) #Distance Left                        
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]+i == game.game_width - game.block_size:
                    self.head_distance3 = abs(i)
                
        if self.y_change > 0: #Moving in +y direction (Down)
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size):
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] + (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance1 = abs(i) #Distance straight                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]+i == game.game_width - game.block_size:
                    self.head_distance1 = abs(i)
                
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][0] - (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance2 = abs(i) #Distance Right                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][0]-i == 0:
                    self.head_distance2 = abs(i)
                    
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][0] + (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance3 = abs(i) #Distance Left                     
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][0]+i == game.game_width - game.block_size:
                    self.head_distance3 = abs(i)
                
        if self.y_change < 0: #Moving in -y direction (Up)
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size):
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][1] - (i) == self.position[j][1] and self.position[-1][0] == self.position[j][0]):
                        self.head_distance1 = abs(i) #Distance straight                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][1]-i == 0:
                    self.head_distance1 = abs(i)
                
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][0] + (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance2 = abs(i) #Distance Right                      
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][0]+i == game.game_width - game.block_size:
                    self.head_distance2 = abs(i)                    
            
            for i in range(game.block_size, game.game_width-game.block_size, game.block_size): 
                count = 0
                for j in range(0,self.food-2):
                    if (self.position[-1][0] - (i) == self.position[j][0] and self.position[-1][1] == self.position[j][1]):
                        self.head_distance3 = abs(i) #Distance Left                     
                        count = 1
                        break
                if count == 1:
                    break
                if self.position[-1][0]-i == 0:
                    self.head_distance3 = abs(i)

    def display_player(self, x, y, food, game, params):
        self.position[-1][0] = x
        self.position[-1][1] = y        
        if self.x_change > 0: #Right
            self.head = pygame.transform.rotate(self.img, 270)
        
        elif self.x_change < 0: #Left
            self.head = pygame.transform.rotate(self.img, 90)
            
        elif self.y_change < 0: #Up
            self.head = self.img
            
        elif self.y_change > 0: #Down
            self.head = pygame.transform.rotate(self.img, 180)

        if game.crash == False:
            game.gameDisplay.blit(self.head, (x,y))
            for i in range(1,food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))
            self.update_screen()
            self.clock.tick(params['FPS'])
            
    def update_screen(self):
        pygame.display.update()
        pygame.event.pump()
        
    def eat(self, player, food, game):
        if player.x == food.x_food and player.y == food.y_food:
            food.food_coord(game, player)
            player.eaten = True
            game.score += 1
