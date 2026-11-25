from pathlib import Path


def answer_question(question:str) ->str:
    return f"I received your question: {question}"

def create_file(filename:str, content:str)->None:
    path = Path(filename)

    with path.open(mode="a", encoding="utf-8") as f:
        f.write(content+"\n")
    print(f"file created: {path}")


if __name__ == "__main__":
    answer = answer_question("What is Python?")
    print(answer)

    create_file("notes.txt", "My first assistant-created file.")