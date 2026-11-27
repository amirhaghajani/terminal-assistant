from pathlib import Path
import typer
from terminal_assistant.llm import ask_ollama, OllamaError

app = typer.Typer(
    help="A simple terminal assistant",
    context_settings={"help_option_names": ["-h", "--help"]}
)


def answer_question(question: str) -> str:
    return ask_ollama(question)


@app.command("ask")
def ask(question: str):
    try:
        print(answer_question(question))
    except OllamaError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1)

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