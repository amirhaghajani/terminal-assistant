# How I Built My Own Python CLI to Understand How Command-Line Tools Work

I have always used command-line tools, but I never really understood how they were created.

As a Python developer, I often use commands like:

```bash
pytest tests/
pytest -v
pytest --help
```

I know that `pytest` is a Python testing tool, but I started wondering:

- How does the word `pytest` become an executable command in my terminal?
- How does it understand commands, arguments, and options?
- How does it know what to do when I type `-v`?
- How does `--help` know which options and commands to display?
- Is it just a Python function somewhere? How does that function get connected to the terminal?

I had used many CLI tools, but I had never built one from scratch.

So I decided to create my own command-line application in Python. Not just to make something that works, but to understand how it works, step by step.

I didn't want to start with a framework and copy code from a tutorial. I wanted to understand what happens underneath.

I started with a simple Python function and gradually turned it into a CLI application. Eventually, I connected it to Ollama so it could communicate with a local language model.

Here is my journey.

You can find the complete project on [GitHub](https://github.com/amirhaghajani/terminal-assistant). Each stage has its own branch, so you can follow the development step by step.

## What Are We Going to Build?

We're going to build a small command-line assistant called `assistant`.

The final application will support two commands:

**1. Ask a question**

```bash
assistant ask "What is dependency injection in Python?"
```

The application sends the question to a local language model running through Ollama and prints its response.

**2. Create a file**

```bash
assistant create-file notes.txt "My first CLI application"
```

This command creates `notes.txt` and writes the supplied content into it.

We can also ask the application for help:

```bash
assistant --help
```

The interesting thing is that we'll build this application gradually.

At the beginning, we won't have commands like `assistant ask`. We'll start with an ordinary Python function and work our way toward this final interface.

By the end, we'll understand how Python code becomes an executable terminal command.

## The Journey: From a Python Script to a CLI Application

I didn't build the final application in one step. I divided the project into smaller stages, and each stage introduced a new concept.

I also created a separate Git branch for each stage. This way, you can explore the code at every point and see exactly how the application evolved.

Here is the roadmap:

1. [Plain Python](https://github.com/amirhaghajani/terminal-assistant/tree/01-plain-python) — Start with a simple Python function.
2. [Manual CLI with `sys.argv`](https://github.com/amirhaghajani/terminal-assistant/tree/02-manual-cli) — Learn how Python receives arguments from the terminal.
3. [CLI with `argparse`](https://github.com/amirhaghajani/terminal-assistant/tree/03-argparse-cli) — Use Python's built-in argument-parsing library.
4. [Python Packaging](https://github.com/amirhaghajani/terminal-assistant/tree/04-python-packaging) — Turn the script into an installable Python package.
5. [Package Updates](https://github.com/amirhaghajani/terminal-assistant/tree/05-package-updates) — Explore package versioning, rebuilding distributions, and upgrading an installed package.
6. [Functions and Decorators](https://github.com/amirhaghajani/terminal-assistant/tree/06-python-functions-and-decorators) — Understand the Python concepts behind decorator-based frameworks.
7. [Typer](https://github.com/amirhaghajani/terminal-assistant/tree/07-typer-cli) — Build a CLI using decorators, function parameters, and type annotations.
8. [Ollama Integration](https://github.com/amirhaghajani/terminal-assistant/tree/08-ollama-integration) — Connect the application to a local language model.

Each stage builds on the previous one. We'll avoid jumping ahead and try to understand each new concept before using it.

## Stage 1: [Start with Plain Python](https://github.com/amirhaghajani/terminal-assistant/tree/01-plain-python)

I started with a simple Python file called `assistant.py`. No CLI frameworks, no external dependencies—just two ordinary Python functions.

```python
from pathlib import Path


def answer_question(question: str) -> str:
    return f"I received your question: {question}"


def create_file(filename: str, content: str) -> None:
    path = Path(filename)

    with path.open(mode="a", encoding="utf-8") as f:
        f.write(content + "\n")

    print(f"file created: {path}")


if __name__ == "__main__":
    answer = answer_question("What is Python?")
    print(answer)

    create_file("notes.txt", "My first assistant-created file.")
```

Running it:

```bash
python3 assistant.py
```

Output:

```text
I received your question: What is Python?
file created: notes.txt
```

The application has two features:

- `answer_question()` receives a question and returns a placeholder answer.
- `create_file()` creates a file or appends content to an existing one using `pathlib`.

I also used `if __name__ == "__main__"` to make sure the application code runs when the file is executed directly, rather than when it is imported by another module.

Everything works, but there is one problem: the question is hardcoded.

I don't want to edit the Python file every time I want to ask something different. I want to provide the question directly from the terminal.

**How can Python receive arguments from the command line? That's what we'll explore next.**

## Stage 2: [Building a CLI Manually with `sys.argv`](https://github.com/amirhaghajani/terminal-assistant/tree/02-manual-cli)

I wanted to run my application like this:

```bash
python3 assistant.py ask "What is Python?"
python3 assistant.py create-file notes.txt "Hello"
```

Python provides `sys.argv`, a list containing the arguments passed from the terminal.

For example:

```bash
python3 assistant.py ask "What is Python?"
```

Produces:

```python
[
    "assistant.py",
    "ask",
    "What is Python?"
]
```

I used this list to identify the command, extract its arguments, and decide what to execute.

The core of my implementation was a `match` statement:

```python

args = sys.argv

if len(args) < 2:
    show_help()
    return
    
command = args[1]

match command:
    case "ask":
        if len(args) < 3:
            print("Error: question is required.")
            return

        question = " ".join(args[2:])
        print(answer_question(question))

    case "create-file":
        if len(args) < 4:
            print("Error: filename and content are required.")
            return

        filename = args[2]
        content = " ".join(args[3:])
        create_file(filename, content)

    case _:
        print(f"Unknown command: {command}")
        show_help()
```

Now the application supports multiple commands, validates required arguments, and displays help information.

But I had to implement all the argument parsing and validation myself.

Wouldn't it be better if Python did some of this work for us?

That's where `argparse` comes in.

## Stage 3: [Using `argparse` to Handle Command-Line Arguments](https://github.com/amirhaghajani/terminal-assistant/tree/03-argparse-cli)

In Stage 2, I manually inspected `sys.argv` to identify commands and their arguments. It worked, but I had to handle argument parsing and validation myself.

Python already provides a built-in module for this: `argparse`.

I replaced most of my manual parsing code with an `ArgumentParser` and subcommands:

```python
parser = argparse.ArgumentParser(
    description="A simple terminal assistant"
)

subparsers = parser.add_subparsers(dest="command", required=True)

ask_parser = subparsers.add_parser(name="ask", help="Ask a question")
ask_parser.add_argument("question")

file_parser = subparsers.add_parser(name="create-file", help="Create a text file")
file_parser.add_argument("filename")
file_parser.add_argument("content")

args = parser.parse_args()
```

The `argparse` module now handles parsing the commands and their arguments. It also generates help messages and reports missing required arguments.

I still use a `match` statement to decide which function to execute:

```python
match args.command:
    case "ask":
        print(answer_question(args.question))

    case "create-file":
        create_file(args.filename, args.content)
```

This is much cleaner than manually inspecting `sys.argv`.

But I still have to run the application through Python:

```bash
python3 assistant.py ask "What is Python?"
```

I want to run it directly as `assistant ask ...`.

**How can I turn my Python script into an installable command-line application?**

## Stage 4: [Turning the Project into an Installable Python Package](https://github.com/amirhaghajani/terminal-assistant/tree/04-python-packaging)

Until now, I had to run my application using `python3 assistant.py`.

I wanted to run it directly:

```bash
assistant ask "What is Python?"
```

To achieve this, I reorganized the project using the `src/` layout:

```text
terminal-assistant/
├── pyproject.toml
└── src/
    └── terminal_assistant/
        ├── __init__.py
        └── cli.py
```

Then I created `pyproject.toml` to define the package metadata and build configuration.

The most interesting part was:

```toml
[project.scripts]
assistant = "terminal_assistant.cli:main"
```

This tells the packaging tool to create an `assistant` executable that invokes the `main()` function inside `terminal_assistant.cli`.

I used `setuptools` as the build backend and installed the project:

```bash
python -m pip install .
```

Now I could run `assistant` directly from the terminal.

I also learned how to build distribution files:

```bash
python -m pip install build
python -m build
```

This creates a wheel (`.whl`) and a source distribution (`.tar.gz`) inside the `dist/` directory.

**The CLI was now installable. But what happens when I change the application and want to install a newer version?**

## Stage 5: [Versioning and Upgrading the Package](https://github.com/amirhaghajani/terminal-assistant/tree/05-package-updates)

Now that I had an installable CLI, I wanted to understand how to release an updated version.

I changed the version in `pyproject.toml`:

```toml
[project]
name = "terminal-assistant"
version = "0.2.0"
```

Then I rebuilt the package:

```bash
python -m build
```

This generated new distribution files:

```text
dist/terminal_assistant-0.2.0-py3-none-any.whl
dist/terminal_assistant-0.2.0.tar.gz
```

But building a new version doesn't automatically update the package already installed on my machine.

I had to upgrade it explicitly:

```bash
python -m pip install --upgrade dist/terminal_assistant-0.2.0-py3-none-any.whl
```

Finally, I verified the installed version:

```bash
python -m pip show terminal-assistant
```

The result showed:

```text
Version: 0.2.0
```

I now understood the basic release cycle: update the version, rebuild the distributions, and upgrade the installed package.

**The next challenge was different. I wanted to understand how frameworks like Typer use Python functions and decorators to register CLI commands.**

## Stage 6: [Understanding Python Functions and Decorators](https://github.com/amirhaghajani/terminal-assistant/tree/06-python-functions-and-decorators)

Before using Typer, I wanted to understand something: how can a Python framework register a normal function as a CLI command using `@app.command()`?

Instead of memorizing the syntax, I decided to explore the underlying Python concepts.

I created several small examples to understand:

- Functions as objects.
- Passing functions as arguments.
- Returning functions.
- Wrapper functions and closures.
- Decorator syntax (`@`).
- Decorator factories.

One important discovery was that:

```python
@app.command()
def ask(question: str):
    ...
```

is not some special Python syntax. It's decorator syntax built on ordinary function behavior.

For example, this:

```python
@register
def ask():
    print("Question")
```

is equivalent to:

```python
def ask():
    print("Question")

ask = register(ask)
```

Understanding this made decorators much less mysterious.

I also explored decorator factories such as `@command()`, where calling the decorator factory returns the actual decorator.

This stage helped me understand what happens behind the scenes when frameworks register functions and add behavior to them.

**Now I was ready to return to the CLI project and use Typer.**

## Stage 7: [Building a CLI with Typer](https://github.com/amirhaghajani/terminal-assistant/tree/07-typer-cli)

After exploring Python decorators and function registration, I was ready to use Typer.

Previously, with `argparse`, I had to explicitly define every command and its arguments. With Typer, I could describe commands using ordinary Python functions.

For example, this was enough to register a command:

```python
@app.command("ask")
def ask(question: str):
    print(answer_question(question))
```

Typer uses the decorator to register the function, and its parameter and type hint to understand the command-line argument.

Our application became much simpler:

```python
import typer

app = typer.Typer(
    help="A simple terminal assistant",
    context_settings={"help_option_names": ["-h", "--help"]}
)

@app.command("ask")
def ask(question: str):
    print(answer_question(question))
```

I also learned that function parameters define CLI behavior:

- A parameter without a default value becomes a required argument.
- A parameter with a default value becomes an option.
- Type hints allow Typer to convert and validate input automatically.
- Boolean parameters can become command-line flags.

For example:

```python
def calculate(
    price: float,
    quantity: int,
    discount: bool = False
):
    print(price, quantity, discount)
```

Typer understands the expected types and generates the appropriate CLI interface.

Most importantly, I finally understood what happens behind this syntax:

```python
@app.command("ask")
def ask(question: str):
    ...
```

It's decorator-based function registration—not magic or special Python syntax.

I also discovered that Typer is built on Click, which provides much of its underlying command-line functionality.

At this point, I had a properly packaged CLI application with commands, arguments, options, automatic validation, and help generation.

But the assistant was still returning placeholder answers.

**It was time to connect it to a real LLM.**

## Stage 8: [Connecting the CLI to a Local LLM with Ollama](https://github.com/amirhaghajani/terminal-assistant/tree/08-ollama-integration)

Until now, our `ask` command returned a hardcoded response. I wanted to replace it with something real: a local LLM.

I chose Ollama to run a local model, `qwen3:14b`, and communicate with it through its HTTP API.

### Understanding the architecture

I separated the application into three responsibilities:

```text
Terminal
   |
   v
Typer CLI
   |
   v
answer_question()
   |
   v
ask_ollama()
   |
   v
Ollama HTTP API
   |
   v
Local LLM
```

This separation means the CLI doesn't need to know how HTTP communication works.

### Implementing the Ollama client

I created a new module:

```text
src/terminal_assistant/llm.py
```

Rather than introducing an HTTP client library, I decided to use Python's standard library:

```python
import json
from urllib.request import Request, urlopen
```

This gave me an opportunity to understand what happens when an application sends an HTTP request:

1. Build a Python dictionary containing the model and message.
2. Convert the dictionary into JSON.
3. Encode the JSON as UTF-8 bytes.
4. Send an HTTP POST request to Ollama.
5. Read and decode the response.
6. Parse the JSON and extract the generated text.

I also introduced `python-dotenv` to load the Ollama endpoint from a `.env` file rather than hardcoding a machine-specific URL.

### Handling errors

I created a custom exception called `OllamaError` to keep HTTP and connection errors inside the LLM module.

The Typer command catches this exception and reports the error to the terminal:

```python
@app.command("ask")
def ask(question: str):
    try:
        print(answer_question(question))
    except OllamaError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1)
```

I also tested what happens when Ollama is unavailable. The application displayed an error and returned exit code `1`, rather than pretending the operation had succeeded.

### The result

Now I could finally run:

```bash
assistant ask "What is dependency injection in Python?"
```

And receive an actual response from my local LLM.

The original placeholder:

```python
return f"I received your question: {question}"
```

had become a real call to Ollama.

**I started this project with one question: how does a Python function become a command in the terminal? Now I understand the journey—from sys.argv and argparse to Python packaging, Typer, and finally connecting the CLI to a local LLM.**