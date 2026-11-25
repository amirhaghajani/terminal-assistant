import argparse
from pathlib import Path


def answer_question(question:str) ->str:
    return f"I received your question: {question}"

def create_file(filename:str, content:str)->None:
    path = Path(filename)

    with path.open(mode="a", encoding="utf-8") as f:
        f.write(content+"\n")
    print(f"file created: {path}")

def show_help():
    print("""
        Terminal Assistant

        Usage:
            python3 assistant.py <command> [arguments]

        Commands:
            ask <question>                  Ask a question
            create-file <filename> <text>   Create a text file

        Options:
            -h, --help                      Show this help message

        Examples:
            python3 assistant.py ask "What is Python?"
            python3 assistant.py create-file notes.txt "Hello"
        """)

def main():
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

    match args.command:
        case "ask":
            print(answer_question(args.question))
            
        case "create-file":
            create_file(args.filename, args.content)

        case _:
            print(f"Unknown command: {args.command}")
            show_help()


if __name__ == "__main__":
    main()