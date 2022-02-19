from markdown import *
from wordle import Wordle
from lib.retrieve import retrieve_word

game = Wordle()
users = {}
game = game.load_game()
# print all values of game object
print(game.__dict__)
