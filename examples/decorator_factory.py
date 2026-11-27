def command():
    print("Creating a decorator")

    def decorator(func):
        print("Registering:", func.__name__)
        return func  # returning original function

    return decorator


@command()
def ask():
    print("Question")


print("After decoration:", ask.__name__)

print('\n-----------------')
ask()