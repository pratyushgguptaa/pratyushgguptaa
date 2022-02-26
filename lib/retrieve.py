from cryptography.fernet import Fernet
from lib.getEnv import getEnv


def retrieve_word():
    '''
    Retrieve hidden word by decrypting using the KEY env variable
    '''
    key = getEnv('KEY')

    f = Fernet(key)

    with open('./data/word.txt', 'rb') as fileRead:
        word = fileRead.read()

    return f.decrypt(word).decode()[:5].upper()
