# import wordle
from string import Template


def boardToMarkdown(board):
    template = Template(
        '<img src="https://via.placeholder.com/75/$color/f?text=$text">')
    board_md = '<div align="center">'
    for i, row in enumerate(board):
        row_md = ''
        for cell in row:
            row_md += '&nbsp;' + \
                template.substitute(color=cell['color'], text=cell['letter'])
        row_md += '<br>'
        board_md += row_md
    return board_md+'</div>\n'
