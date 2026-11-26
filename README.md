# Terminal Assistant

A small Python project that gradually evolves into an installable command-line application.

This is stage 4: converting the application into a Python package and creating an installable CLI command.

## What's new?

- Organized source code using the `src/` layout.
- Created a Python package named `terminal_assistant`.
- Added `pyproject.toml` for package configuration and metadata.
- Configured setuptools as the build backend.
- Registered the `assistant` terminal command.

## Project Structure

```text
terminal-assistant/
├── pyproject.toml
├── README.md
└── src/
    └── terminal_assistant/
        ├── __init__.py
        └── cli.py
```

## Requirements

- Python 3.10 or newer

## Development setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install .
```

## Using the CLI

Show available commands:

```bash
assistant --help
```

Ask a question:

```bash
assistant ask "What is an AI agent?"
```

Create a file:

```bash
assistant create-file notes.txt "Hello world"
```

## Build distributions

Install the build frontend:

```bash
python -m pip install build
```

Build the package:

```bash
python -m build
```

This creates two distribution formats in `dist/`:

- **Wheel (`.whl`)**: a built distribution that can be installed directly.
- **Source distribution (`.tar.gz`)**: the source package from which a distribution can be built.

## Important packaging concepts

- `pyproject.toml`: project metadata and build configuration.
- `setuptools`: the build backend.
- `build`: the frontend that invokes the backend.
- `pip`: the package installer.
- `project.scripts`: maps the `assistant` command to `terminal_assistant.cli:main`.

## What's next?

In stage 5, we'll explore package versioning and upgrade an already installed CLI application.