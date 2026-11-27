# Stage 8 — Connecting a Python CLI to Ollama

In the previous stages, we built a command-line application using plain Python, `sys.argv`, `argparse`, Python packaging, and Typer.

Our CLI could accept commands, but it didn't actually use an AI model.

In this stage, we'll connect our terminal assistant to a local Large Language Model (LLM) running through **Ollama**.

Our goal is to send a question from the terminal to Ollama and display the model's response.

## 1. What are we building?

Our CLI supports these commands:

```bash
assistant --help

assistant ask "What is RAG?"

assistant create-file notes.txt "Hello from Typer"
```

Now, instead of returning a hardcoded response, the `ask` command sends the question to a real LLM.

For example:

```bash
assistant ask "What is dependency injection in Python?"
```

The assistant sends the question to Ollama and displays the model's answer.

## 2. Understanding the architecture

Our application has three main responsibilities:

1. **CLI:** Receives commands and arguments from the terminal.
2. **LLM client:** Communicates with Ollama.
3. **Ollama:** Runs the local language model and generates responses.

The flow looks like this:

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
   |
   v
Response
```

We keep the Ollama communication separate from the CLI implementation. This makes it easier to replace or extend the LLM integration later.

## 3. Understanding Ollama's HTTP API

Ollama provides an HTTP API that allows other applications to communicate with locally running models.

For this project, we use the chat endpoint:

```text
POST /api/chat
```

Our application sends a JSON request containing:

- The model name.
- The conversation messages.
- The streaming configuration.

For example:

```json
{
    "model": "qwen3:14b",
    "messages": [
        {
            "role": "user",
            "content": "What is RAG?"
        }
    ],
    "stream": false
}
```

We set `stream` to `false` because we want to receive the complete response in one HTTP response rather than receiving it in multiple chunks.

You can test the API independently with `curl`:

```bash
curl http://YOUR_OLLAMA_HOST:11434/api/chat \
  -d '{
    "model": "qwen3:14b",
    "messages": [
      {"role": "user", "content": "What is RAG?"}
    ],
    "stream": false
  }'
```

Replace `YOUR_OLLAMA_HOST` with the address where your Ollama server is accessible.

## 4. Why do we use Python's standard library?

We could use an HTTP library such as `requests` or an Ollama-specific Python package.

However, for this learning stage, we'll use Python's standard library for HTTP communication and JSON processing.

We need three modules:

```python
import json
from urllib.request import Request, urlopen
```

- `json` converts Python dictionaries into JSON and parses JSON responses.
- `Request` represents an HTTP request.
- `urlopen` sends the request and returns the HTTP response.

This lets us understand what's happening underneath before introducing another dependency.

We'll use one small external package, `python-dotenv`, to manage environment-based configuration.

## 5. Configuring the Ollama endpoint

We don't want to hardcode a machine-specific URL in our Python source code.

Instead, we'll use an environment variable named `OLLAMA_API_URL`.

First, install the project dependencies:

```bash
uv sync
```

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and configure the Ollama API URL:

```env
OLLAMA_API_URL=http://localhost:11434/api/chat
```

If Ollama runs on another machine, replace `localhost` with the address where that server is accessible.

For example, when running the Python application inside WSL and Ollama on Windows, you may need to use the Windows host's accessible WSL network address.

Our project includes two environment files:

- `.env.example` is a configuration template committed to Git.
- `.env` contains your actual local configuration and is excluded from Git through `.gitignore`.

This allows different developers to use different Ollama endpoints without changing the application source code.

## 6. Implementing the Ollama client

Create a new file:

```text
src/terminal_assistant/llm.py
```

Our implementation:

```python
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/chat"
)
MODEL = "qwen3:14b"


class OllamaError(Exception):
    """Raised when communication with Ollama fails."""


def ask_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["message"]["content"]

    except HTTPError as error:
        raise OllamaError(
            f"Ollama returned HTTP {error.code}: {error.reason}"
        ) from error

    except (URLError, TimeoutError) as error:
        raise OllamaError(
            f"Could not connect to Ollama: {error}"
        ) from error

    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise OllamaError(
            f"Invalid response from Ollama: {error}"
        ) from error
