from lib.retrieve import retrieve_word
from lib.update import update_word
import markdown
from wordle import Wordle
from github import Github
import os
import re

guess_word = "CROOL"


def main(game, issue):
    actual_word = retrieve_word()
    game = Wordle().load_game()
    if issue.title.upper() == "WORDLE: START NEW GAME":
        # check if the previous game is over
        if game.is_over(actual_word) == False:
            s = '@'+issue.user.login + \
                ', there is a game in progress. Please make more guesses and finish it first.'
            issue.create_comment(s)
            issue.edit(state='closed')
            return
        game.start_new()
        s = '@'+issue.user.login+', the new game has started. Start making your guesses!!'
        issue.create_comment(s)
        issue.edit(state='closed')

    elif issue.title.upper().startsWith('WORDLE: GUESS '):
        pattern = 'WORDLE: GUESS ([A-Z]{'+str(game.letters)+'})'
        match = re.match(pattern, issue.title.upper())
        if match is None:
            s = '@'+issue.user.login+', please enter a valid guess word.'
            issue.create_comment(s)
            issue.edit(state='closed')
            return
        guessed_word = match.group(1)
        if game.guess_word(actual_word, guessed_word) != 'OK':
            s = '@'+issue.user.login+', please enter a valid guess word.'
            issue.create_comment(s)
            issue.edit(state='closed')
            return

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

    repo = Github(os.environ['GITHUB_TOKEN']).get_repo(
        os.environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(os.environ['ISSUE_NUMBER']))

    game = Wordle().load_game()

    x = main(game, issue)

    print(x)
