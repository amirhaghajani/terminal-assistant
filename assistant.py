import sys
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
    args = sys.argv

    if len(args)<2 or args[1] in ("-h","--help"):
        show_help()
        return

    command = args[1]

    match command:
        case "ask":
            if len(args) < 3:
                print("Error: question is required.")
                return
            
            question = " ".join(args[2:])
            print(answer_question(question))
            
        case "create-file":
            if len(args) < 4:
                print("Error: filename and content are required.")
                return

            filename = args[2]
            content = " ".join(args[3:])
            create_file(filename, content)

        case _:
            print(f"Unknown command: {command}")
            show_help()


if __name__ == "__main__":
    main()