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

    print(retrieve_word())

    repo = Github(getEnv('GITHUB_TOKEN')).get_repo(
        getEnv('GITHUB_REPOSITORY'))
    issue = repo.get_issue(number=int(getEnv('ISSUE_NUMBER')))
    issue_author = '@' + issue.user.login
    repo_owner = '@' + getEnv('REPOSITORY_OWNER')

    print('calling main.py')
