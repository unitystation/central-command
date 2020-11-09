import time


def generate_isbn():
    return str(time.time()).replace(".", "")[:13]
