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


def replaceText(readme, item, replace):
    start = '<!-- {} START -->'.format(item)
    end = '<!-- {} END -->'.format(item)
    before = readme.split(start)[0]
    after = readme.split(end)[1]

    readme = before + start + replace + end + after
    return readme


def updateReadme(issue, game, actual_word):
    with open('README.md', 'r') as file:
        readme = file.read()

    # update details about the game
    readme = replaceText(
        readme, 'DETAILS', markdown.howToMarkdown(game.is_over(actual_word)))

    # update the board
    readme = replaceText(
        readme, 'BOARD', markdown.boardToMarkdown(game.get_board()))

    # update the stats
    readme = replaceText(
        readme, 'STATS', markdown.statsToMarkdown(game.get_stats()))

    # update the guesses
    readme = replaceText(
        readme, 'GUESSES', markdown.guessesToMarkdown(game.get_stats()))

    # update the top 10 players section
    readme = replaceText(
        readme, 'TOP', markdown.usersToMarkdown(game.users()))

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
        update_word()
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
        result = game.guess_word(
            actual_word, guessed_word, '@'+issue.user.login)
        if result == 'Not in dictionary':
            commentAndClose(issue, 'please enter a valid english word.')
            return
        elif result == 'Already guessed':
            commentAndClose(
                issue, 'the word is already guessed in the current game.')
            return
        commentAndClose(
            issue, 'nice guess! Your guess has been added to the board.\nIt will be reflected on the page shortly 🙌')
    else:
        commentAndClose(
            issue, 'please use a valid command and do not modify any other thing in the issue title.')
        issue.edit(labels=['Invalid'])
        return

    game.save_game()

    if game.is_over(actual_word) == True:
        comment = 'The game is over. The word was: '+actual_word+'.\n'
        if game.result(actual_word) == 'WIN':
            issue.add_to_labels('🏆 WINNING GUESS!!')
            comment += 'Congratulations! You all won the game 🥳.\nThanks for playing everyone. We gotta maintain the streak right?\n'
        else:
            issue.add_to_labels('💩 LOSING GUESS!!')
            comment += 'Awww man, we lost the game 🤕.\nThanks for playing everyone. We will get it right next time.\n'
        game.update_stats(actual_word)
        # showing all the users in the currect game
        comment += 'Players this game: '
        comment += ", ".join(set(game.get_guessers()))
        comment += '\n'
        issue.create_comment(comment)

    updateReadme(issue, game, actual_word)


if __name__ == '__main__':

    repo = Github(os.environ['GITHUB_TOKEN']).get_repo(
        os.environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(os.environ['ISSUE_NUMBER']))

    x = main(issue)
