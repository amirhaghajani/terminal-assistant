# Stage 7 — Building a CLI with Typer

In the previous stages, we built a command-line application using plain Python, manual argument parsing, and `argparse`. We also explored Python functions, function references, decorators, and function registration.

In this stage, we'll use **Typer** to build the CLI.

Our goal is to achieve the same functionality with less boilerplate and a more Pythonic approach.

## 1. What are we building?

Our terminal assistant supports these commands:

```bash
assistant --help

assistant ask "What is RAG?"

assistant create-file notes.txt "Hello from Typer"
```

Expected output:

```text
I received your question: What is RAG?
```

For file creation:

```text
file created: notes.txt
```

## 2. Why Typer?

Before Typer, we used `argparse` to define commands and their arguments.

For example:

```python
ask_parser = subparsers.add_parser(
    name="ask",
    help="Ask a question"
)

ask_parser.add_argument("question")
```

We had to explicitly define the command and its arguments.

With Typer, we can express the same information using Python functions and decorators:

```python
@app.command("ask")
def ask(question: str):
    print(f"I received your question: {question}")
```

Typer uses the function name, parameters, and type hints to construct the command-line interface.

## 3. Installing Typer

Add Typer to the project's dependencies in `pyproject.toml`:

```toml
[project]
dependencies = [
    "typer>=0.29.2,<1.0.0"
]
```

Install the project in editable mode:

```bash
python -m pip install -e .
```

Editable installation means that changes to our Python source files are immediately available without reinstalling the package.

## 4. Understanding the application

Our application is defined in:

`src/terminal_assistant/cli.py`

```python
from pathlib import Path
import typer

app = typer.Typer(
    help="A simple terminal assistant",
    context_settings={"help_option_names": ["-h", "--help"]}
)


def answer_question(question: str) -> str:
    return f"I received your question: {question}"


@app.command("ask")
def ask(question: str):
    print(answer_question(question))


@app.command("create-file")
def create_file(filename: str, content: str) -> None:
    path = Path(filename)

    with path.open(mode="a", encoding="utf-8") as f:
        f.write(content + "\n")

    print(f"file created: {path}")


def main():
    app()


if __name__ == "__main__":
    main()
```

Let's understand the important parts.

### Creating the Typer application

```python
app = typer.Typer(
    help="A simple terminal assistant"
)
```

This creates our CLI application.

We use `app` to register commands.

### Registering a command

```python
@app.command("ask")
def ask(question: str):
    print(answer_question(question))
```

The decorator registers the `ask` function as a CLI command.

The command name is explicitly specified as `"ask"`.

Typer reads the function signature and understands that `question` is a required string argument.

We can now execute:

```bash
assistant ask "What is RAG?"
```

### Understanding the decorator

We previously learned that:

```python
@app.command()
def ask(question: str):
    ...
```

is conceptually similar to:

```python
def ask(question: str):
    ...

ask = app.command()(ask)
```

`app.command()` returns a decorator. That decorator receives the `ask` function and registers it with the application.

The actual Typer implementation is more sophisticated, but this model helps us understand the registration mechanism.

### Separating business logic from CLI interaction

Notice that we have two functions:

```python
def answer_question(question: str) -> str:
    return f"I received your question: {question}"
```

And:

```python
@app.command("ask")
def ask(question: str):
    print(answer_question(question))
```

`answer_question` contains business logic. It returns a string.

`ask` handles the CLI interaction and displays the result.

This separation is useful because we can later replace the placeholder implementation with an actual LLM call without coupling our business logic to Typer.

## 5. How Typer interprets function parameters

One of Typer's most useful features is that it uses Python type hints and default values to define CLI arguments and options.

Consider:

```python
@app.command()
def calculate(
    price: float,
    quantity: int,
    discount: bool = False
):
    print(price, quantity, discount)
```

Typer interprets the parameters as follows:

| Python parameter | CLI behavior |
|---|---|
| `price: float` | Required positional argument |
| `quantity: int` | Required positional argument |
| `discount: bool = False` | Optional Boolean flag |

Without the discount flag:

```bash
assistant calculate 12.5 3
```

Output:

```text
12.5 3 False
```

With the discount flag:

```bash
assistant calculate 12.5 3 --discount
```

Output:

```text
12.5 3 True
```

### Positional arguments and options

Consider:

```python
def download(url: str, output: str = "download.zip"):
    print(url, output)
```

Because `url` has no default value, Typer treats it as a required positional argument.

Because `output` has a default value, Typer treats it as an option.

These commands are valid:

```bash
assistant download https://example.com

assistant download https://example.com --output file.zip
```

By default, the option name comes from the parameter name. For example, `has_discount` becomes `--has-discount`.

You can also explicitly configure arguments and options using `typer.Argument()` and `typer.Option()`.

## 6. Automatic type conversion and validation

Type hints are not just documentation.

Consider:

```python
def calculate(price: float, quantity: int):
    print(price * quantity)
```

When we execute:

```bash
assistant calculate 12.5 3
```

Typer converts the terminal input into the appropriate Python types:

```python
price = 12.5       # float
quantity = 3       # int
```

But if we execute:

```bash
assistant calculate 12.5 three
```

Typer rejects the invalid integer input before calling our function.

This means we don't have to manually convert every command-line argument or write basic type-validation logic ourselves.

## 7. Understanding Click

Typer is built on Click's command-line infrastructure.

Click provides functionality for:

- Command-line argument parsing
- Commands and groups
- Options and arguments
- Help generation
- Shell completion

Typer provides a more convenient Python interface by using function signatures, decorators, and type hints.

Instead of explicitly declaring every CLI argument, we can often describe our command using an ordinary Python function.

One detail about our installed version: Typer 0.29.2 vendors Click internally.

## 8. Customizing help options

By default, our previous `argparse` implementation supported both:

```bash
assistant -h
assistant --help
```

Our Typer application initially supported `--help`, but not `-h`.

We configured both options using:

```python
app = typer.Typer(
    help="A simple terminal assistant",
    context_settings={
        "help_option_names": ["-h", "--help"]
    }
)
```

Now both commands work.

## 9. Why do we keep `main()`?

Our `pyproject.toml` contains:

```toml
[project.scripts]
assistant = "terminal_assistant.cli:main"
```

This tells the Python packaging system to create an executable command named `assistant` that calls the `main` function.

Our entry point is:

```python
def main():
    app()
```

We could call `app()` directly, but keeping `main()` preserves the existing package entry point.

## 10. Running the application

Install the project:

```bash
python -m pip install -e .
```

Display application help:

```bash
assistant --help
assistant -h
```

Display command help:

```bash
assistant ask --help
assistant create-file --help
```

Ask a question:

```bash
assistant ask "What is RAG?"
```

Create a file:

```bash
assistant create-file notes.txt "Hello from Typer"
```

## 11. What did we learn?

In this stage, we learned:

- Creating a Typer application.
- Registering commands with decorators.
- Understanding how `@app.command()` works.
- Using Python function parameters as CLI arguments.
- Understanding positional arguments and options.
- Using Boolean parameters as CLI flags.
- Automatic type conversion and validation.
- The relationship between Typer and Click.
- Customizing CLI help options.
- Preserving our Python package entry point.

## What's next?

We now have a working CLI built with Typer.

In the next stage, we'll continue improving our terminal assistant and move closer to our original goal: an assistant that can communicate with a local LLM through Ollama.