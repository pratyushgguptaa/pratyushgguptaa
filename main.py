from lib.retrieve import retrieve_word
from lib.update import update_word
from lib.getEnv import getEnv
import markdown
from wordle import Wordle
from github import Github
import os

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

    print(retrieve_word())

    repo = Github(os.environ['GITHUB_TOKEN']).get_repo(
        os.environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(os.environ['ISSUE_NUMBER']))
    issue_author = '@' + issue.user.login
    repo_owner = '@' + os.environ['REPOSITORY_OWNER']

    print(issue_author)
    print(repo_owner)

    print('calling main.py')
