def register(func):
    print("Registering:", func.__name__)
    return func


def ask():
    print("Question")


ask = register(ask)

ask()