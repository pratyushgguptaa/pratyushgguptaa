from markdown import *
from wordle import Wordle
from lib.retrieve import retrieve_word

game = Wordle()

stats = game.get_stats()
print(stats)
# print(guessesToMarkdown(stats))
print(retrieve_word())