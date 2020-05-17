# Reinforcement-Learning-with-Pygame
Train an AI bot to play snake game

## Introduction
The goal of this project is to develop an AI based bot which can learn how to play a popular game SNAKE from scratch using deep reinforcement learning algorithm. The game is developed using pygame library and is trained using keras and tensorflow libraries. The approach is simple. Some state parameters are defined and based on state and actions corresponding positive or negative reward is given to the bot. Initially the bot has no information about the game and it developes a strategy to figure out how to play and how to maximize the score or reward.

## Requirements
This project requires python 3.7 with pygame, keras, tensorflow libraries installed

## Run
To run this game, execute the following command
```
python main.py
```
This will run and show the agent. The default configuration loads the file Weights/weights.hdf5 and runs a test. The Deep neural network can be customized in the file main.py modifying the dictionary params in the function define_parameters() or by adding corresponding arguments in terminal.

