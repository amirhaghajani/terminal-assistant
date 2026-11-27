def register(func):
    print("Registering:", func.__name__)

    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper


def ask():
    print("Question")


print("Before decoration:", ask.__name__)

ask = register(ask)

print("After decoration:", ask.__name__)

print('\n-----------------')
ask()