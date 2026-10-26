import hashlib
from pathlib import Path
from src.file_handler import load_file


def fingerprint_file(path:str,algorithm:str="sha256",chunk_size:int =8192)->str:
    # 接收文件路径并转化成Path对象
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')
    if not file_path.is_file():
        raise ValueError(f'File not file: {file_path}')
    #检查algorithm是否受支持
    if algorithm not in ('sha256','md5'):
        raise ValueError(f"{algorithm} is not supported")
    #检查chunk_size是否为正整数
    if type(chunk_size) != int or chunk_size<=0:
        raise ValueError(f"{chunk_size} is not supported")
    #根据algorithm创建哈希计算器
    hasher = hashlib.new(algorithm)
    #使用rb打开文件
    with open(file_path,'rb') as f:
        #循环读取固定大小数据块
        while True:
            content = f.read(chunk_size)
            # 将每个数据块交给哈希计算器
            if not content:
                break
            hasher.update(content)

    #返回十六进制摘要
    return hasher.hexdigest()





