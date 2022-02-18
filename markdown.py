from string import Template


def boardToMarkdown(board):
    template = Template(
        '<img src="https://via.placeholder.com/70/$color/f?text=$text">')
    board_md = '<div align="center">'
    for i, row in enumerate(board):
        row_md = ''
        for cell in row:
            row_md += '&nbsp;' + \
                template.substitute(color=cell['color'], text=cell['letter'])
        row_md += '<br>'
        board_md += row_md
    return board_md+'</div>\n'


def statsToMarkdown(stats):
    # not using a generic function
    # stats_md = "| "
    # for stat in stats.keys():
    #     stats_md += str(stats[stat]) + " | "
    # stats_md += "\n|"
    # stats_md += ":---:|"*len(stats)
    # stats_md += "\n| "
    # for stat in stats.keys():
    #     stats_md += stat + " | "
    # return stats_md+"\n"

    # only show some needed values
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
    N = 20  # for the maximum row
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
        guesses_md += str(stats[str(i+1)])
        guesses_md += "\n"
    return guesses_md+"\n"
