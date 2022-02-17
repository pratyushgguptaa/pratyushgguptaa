from lib.retrieve import retrieve_word
from lib.update import update_word
from lib.getEnv import getEnv
import markdown
from wordle import Wordle
from github import Github

guess_word = "CROOL"


def main(game, actual_word):
    game.guess_word(actual_word, guess_word)
    game.save_game()

    with open('README.md', 'r') as file:
        readme = file.read()
    boardStart = '<!-- BOARD START -->'
    boardEnd = '<!-- BOARD END -->'
    before = readme.split(boardStart)[0]
    after = readme.split(boardEnd)[1]

    readme = before + boardStart + \
        markdown.boardToMarkdown(game.get_board()) + boardEnd + after

    with open('README.md', 'w') as file:
        file.write(readme)

    game.save_game()


if __name__ == '__main__':

    g = Github(getEnv('GITHUB_TOKEN'))
    for repo in g.get_user().get_repos():
        print(repo.name)
        # to see all the available attributes and methods
        # print(dir(repo))

    print('calling main.py')
