# Terminal Assistant

A small Python project that gradually evolves into a command-line assistant.

This is stage 3: replacing manual argument parsing with Python's built-in `argparse` library.

## Features

- `ask`: Accepts a question and returns a placeholder response.
- `create-file`: Creates a text file or appends content to an existing file.
- Automatic help generation.
- Automatic validation of required command arguments.
- Command dispatch using `match/case`.

## Requirements

- Python 3.10 or newer

## Run the application

Show available commands:

```bash
python3 assistant.py --help
```

Ask a question:

```bash
python3 assistant.py ask "What is Python?"
```

Create a file:

```bash
python3 assistant.py create-file notes.txt "Hello world"
```

## How it works

The application uses:

- `argparse.ArgumentParser` to define the CLI.
- Subparsers to define commands such as `ask` and `create-file`.
- `add_argument()` to declare required arguments.
- `parse_args()` to parse and validate user input.
- `match/case` to dispatch the parsed command.

## Project Structure

```text
terminal-assistant/
├── assistant.py
└── README.md
```

## What you'll learn

- Defining CLI commands with `argparse`
- Using subparsers
- Declaring positional arguments
- Automatic help and argument validation
- Separating argument parsing from application logic

## Improvement over stage 2

In stage 2, we manually inspected `sys.argv`, checked argument counts, and generated help text ourselves.

Now `argparse` handles those responsibilities, making the CLI simpler and easier to extend.

## What's next?

In stage 4, we'll organize the application as a Python package and make it installable as a command-line tool.