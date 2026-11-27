# Terminal Assistant

A small Python project that gradually evolves into an installable command-line application.

This is **Stage 6: Understanding Python Functions and Decorators**.

Before introducing Typer, we'll explore the Python concepts that make decorator-based frameworks possible.

This stage is written for learners who may have experience in other programming languages but aren't yet familiar with Python's function objects, decorators, and function registration.

## What's new?

In this stage, we explore:

- Functions as objects.
- Assigning functions to variables.
- Passing functions as arguments.
- Returning functions from other functions.
- Registering functions in a dictionary.
- Wrapper functions and closures.
- Decorator syntax (`@`).
- Decorator factories (`@command()`).
- The difference between returning the original function and returning a wrapper.

## Project structure

```text
terminal-assistant/
├── examples/
│   ├── decorators.py
│   ├── decorator_wrapper.py
│   ├── decorator_syntax.py
│   ├── decorator_factory.py
│   └── decorator_registration.py
├── pyproject.toml
├── README.md
└── src/
    └── terminal_assistant/
        ├── __init__.py
        └── cli.py
```

Each file in `examples/` demonstrates a separate concept. Run them independently and experiment with the code.

## 1. Functions are objects

In Python, functions are objects. This means we can assign a function to another variable and call it through that variable.

```python
def say_hello():
    print("Hello!")

x = say_hello
x()
```

Output:

```text
Hello!
```

Notice the difference:

- `say_hello` refers to the function itself.
- `say_hello()` executes the function.

When we write `x = say_hello`, we don't execute the function. We assign a reference to the same function object.

Example: `examples/decorators.py`

## 2. Passing functions as arguments

A function can receive another function as an argument.

```python
def register(func):
    print("Registering:", func.__name__)

def ask():
    print("Question")

register(ask)
```

Output:

```text
Registering: ask
```

Here, `func` refers to the original `ask` function.

The `__name__` attribute allows us to inspect the function's name.

Example: `examples/decorators.py`

## 3. Returning functions

A function can return another function or return the original function it received.

For example:

```python
def register(func):
    print("Registering:", func.__name__)
    return func

def ask():
    print("Question")

ask = register(ask)
ask()
```

Output:

```text
Registering: ask
Question
```

Let's understand this assignment:

```python
ask = register(ask)
```

1. The original `ask` function is passed to `register`.
2. `register` receives it through `func`.
3. `return func` returns the original function.
4. The returned function is assigned back to `ask`.

The name `ask` still refers to the original function.

Example: `examples/decorators.py`

## 4. Wrapper functions

A wrapper is a function that calls another function and adds behavior before or after that call.

```python
def register(func):
    print("Registering:", func.__name__)

    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper


def ask():
    print("Question")


ask = register(ask)

ask()
```

Output:

```text
Registering: ask
Before
Question
After
```

The important difference is:

```python
return wrapper
```

Instead of returning the original function, we return a new function.

Therefore:

```python
ask = register(ask)
```

makes the name `ask` refer to `wrapper`.

Inside `wrapper`, `func()` still calls the original function.

### What is a closure?

The inner function `wrapper` uses the variable `func` from the surrounding function `register`.

Even after `register` finishes executing, `wrapper` can still access `func`.

This behavior is called a **closure