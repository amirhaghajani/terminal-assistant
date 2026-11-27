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