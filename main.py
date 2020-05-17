import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from DQN import DQNAgent
from random import randint
from keras.utils import to_categorical
from GameClass import Game

def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/35
    params['learning_rate'] = 0.0005
    params['layer1'] = 256   # neurons in the Layer 1 
    params['layer2'] = 128   # neurons in the layer 2
    params['layer3'] = 64   # neurons in the layer 3 
    params['episodes'] = 1000            
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'Weights/weights.hdf5'
    params['load_weights'] = True
    params['train'] = True
    params['display'] = True
    params['game_width'] = 600
    params['game_height'] = params['game_width'] + 100
    params['white'] = (255,255,255)
    params['black'] = (0,0,0)
    params['green'] = (0,192,0)
    params['FPS'] = 30
    params['block_size'] = 20
    params['cf'] = 1
    params['cp'] = "Snake"
    return params

def get_record(score, record):
    if score>=record:
        return score
    else:
        return record

def display(player, food, game, record, game_counter, total_reward, params):
    game.gameDisplay.fill(params['white'])
    display_ui(game, game.score, record, game_counter, total_reward)
    food.display_food(food.x_food, food.y_food, game)
    player.display_player(player.position[-1][0], player.position[-1][1], player.food, game, params)

def display_ui(game, score, record, game_counter, total_reward):
    params = define_parameters()
    smallfont = pygame.font.SysFont("comicsansms", 25)
    text_score = smallfont.render("SCORE: "+str(score), True, params['black'])
    text_highest = smallfont.render("HIGHEST SCORE: "+str(record), True, params['black'])
    game_counter_text = smallfont.render("GAME NUMBER: " + str(game_counter+1), True, params['black'])
    reward_text = smallfont.render("REWARD: " + str(total_reward),True, params['black'])
    game.gameDisplay.blit(text_score, (game.game_width*0, game.game_height - 40))
    game.gameDisplay.blit(text_highest, (game.game_width*0.5, game.game_height - 40))
    game.gameDisplay.blit(game_counter_text, (0, game.game_height - 80))
    game.gameDisplay.blit(reward_text, (game.game_width*0.5, game.game_height - 80))
    pygame.draw.rect(game.gameDisplay, params['black'], [0, 0, game.game_width, game.block_size])
    pygame.draw.rect(game.gameDisplay, params['black'], [0, 0, game.block_size, game.game_width])
    pygame.draw.rect(game.gameDisplay, params['black'], [game.game_width - game.block_size, 0, game.block_size,  game.game_width])
    pygame.draw.rect(game.gameDisplay, params['black'], [0, game.game_width - game.block_size, game.game_width, game.block_size])

def initialize_game(player, game, food, agent, batch_size, counter_games):
    params = define_parameters()
    state_init1 = agent.get_state(game, player, food, params)
    action = [1,0,0]
    player.do_move(action, player.x, player.y, game, food, agent)
    state_init2 = agent.get_state(game,player,food,params)
    reward1 = agent.set_reward(player, game.crash, food, counter_games, action)
    agent.remember(state_init1, action, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory, batch_size)

def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()
    
def arg_parser(params):
    parser = argparse.ArgumentParser()
    parser.add_argument("--display", nargs='?', type=bool, default=True)
    parser.add_argument("--speed", nargs='?', type=int, default=30)
    parser.add_argument("--block_size", nargs='?', type=int, default=20, help="Block size of snake and food, should be a divisor of game_width")
    parser.add_argument("-train", default=True,  action='store_false')
    parser.add_argument("-load_weights", default=True, action='store_false')
    parser.add_argument("--weights_path", nargs='?', type=str, default='Weights/weights.hdf5')
    parser.add_argument("--batch_size", nargs='?', type=int, default=500)
    parser.add_argument("--memory_size", nargs='?', type=int, default=2500)
    parser.add_argument("--episodes", nargs='?', type=int, default=150)
    parser.add_argument("--lr", nargs='?', type=float, default=0.0005, help="Learning Rate")
    parser.add_argument("--edl", nargs='?', type=float, default=1/35, help="epsilon decay linear")
    parser.add_argument("--game_width", nargs='?', type=int, default=600, help="Width of game screen, should be a multiple of block size")
    parser.add_argument("--cf", nargs='?', type=int, default=1, help="Checkpoint creating frequency")
    parser.add_argument("--cp", nargs='?', type=str, default="Snake",help="Checkpoint name prefix")
    args = parser.parse_args()
    params['display'] = args.display
    params['FPS'] = args.speed
    params['block_size'] = args.block_size
    params['train'] = args.train
    params['load_weights'] = args.load_weights
    params['weights_path'] = args.weights_path
    params['batch_size'] = args.batch_size
    params['memory_size'] = args.memory_size
    params['episodes'] = args.episodes
    params['learning_rate'] = args.lr
    params['epsilon_decay_linear'] = args.edl
    params['game_width'] = args.game_width
    params['game_height'] = args.game_width + 100
    params['cf'] = args.cf
    params['cp'] = args.cp
    return params
    
