import wordle
from string import Template


def boardToMarkdown(board):
    """
    Convert a board to markdown.
    """
    template = Template(
        '![$text](https://via.placeholder.com/125/$color/f?text=$text)')
    template = Template(
        '<img src="https://via.placeholder.com/125/$color/f?text=$text">')
    board_md = '<div align="center">'
    for i, row in enumerate(board):
        row_md = ''
        for cell in row:
            row_md += '&nbsp;' + \
                template.substitute(color=cell['color'], text=cell['letter'])
        row_md += '<br>'
        board_md += row_md
    return board_md+'</div>'
    # board_md = '| W | O | R | D | L | E |\n|---|:-:|:-:|:-:|:-:|:-:|\n'
    # for i, row in enumerate(board):
    #     row_md = '| **'+str(i+1)+'** '
    #     for cell in row:
    #         row_md += '|' + \
    #             template.substitute(color=cell['color'], text=cell['letter'])
    #     row_md += '|\n'
    #     board_md += row_md
    # return board_md


game = wordle.Wordle().load_game()

md = boardToMarkdown(game.get_board())
with open('check.md', 'w') as f:
    f.write(md)
