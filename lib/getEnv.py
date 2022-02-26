from os import environ


def getEnv(VAR):
    """
    Get the value of an environment variable.
    :param VAR: The name of the environment variable.
    :return: The value of the environment variable.
    """
    if VAR in environ:
        return environ['KEY']
    else:
        path = './secrets/'+VAR
        with open(path, 'r') as keyRead:
            return keyRead.read()
