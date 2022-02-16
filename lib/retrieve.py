from os import environ
from cryptography.fernet import Fernet


def retrieve_word():
    key = ''

    if 'KEY' in environ:
        key = environ['KEY']
    else:
        readSecret = open('secret.txt', 'rb')
        key = readSecret.read()
        readSecret.close()

    f = Fernet(key)

    fileRead = open('./data/word.txt', 'rb')
    word = fileRead.read()
    fileRead.close()

    return f.decrypt(word).decode()
