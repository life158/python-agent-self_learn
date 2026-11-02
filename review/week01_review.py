#文件读取 --主要解决文件怎么读
import hashlib
import json
from json import JSONDecodeError
from pathlib import Path


def load_file(path:str):
    # 1.路径处理
   file_root = Path(__file__).resolve().parent.parent
   file_path = file_root.joinpath(path).resolve()
   # 2.判断路径
   if not file_path.exists():
        raise FileNotFoundError(f"文件不存在:{file_path}")
   if not file_path.is_file():
       raise  ValueError(f"该文件不是普通文件:{file_path}")
   #判断 suffix
   if file_path.suffix.lower() in (".txt",".md"):
       with open(file_path,"r",encoding="utf-8") as f:
           content = f.read()
   elif file_path.suffix.lower() ==".json":
       with open(file_path,"r",encoding="utf-8") as f:
           data = json.load(f)
       content = json.dumps(data,ensure_ascii=False)
   else:
       raise ValueError(f"该文件格式不支持:{file_path.suffix}")

   #统一处理
   return{"path":path,"content":content,"type":file_path.suffix.lower()}

# 文件指纹--用来识别文件
def fingerprint_file(path:str,algorithm:str = "sha256",chunk_size:int = 8192)->str:
    #Path
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    #文件检查
    if not file_path.exists():
        raise FileNotFoundError(f"该文件路径不存在:{file_path}")
    if not file_path.is_file():
        raise ValueError(f"该文件不是普通文件:{file_path}")
    if algorithm not in ("sha256","md5"):
        raise ValueError("该算法类型不支持")
    if type(chunk_size) is not int or chunk_size <= 0:
        raise ValueError("chunk_size必须为正整数")
    #创建hashlib对象
    hasher = hashlib.new(algorithm)
    with open(file_path,"rb",encoding="utf-8") as f:
        while True:
            content = f.read(chunk_size)
            if not content:
                break
            hasher.update(content)

    return hasher.hexdigest()

# FileTracker核心逻辑 --如何知道文件以前是否处理过
def load_index(path:str)->dict:
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    #判断路径
    if not file_path.exists():
        raise TypeError(f"该文件不存在:{file_path}")
    if not file_path.is_file():
        raise ValueError(f"该文件不是普通文件:{file_path}")
    if file_path.suffix.lower() !=".json":
        raise ValueError(f"该文件类型不支持处理")
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"索引文件已损坏:{file_path}") from e

def save_index(index_path:str,data:dict)->None:
    #Path
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(index_path).resolve()
    if not file_path.suffix.lower() == ".json":
        raise ValueError("该类型文件不支持处理")
    #确保文件父目录存在
    file_path.parent.mkdir(parents = True, exist_ok = True)
    with open(file_path,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def is_processed(data:dict,file_hash:str)->bool:
    for record in data["files"]:
        if record["hash"] == file_hash:
            return True
    return False

def add_file(data:dict,path:str,file_hash:str)->None:
    #Path对象
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    #获取文件的字节
    file_size = file_path.stat().st_size
    file_mtime = file_path.stat().st_mtime
    record = {"path":path,"hash":file_hash,"size":file_size,"mtime":file_mtime}
    data["files"].append(record)

def update_file(data:dict,path:str,file_hash:str)->bool:
    #Path对象
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    file_size = file_path.stat().st_size
    file_mtime = file_path.stat().st_mtime
    for record in data["files"]:
        if record["path"] == path:
            record["hash"] = file_hash
            record["size"] = file_size
            record["mtime"] = file_mtime
            return True
    print("未找到该文件")
    return False

















