from lib.retrieve import retrieve_word
from lib.update import update_word
from lib.markdown import howToMarkdown, boardToMarkdown, statsToMarkdown, guessesToMarkdown, usersToMarkdown

from wordle import Wordle
from github import Github
import os
import re


def commentAndClose(issue, comment):
    '''
    Comment on the issue (also mentioning the user who created the issue) and close it.
    '''
    issue.create_comment('@'+issue.user.login+', '+comment)
    issue.edit(state='closed')


def replaceText(readme, item, replace):
    '''
    Replace text in a readme file with new data inside the comment tags

    Args:
        readme: string of the readme file
        item: string of the comment tag
        replace: string of the new data

    Returns:
        readme: string of the readme file with new data
    '''
    start = '<!-- {} START -->'.format(item)
    end = '<!-- {} END -->'.format(item)
    before = readme.split(start)[0]
    after = readme.split(end)[1]

    readme = before + start + replace + end + after
    return readme


def updateReadme(issue, game, actual_word):
    '''
    To read, update and save the readme file

    This method reads the current readme file, replaces text from specified comment tags with new game data.
    It then saves the new readme file.

    Args:
        issue: GitHub issue object
        game: wordle game object
        actual_word: string of the actual word 

    Returns:
        None
    '''
    with open('README.md', 'r') as file:
        readme = file.read()

    readme = replaceText(
        readme, 'DETAILS', howToMarkdown(game.is_over(actual_word)))
    readme = replaceText(
        readme, 'BOARD', boardToMarkdown(game.get_board()))
    readme = replaceText(
        readme, 'STATS', statsToMarkdown(game.get_stats()))
    readme = replaceText(
        readme, 'GUESSES', guessesToMarkdown(game.get_stats()))
    readme = replaceText(
        readme, 'TOP', usersToMarkdown(game.get_users()))

    with open('README.md', 'w') as file:
        file.write(readme)


def main(issue):
    '''
    Parse the issue title and updates the current game.



    Args:
        issue: GitHub issue object

    Returns:
        None
    '''
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
        comment = 'The game is over. The word was: `'+actual_word+'`.\n'
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
