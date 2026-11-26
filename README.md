# Terminal Assistant

A small Python project that gradually evolves into an installable command-line application.

This is stage 5: understanding package versioning and upgrading an already-installed CLI application.

## What's new?

- Updated the package version from `0.1.0` to `0.2.0`.
- Rebuilt the package with the new version.
- Upgraded the previously installed CLI using the new wheel.
- Verified that the installed package reports version `0.2.0`.
- Confirmed that the CLI commands still work after upgrading.

## Project structure

```text
terminal-assistant/
├── pyproject.toml
├── README.md
└── src/
    └── terminal_assistant/
        ├── __init__.py
        └── cli.py
```

## Versioning

The package version is defined in `pyproject.toml`:

```toml
[project]
name = "terminal-assistant"
version = "0.2.0"
```

When you change the version, you must rebuild the distributions. The new version number becomes part of the generated distribution filenames and package metadata.

## Build the new version

```bash
python -m build
```

This creates:

- `dist/terminal_assistant-0.2.0-py3-none-any.whl`
- `dist/terminal_assistant-0.2.0.tar.gz`

## Upgrade an installed package

Install or upgrade the package using its new wheel:

```bash
python -m pip install --upgrade dist/terminal_assistant-0.2.0-py3-none-any.whl
```

Check the installed version:

```bash
python -m pip show terminal-assistant
```

You should see:

```text
Version: 0.2.0
```

## Verify the CLI

```bash
assistant --help
assistant ask "What is an AI agent?"
assistant create-file notes.txt "Hello from version 0.2.0"
```

The commands should continue working after the upgrade.

## Important concepts

- **Package version:** Identifies a particular release of your application.
- **Build:** Generates distributions from the current source code and metadata.
- **Upgrade:** Replaces an installed package with a newer version.
- **Wheel:** A built distribution that can be installed directly using pip.
- **pip:** Handles package installation and upgrades.

## What's next?

In stage 6, we'll improve the CLI implementation and explore a more convenient way to define commands and arguments.