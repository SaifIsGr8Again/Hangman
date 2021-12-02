"""
Module that starts the game.
"""
import sys
sys.path.insert(1, 'classes')
from game import Game

def start():
    """
    Starts the game.
    """
    current_dir = "D:\\Personal\\Code\\all games\\Python\\hangman_pg\\"
    Game(current_dir, "hangman", 1000, (0, 0))

start()
