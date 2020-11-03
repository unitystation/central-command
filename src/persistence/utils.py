import time


def generate_isb():
    return str(time.time()).replace('.', '')[:13]
