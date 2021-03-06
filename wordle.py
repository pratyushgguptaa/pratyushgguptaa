import pickle


class Wordle:
    '''
    Colors

    '''
    green = '538d4e'
    yellow = 'b59f3b'
    grey = '3a3a3c'
    blank = '121213'

    def __init__(self, rows=6, letters=5):
        '''
        Initialize a new wordle game. Rows define the number of guesses and letters the word has.
        '''
        self.guess_count = 0
        self.board = [[{'color': self.blank, 'letter': '+'}
                       for _ in range(letters)] for _ in range(rows)]
        self.rows = rows
        self.letters = letters
        self.guessed_words = []
        self.guessers = []

    def start_new(self):
        '''
        Start a new game. Reset everything to the initial state
        '''
        self.guess_count = 0
        self.guessed_words = []
        self.guessers = []
        self.board = [[{'color': self.blank, 'letter': '+'}
                       for _ in range(self.letters)] for _ in range(self.rows)]

    def guess_word(self, actual_word, guessed_word, user):
        '''
        Add a new guessed word to the board.
        '''
        if guessed_word in self.guessed_words:
            return 'Already guessed'
        words = []
        with open('data/words.txt', 'r') as f:
            for line in f:
                words.append(line.strip())
        if guessed_word.lower() not in words:
            return 'Not in dictionary'
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
        self.guessers.append(user)
        users = self.get_users()
        if user not in users:
            users[user] = 1
        else:
            users[user] += 1
        self.save_users(users)
        return 'OK'

    def is_over(self, actual_word):
        '''
        Check if the game is over.
        '''
        if self.guess_count == 0:
            return False
        if self.guessed_words[-1] == actual_word:
            return True
        elif self.guess_count == self.rows:
            return True
        return False

    def result(self, actual_word):
        '''
        Check the result of the game.
        TODO: It can break if result is called before the game is over. FIX IT
        '''
        if self.guessed_words[-1] == actual_word:
            return 'WIN'
        elif self.guess_count == self.rows:
            return 'LOSE'
        return ''

    def get_guessed_words(self):
        return self.guessed_words

    def get_guess_count(self):
        return self.guess_count

    def get_guessers(self):
        return self.guessers

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

    def get_stats(self, path='data/stats.txt'):
        with open(path, 'rb') as f:
            stats = pickle.load(f)
        return stats

    def update_stats(self, actual_word):
        '''
        Update the stats file.
        '''
        stats = self.get_stats()
        stats['Played'] += 1
        win = self.result(actual_word) == 'WIN'
        if win:
            stats['Total Win'] += 1
            stats['Current Streak'] += 1
            stats['Last'] = self.guess_count
            stats[str(stats['Last'])] += 1
            if stats['Current Streak'] > stats['Max Streak']:
                stats['Max Streak'] = stats['Current Streak']
        else:
            stats['Current Streak'] = 0
            stats['Last'] = -1
        stats['Win %'] = int(stats['Total Win'] / stats['Played'] * 100)
        self.save_stats(stats)

    def save_stats(self, stats, path='data/stats.txt'):
        with open(path, 'wb') as f:
            pickle.dump(stats, f)

    def get_users(self, path='data/users.txt'):
        with open(path, 'rb') as f:
            users = pickle.load(f)
        return users

    def save_users(self, users, path='data/users.txt'):
        with open(path, 'wb') as f:
            pickle.dump(users, f)
