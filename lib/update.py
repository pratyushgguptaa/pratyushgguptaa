from os import environ
import secrets
from cryptography.fernet import Fernet


def update_word():
    words = []
    with open('./data/words.txt', 'r') as f:
        for line in f:
            words.append(line.strip())
    print(len(words))
    next = words[secrets.randbelow(len(words))]
    next += words[secrets.randbelow(len(words))]
    next += words[secrets.randbelow(len(words))]
    key = ''
    if 'KEY' in environ:
        key = environ['KEY']
    else:
        with open('./data/key.txt', 'r') as f:
            key = f.read()
    f = Fernet(key)

    word = f.encrypt(next.encode())

    with open('./data/word.txt', 'wb') as f:
        f.write(word)
