# Terminal Assistant

A small Python project that gradually evolves into a command-line assistant.

This is stage 2: building a CLI manually using Python's `sys.argv`.

## Features

- `ask`: Accepts a question and returns a placeholder response.
- `create-file`: Creates a text file or appends content to an existing file.
- `--help`: Displays available commands and usage instructions.
- Manual argument validation and error handling.

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

- `sys.argv` to read command-line arguments.
- `match/case` to dispatch commands.
- Manual checks to validate required arguments.
- `pathlib.Path` to work with files.

## Project Structure

```text
terminal-assistant/
├── assistant.py
└── README.md
```

## What you'll learn

- Reading command-line arguments with `sys.argv`
- Building a CLI without external libraries
- Parsing commands and arguments manually
- Validating user input
- Handling basic CLI errors

## Limitations

Argument parsing and validation are implemented manually. As the application grows, this approach becomes harder to maintain.

## What's next?

In stage 3, we'll replace manual argument parsing with Python's built-in `argparse` library.