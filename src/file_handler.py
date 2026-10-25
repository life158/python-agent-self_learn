from pathlib import Path

def read_text(path:str|Path, encoding="utf-8")->str:
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    print(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')
    if not file_path.is_file():
        raise IsADirectoryError(f'File not file: {file_path}')
    return file_path.read_text(encoding=encoding)


if __name__ == '__main__':
    path1 = "data/chinese.txt"
    path2 ="data/empty.txt"
    path3 ="data/normal.txt"
    path4 = "data/test.txt"
    print("="*20)
    print(read_text(path1))
    print("="*20)
    print(read_text(path2))
    print("="*20)
    print(read_text(path4))
    print("=" * 20)
    print(read_text(path3))

