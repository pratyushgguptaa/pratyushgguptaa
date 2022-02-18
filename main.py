from lib.retrieve import retrieve_word
from lib.update import update_word
import markdown
from wordle import Wordle
from github import Github
import os
import re

guess_word = "CROOL"


def commentAndClose(issue, comment):
    issue.create_comment('@'+issue.user.login+', '+comment)
    issue.edit(state='closed')


def updateReadme(issue, game, actual_word):
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


def main(issue):
    actual_word = retrieve_word()
    game = Wordle().load_game()
    if issue.title.upper() == "WORDLE: START NEW GAME":
        # check if the previous game is over
        if game.is_over(actual_word) == False:
            commentAndClose(
                issue, 'there is a game in progress. Please make more guesses and finish it first.')
            return
        game.start_new()
        commentAndClose(
            issue, 'the new game has started. Start making your guesses!!')

    elif issue.title.upper().startswith('WORDLE: '):
        if game.is_over(actual_word) == True:
            commentAndClose(
                issue, 'the game is over. Start a new game to continue.')
            return
        pattern = 'WORDLE: ([A-Z]{'+str(game.letters)+'})'
        match = re.match(pattern, issue.title.upper())
        if match is None:
            commentAndClose(issue, 'please enter a valid guess word.')
            return
        guessed_word = match.group(1)
        print('New word guessed_word is: '+guessed_word)
        result = game.guess_word(actual_word, guessed_word)
        if result == 'Not in dictionary':
            commentAndClose(issue, 'please enter a valid english word.')
            return
        elif result == 'Already guessed':
            commentAndClose(
                issue, 'the word is already guessed in the current game.')
            return
    else:
        commentAndClose(
            issue, 'please use a valid command and do not modify any other thing in the issue title.')
        issue.edit(labels=['Invalid'])
        return

    commentAndClose(
        issue, 'nice guess! Your guess has been added to the board.\nIt will be reflected on the page shortly 🙌')
    game.save_game()

    if game.is_over(actual_word) == True:
        if game.result(actual_word) == 'WIN':
            issue.add_to_labels('🏆 WINNING GUESS!!')
        else:
            issue.add_to_labels('💩 LOSING GUESS!!')
        update_word()
        issue.create_comment('The word was '+actual_word +
                             '.\nThanks everyone for finishing the WORDLE 🥳')

    updateReadme(issue, game, actual_word)


if __name__ == '__main__':

    # game = Wordle().load_game()

    # print(game.guess_word(retrieve_word(), guess_word))
    # print(game.get_board())
    # print(retrieve_word())
    # game.save_game()

    repo = Github(os.environ['GITHUB_TOKEN']).get_repo(
        os.environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(os.environ['ISSUE_NUMBER']))

    x = main(issue)
