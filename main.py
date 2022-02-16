import os
import sys
import lib.retrieve as retrieve_word
import lib.update as update_word
import pickle
import wordle

if __name__ == '__main__':
    actual_word = retrieve_word.retrieve_word()
    game = wordle.Wordle()

    game.guess_word(actual_word, 'SPORT')
    game.guess_word(actual_word, 'ADIEU')
    game.guess_word(actual_word, 'CROOL')
    game.save_game()

    print('calling main.py')
