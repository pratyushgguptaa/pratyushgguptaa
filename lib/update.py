import secrets
from cryptography.fernet import Fernet
from lib.getEnv import getEnv


def update_word():
    words = []
    with open('./data/words.txt', 'r') as f:
        for line in f:
            words.append(line.strip())
    print(len(words))
    next = words[secrets.randbelow(len(words))]
    next += words[secrets.randbelow(len(words))]
    next += words[secrets.randbelow(len(words))]
    key = getEnv('KEY')
    f = Fernet(key)

    word = f.encrypt(next.encode())

    with open('./data/word.txt', 'wb') as f:
        f.write(word)
