from os import environ


def getEnv(VAR):
    if VAR in environ:
        return environ['KEY']
    else:
        path = './secrets/'+VAR
        with open(path, 'r') as keyRead:
            return keyRead.read()
