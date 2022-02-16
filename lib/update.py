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
    key = ''
    if 'KEY' in environ:
        key = environ['KEY']
    else:
        readSecret = open('secret.txt', 'rb')
        key = readSecret.read()
        readSecret.close()
    f = Fernet(key)

    word = f.encrypt(next.encode())

    fileRead = open('./data/word.txt', 'w')
    fileRead.write(word.decode())
    fileRead.close()

    print('New word loaded. And the word is: hehe Tumhe kyun btaun')
