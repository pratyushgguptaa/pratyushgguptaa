import os
import sys
import lib.retrieve as retrieve_word
import lib.update as update_word
import pickle
import wordle

if __name__ == '__main__':
    # update_word.update_word()
    actual_word = retrieve_word.retrieve_word()
    # with open('data/game.wordle', 'rb') as f:
    #     wordle = pickle.load(f)
    # print(wordle.is_over(actual_word))
    # print(wordle.get_board())
    # guessed_word = input('Guess word: ')
    game = wordle.Wordle()
    print(actual_word)
    game.guess_word(actual_word, 'ABCDE')
    game.guess_word(actual_word, 'FGHIJ')
    game.guess_word(actual_word, 'KLMNO')
    game.guess_word(actual_word, 'PQRST')
    game.guess_word(actual_word, 'CROOL')

    print(game.is_over(actual_word))
    print(game.guess_count)
    print(game.get_board())

    with open('data/game.wordle', 'wb') as f:
        pickle.dump(game, f)

    print('calling main.py')
