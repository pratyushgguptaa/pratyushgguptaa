from markdown import statsToMarkdown
from wordle import Wordle

stats = {"Played": 0, "Total Win": 0, "Win %": 0,
         "Current Streak": 0, "Max Streak": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}

game = Wordle()

game.save_stats(stats)

print(statsToMarkdown(stats))
