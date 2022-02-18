from markdown import *
from wordle import Wordle
from lib.retrieve import retrieve_word

stats = {"Played": 1, "Total Win": 1, "Win %": 100,
         "Current Streak": 1, "Max Streak": 1, "1": 2, "2": 0, "3": 3, "4": 3, "5": 1, "6": 0, "Last": 4}

game = Wordle()

# game.save_stats(stats)

print(guessesToMarkdown(stats))
print(retrieve_word())