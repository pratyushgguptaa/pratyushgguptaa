from cryptography.fernet import Fernet
from lib.getEnv import getEnv


def retrieve_word():
    key = getEnv('KEY')

    f = Fernet(key)

    with open('./data/word.txt', 'rb') as fileRead:
        word = fileRead.read()

    return f.decrypt(word).decode()[:5].upper()
