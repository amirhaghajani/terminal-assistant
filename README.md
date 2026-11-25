# Terminal Assistant

A small Python project that starts with simple functions and gradually evolves into a command-line assistant.

This is the first stage of the project: a basic Python script.

## Current Features

- `answer_question()`: Receives a question and returns a placeholder response.
- `create_file()`: Creates a text file or appends content to an existing file.

## Requirements

- Python 3.10 or newer

## Run the application

```bash
python3 assistant.py
```

Example output:

```text
I received your question: What is Python?
```

## Project Structure

```text
terminal-assistant/
├── assistant.py
└── README.md
```

## What you'll learn

- Defining Python functions
- Using function parameters and return values
- Working with files using `pathlib.Path`
- Using the `__name__ == "__main__"` entry-point guard

## What's next?

In the next stage, we'll turn this simple script into a command-line application that accepts user input through terminal arguments.