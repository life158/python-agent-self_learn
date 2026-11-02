from encodings import utf_8
from pathlib import Path

def read_file(path, encoding="utf-8")->str:
    file_path = Path(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path} is not a file")
    return file_path.read_text(encoding=encoding)

if __name__ == "__main__":
    path = ("./data/samples.txt")
    print(read_file(path))


