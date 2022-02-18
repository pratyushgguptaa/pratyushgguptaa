from markdown import statsToMarkdown
from wordle import Wordle

stats = {"Played": 1, "Total Win": 1, "Win %": 100,
         "Current Streak": 1, "Max Streak": 1, "1": 0, "2": 0, "3": 1, "4": 0, "5": 0, "6": 0, "last": 3}

game = Wordle()

# game.save_stats(stats)

print(statsToMarkdown(stats))
