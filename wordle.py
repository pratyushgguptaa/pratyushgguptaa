import pickle
import inspect


class Wordle:
    green = '538d4e'
    yellow = 'b59f3b'
    grey = '3a3a3c'
    blank = '121213'

    def __init__(self, rows=6, letters=5):
        self.guess_count = 0
        self.board = [[{'color': self.blank, 'letter': '+'}
                       for _ in range(letters)] for _ in range(rows)]
        self.rows = rows
        self.letters = letters
        self.guessed_words = []

    def start_new(self):
        self.guess_count = 0
        self.guessed_words = []
        self.board = [[{'color': self.blank, 'letter': '+'}
                       for _ in range(self.letters)] for _ in range(self.rows)]

    def guess_word(self, actual_word, guessed_word):
        if guessed_word in self.guessed_words:
            return 'Already guessed'
        for i in range(self.letters):
            if guessed_word[i] == actual_word[i]:
                self.board[self.guess_count][i]['color'] = self.green
            elif guessed_word[i] in actual_word:
                self.board[self.guess_count][i]['color'] = self.yellow
            else:
                self.board[self.guess_count][i]['color'] = self.grey
            self.board[self.guess_count][i]['letter'] = guessed_word[i]
        self.guess_count += 1
        self.guessed_words.append(guessed_word)
        return 'OK'

    def is_over(self, actual_word):
        if self.guess_count == 0:
            return False
        if self.guessed_words[-1] == actual_word:
            return True
        elif self.guess_count == self.rows:
            return True
        return False

    def get_guessed_words(self):
        return self.guessed_words

    def get_guess_count(self):
        return self.guess_count

    def get_board(self):
        return self.board

    def save_game(self, path='data/current.wordle'):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load_game(self, path='data/current.wordle'):
        with open(path, 'rb') as f:
            loaded = pickle.load(f)
        if isinstance(loaded, Wordle):
            return loaded
        return Wordle()
