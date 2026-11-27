commands = {}


def command():
    def decorator(func):
        commands[func.__name__] = func
        return func

    return decorator


@command()
def ask():
    print("Question")


print("Function name:", ask.__name__)
print("Registered commands:", list(commands.keys()))

ask()
commands["ask"]()