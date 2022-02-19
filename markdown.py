from string import Template


def howToMarkdown(is_over):
    if is_over == False:
        return """
To make your next guess, [Click here](https://github.com/pratyushgguptaa/pratyushgguptaa/issues/new?body=Just+enter+a+5+letter+word+in+the+title+after+%22WORDLE%3A+%22+and+click+%22Submit+new+issue%22.+You+don%27t+need+to+do+anything+else+%3AD&title=WORDLE%3A+). You will be directed to the **Creat New Issue** page with a default title ready for you: `WORDLE: `. Just enter the 5 letter word after this. For example, you can guess: `WORDLE: HELLO`. Come back here and refresh after about a minute or two your guess will be added.

<details><summary>Your guess does not show up?</summary> Probably someone else guessed a word just before you. Analyze their results and guess a new word!!</details>
"""
    else:
        return """
Looks like its game over. [Click Here](https://github.com/pratyushgguptaa/pratyushgguptaa/issues/new?title=WORDLE%3A+START+NEW+GAME&body=Dont+change+the+title.+If+the+game+is+over+new+game+will+be+loaded) to reset the board and start a new game. You will be directed to the **Create New Issue** page with a default title ready for you: `WORDLE: START NEW GAME`. You do not need to change anything just create a new issue. Come back here and refresh after a minute or two a new game will be loaded, with a brand new hidden word 👀.
"""


def boardToMarkdown(board):
    template = Template(
        '<img src="https://via.placeholder.com/70/$color/f?text=$text">')
    board_md = '\n<div align="center">'
    for i, row in enumerate(board):
        row_md = ''
        for cell in row:
            row_md += '&nbsp;' + \
                template.substitute(color=cell['color'], text=cell['letter'])
        row_md += '<br>'
        board_md += row_md
    return board_md+'</div>\n'


def statsToMarkdown(stats):
    stats_md = "\n| "
    for stat in ['Played', 'Win %', 'Current Streak', 'Max Streak']:
        stats_md += str(stats[stat]) + " | "
    stats_md += "\n|"
    stats_md += ":---:|"*4
    stats_md += "\n| "
    for stat in ['Played', 'Win %', 'Current Streak', 'Max Streak']:
        stats_md += stat + " | "
    return stats_md+"\n"


def guessesToMarkdown(stats):
    N = 20
    maxx = 0
    for stat in ['1', '2', '3', '4', '5', '6']:
        maxx = max(maxx, stats[stat])
    guesses_md = "\n"
    for i in range(6):
        guesses_md += str(i+1)+". "
        count = stats[str(i+1)]*N//maxx
        if count == 0:
            count = 1
        color = 'green' if stats['Last'] == i+1 else 'grey'
        image = "![](data/"+color+".png)"
        guesses_md += image*count
        guesses_md += " "+str(stats[str(i+1)])
        guesses_md += "\n"
    return guesses_md+"\n"
