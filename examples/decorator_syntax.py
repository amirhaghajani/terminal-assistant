def register(func):
    print("Registering:", func.__name__)

    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper


@register
def ask():
    print("Question")


print("After decoration:", ask.__name__)

print('\n-----------------')
ask()