def print_info(params):
    print("Running with width of game: {}".format(params['game_width']))
    print("Running with height of game: {}".format(params['game_height']))
    print("Running with {} episodes".format(params['episodes']))
    print("Running with {} memory_size".format(params['memory_size']))
    print("Running with {} batch_size".format(params['batch_size']))
    print("Running with {} frames per second".format(params['FPS']))
    print("Running with {} block_size".format(params['block_size']))
    print("Running with {} learning rate".format(params['learning_rate']))
    print("Running with display: ",format(params['display']))
    print("Running with training: ",format(params['train']))
    print("Running with Checkpoint frequency: ",format(params['cf']))
    print("Running with Checkpoint prefix: ",format(params['cp']))

def run(params):
    pygame.init()
    agent = DQNAgent(params)
    print_info(params)
    weights_filepath = params['weights_path']
    if params['load_weights']:
        agent.model.load_weights(weights_filepath)
        print("Weights Loaded")
        
    else:
        print("Training From Scratch...")
    counter_games = 0
    score_plot = []
    counter_plot = []
    record = 0
    while counter_games < params['episodes']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Class Objects
        game = Game(params)
        player1 = game.player
        food1 = game.food
        
        total_reward = -150
        total_reward2 = 0 
        # First Move
        initialize_game(player1, game, food1, agent, params['batch_size'], counter_games)
        if params['display']:
            display(player1,food1,game,record, counter_games, total_reward, params)
        while not game.crash:
            if not params['train']:
                agent.epsilon = 0

            else:
                # agent.epsilon is set to give randomness to actions
                agent.epsilon = 1 - ((counter_games) * params['epsilon_decay_linear'])

            # old State
            state_old = agent.get_state(game, player1, food1,params)

            # Random Actions or Choose
            if randint(0,1) < agent.epsilon and not params['load_weights']:
                final_move = to_categorical(randint(0, 2), num_classes=3)

            # Prediction
            else:
                prediction = agent.model.predict(state_old.reshape((1, 20)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)

            player1.do_move(final_move, player1.x, player1.y, game, food1, agent)
            state_new = agent.get_state(game, player1, food1,params)
            reward = agent.set_reward(player1, game.crash, food1, counter_games, final_move)
            total_reward += reward
            total_reward2 += reward
            total_reward = round(total_reward, 2)
            total_reward2 = round(total_reward2, 2)

            if params['train']:
                # train short memory base on the new action and state
                agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
                # store the new data into a long term memory
                agent.remember(state_old, final_move, reward, state_new, game.crash)

            record = get_record(game.score, record)
            if params['display']:
                display(player1, food1, game, record, counter_games, total_reward, params)

        if params['train']:
            agent.replay_new(agent.memory, params['batch_size'])
        counter_games += 1
        print(f'Game {counter_games}      Score: {game.score}    Reward: {total_reward2}')
        score_plot.append(game.score)
        counter_plot.append(counter_games)
        if counter_games%params['cf'] == 0:
            n = int(counter_games/params['cf'])
            agent.model.save_weights(params['cp']+str(n) + ".hdf5")
            print("Checkpoint Saved...")
        
    plot_seaborn(counter_plot, score_plot)
    pygame.quit()
    quit()

if __name__ == '__main__':
    pygame.font.init()
    params = define_parameters()
    params = arg_parser(params)
    run(params)
