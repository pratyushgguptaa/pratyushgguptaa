from os import environ
from cryptography.fernet import Fernet


def retrieve_word():
    key = ''

    if 'KEY' in environ:
        key = environ['KEY']
    else:
        with open('./data/key.txt', 'r') as keyRead:
            key = keyRead.read()

    f = Fernet(key)

    with open('./data/word.txt', 'rb') as fileRead:
        word = fileRead.read()

    return f.decrypt(word).decode()[:5].upper()
