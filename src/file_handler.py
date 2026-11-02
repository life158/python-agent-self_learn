import json
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

def load_file(path:str)->dict:
    # 接收文件路径并转化成Path对象
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')
    if not file_path.is_file():
        raise ValueError(f'File not file: {file_path}')
    # 对文件进行分类处理
    file_suffix = file_path.suffix.lower()
    if file_suffix in ('.txt', '.md'):
        with open(file_path, 'r', encoding="utf_8") as f:
            content = f.read()

    elif file_suffix == ".json":
        with open(file_path, 'r', encoding="utf_8") as f:
            data = json.load(f)
        content = json.dumps(data, ensure_ascii=False)

    else:
        raise TypeError(f'File not supported: {file_suffix}')

    #统一处理
    return {
            "content": content,
            "path": str(file_path),
            "type": file_suffix,
        }



if __name__ == '__main__':
    path1 = "data/chinese.txt"
    path2 ="data/example.json"
    path3 ="data/example.md"
    print("="*20)
    print(load_file(path1))
    print("="*20)
    print(load_file(path2))
    print("="*20)
    print(load_file(path3))