```

**Important:** We load the Ollama endpoint from an environment variable instead of hardcoding it. `load_dotenv()` loads variables from the `.env` file, and `os.getenv()` retrieves the configured URL. If the variable is not defined, the application uses localhost as a fallback.

### Understanding the implementation

**Loading the configuration**

```python
load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/chat"
)
```

There are two important functions here:

- `load_dotenv()` reads the `.env` file and loads its variables into the process environment.
- `os.getenv()` retrieves an environment variable.

The second argument to `os.getenv()` is a default value. If `OLLAMA_API_URL` isn't defined, the application uses the localhost URL.

This separates application configuration from application code.

**Building the payload**

```python
payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False
}
```

This is an ordinary Python dictionary. We later convert it into JSON.

**Creating the HTTP request**

```python
request = Request(
    OLLAMA_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)
```

There are two important conversions here:

1. `json.dumps(payload)` converts the Python dictionary into a JSON string.
2. `.encode("utf-8")` converts that string into bytes.

The HTTP request body is sent as bytes.

We also specify the content type so the server knows that the request body contains JSON.

**Sending the request**

```python
with urlopen(request, timeout=120) as response:
    result = json.loads(response.read().decode("utf-8"))
```

The process is:

1. `urlopen()` sends the HTTP request.
2. `response.read()` reads the response body as bytes.
3. `.decode("utf-8")` converts those bytes into a string.
4. `json.loads()` converts the JSON string into a Python object.

Finally:

```python
return result["message"]["content"]
```

We extract the actual text generated by the model.

## 7. Understanding custom exceptions

We introduced our own exception:

```python
class OllamaError(Exception):
    """Raised when communication with Ollama fails."""
```

Why?

Because our CLI shouldn't need to understand the details of HTTP errors, URL errors, or invalid JSON.

The LLM module handles those technical details and raises one application-specific exception: `OllamaError`.

For example:

```python
except (URLError, TimeoutError) as error:
    raise OllamaError(
        f"Could not connect to Ollama: {error}"
    ) from error
```

The `from error` part is called **exception chaining**.

It preserves the original exception as the cause of the new exception. This is useful when debugging because we don't lose the underlying error.

## 8. Connecting the LLM client to Typer

Now we modify `cli.py`.

First, import our client:

```python
from terminal_assistant.llm import OllamaError, ask_ollama
```

Then replace our previous hardcoded implementation:

```python
def answer_question(question: str) -> str:
    return f"I received your question: {question}"
```

With:

```python
def answer_question(question: str) -> str:
    return ask_ollama(question)
```

The CLI command handles errors:

```python
@app.command("ask")
def ask(question: str):
    try:
        print(answer_question(question))
    except OllamaError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1)
```

Notice the separation:

- `ask_ollama()` handles communication with Ollama.
- `answer_question()` represents our application's question-answering logic.
- `ask()` handles terminal interaction and CLI errors.

The CLI doesn't need to know how HTTP communication works.

## 9. Testing the application

First, make sure Ollama is running and accessible.

Ask a question:

```bash
assistant ask "What is Python?"
```

The application should display the actual model response.

We should also test the failure path.

Stop Ollama and run:

```bash
assistant ask "What is Python?"
```

Expected output will look similar to:

```text
Error: Could not connect to Ollama: <urlopen error ...>
```

Check the exit code:

```bash
echo $?
```

Expected result:

```text
1
```

This confirms that our CLI reports a failed operation correctly instead of silently succeeding.

## 10. What did we learn?

In this stage, we learned:

- How to communicate with Ollama through its HTTP API.
- How to construct HTTP POST requests using Python's standard library.
- How to serialize and deserialize JSON.
- How to use environment variables for application configuration.
- How to use `python-dotenv` to load configuration from a `.env` file.
- How to separate LLM communication from CLI logic.
- How to define custom exceptions.
- How exception chaining works.
- How to handle errors in a Typer command.
- Why CLI applications should return a non-zero exit code when a command fails.

## Conclusion

Our terminal assistant can now communicate with a real local LLM.

We've built the CLI step by step, from plain Python to a packaged Typer application connected to Ollama.